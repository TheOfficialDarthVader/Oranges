//
// Created by akern on 02/04/2020.
//

#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else

#include <CL/cl.h>

#endif

#include <stdio.h>
#include "../../util/clUtils/clUtils.h"
#include "../../util/particleUtils/particleUtils.h"
#include "../../tests/run_tests/run_tests.h"
#include "../../util/simUtils/simUtils.h"
#include "../../sims/simRunner/simRunner.h"
#include <malloc.h>

#define MAX_SOURCE_SIZE (0x100000)
#define VERBOSE FALSE
#define LOG_DATA TRUE

char *prefix[50];
char folder[200];
char dir[200];

particle *hparticles;
cl_ulong NUMPART = 100;

cl_float density = 2000;
cl_float particle_diameter = 0.05;
cl_float particle_effect_diameter;
cl_float fluid_viscosity;

cl_bool periodic = CL_TRUE;

float init_speed_mean = 1;
float init_speed_std_dev = 0.1;

cl_float timestep;
cl_float sim_length;
cl_float log_step;

cl_float domain_length;

cl_context context;
cl_device_id device;

int main() {

    // Initializing OpenCL.
    setContext(&device, &context, TRUE);

    // Run tests
    if (!run_all_tests(device, context, FALSE)) {
        return 1;
    }

    // Build iterate_particle kernel.
    char *iterate_particle_files[] = {PROJECT_DIR "/util/kernelUtils.cl",
                                      PROJECT_DIR "/kernels/get_gravity/no_gravity.cl",
                                      PROJECT_DIR "/kernels/get_vel_fluid/tgv.cl",
                                      PROJECT_DIR "/kernels/iterate_particle.cl"};
    cl_kernel iterate_particle = getKernel(device, context, iterate_particle_files, 4, "iterate_particle", TRUE);

    hparticles = malloc(sizeof(particle) * NUMPART);
    if (hparticles == NULL) {
        fprintf(stderr, "Particles memory allocation failed.\n");
        return 1;
    }

    float stks[] = {0.1, 1.0, 10.0};
    particle_effect_diameter = (cl_float) (1.5 * particle_diameter);

    for (int i = 0; i < 3; i += 1) {
        printf("stokes %f\n", stks[0]);
        fluid_viscosity = getFluidViscFromStks(particle_diameter, density, 0.7839 * 5, PI / 3, stks[i]);

        printf("[INIT] Creating particle positions.\n");
        cl_float3 *positions = malloc(sizeof(cl_float3) * NUMPART);
        // Using particle_effect_diameter so that cohesion effects are considered at the appropriate range.
        float cube_length = createCubePositions(positions, NUMPART, particle_effect_diameter, 2,
                                                (cl_float3) {0, 0, 0});
        domain_length = (cl_float) (2 * PI);
        if (cube_length > domain_length) {
            fprintf(stderr, "Not all particles fit within the specified domain length for the given cube parameters (%.3f > %.3f).", cube_length, domain_length);
            return 1;
        }

        cl_float3 *velocities = malloc(sizeof(cl_float3) * NUMPART);
        createNormalDistVelocities(velocities, NUMPART, init_speed_mean, init_speed_std_dev);

        // Initialize particles.
        initializeMonodisperseParticles(hparticles, NUMPART, density, fluid_viscosity, particle_diameter,
                                        particle_effect_diameter, positions, velocities);
        free(positions);
        free(velocities);

        if (!checkPositions(hparticles, NUMPART, domain_length)) {
            fprintf(stderr, "Particles outside domain limits.\n");
            return 1;
        }

        float tau = get_tau(&(hparticles[0]));
        sim_length = 100 * tau;

        domain_length = 2 * PI;
        printf("Mass = %f\n", get_particle_mass(&(hparticles[0])));
        printf("Tau = %f\n", tau);

        timestep = tau / 8;
        log_step = timestep;

        sprintf(prefix, "tgv_stats");
        char c[50];
        sprintf(c, "%.1f", stks[i]);
        char *token = strtok(c, ".");
        char *num[2];
        int j = 0;
        while (token){
            num[j++] = token;
            token = strtok(NULL, ".");
        }

        snprintf(folder, sizeof(folder), "%s%s%s%s%s", "tgv_stats_stk_", num[0], "_", num[1], "/");
        sprintf(dir, "%s%s", PROJECT_DIR "verification/tgv_stats/data/", folder);
        printf("%.130s\n", dir);

        runSim(hparticles, NUMPART, iterate_particle, particle_diameter, FALSE, domain_length,
               prefix, dir, sim_length, timestep, VERBOSE, LOG_DATA, TRUE, log_step, device, context);
        clReleaseContext(context);
    }
}