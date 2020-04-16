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

char prefix[50];
char folder[50];
char dir[50];

particle *hparticles;
cl_ulong NUMPART = 1;

cl_float density = 997;
cl_float particle_diameter = 0.05;
cl_float fluid_viscosity = 0.1;

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

    char *iterate_particle_files[] = {PROJECT_DIR "/util/kernelUtils.cl",
                                      PROJECT_DIR "/kernels/get_gravity/gravity.cl",
                                      PROJECT_DIR "/kernels/get_vel_fluid/no_fluid_flow.cl",
                                      PROJECT_DIR "/kernels/iterate_particle.cl"};
    cl_kernel iterate_particle = getKernel(device, context, iterate_particle_files, 4, "iterate_particle", TRUE);

    hparticles = malloc(sizeof(particle) * NUMPART);

    hparticles[0].diameter = particle_diameter;
    hparticles[0].effect_diameter = 0;
    hparticles[0].fluid_viscosity = fluid_viscosity;
    hparticles[0].density = density;
    hparticles[0].id = 0;
    hparticles[0].pos = (cl_float3) {0, 0, 0};
    hparticles[0].vel = (cl_float3) {0, 0, 0};
    hparticles[0].forces = (cl_float3) {0, 0, 0};

    float tau = get_tau(&(hparticles[0]));
    sim_length = 10 * tau;

    domain_length = 0.5;
    printf("Mass = %f\n", get_particle_mass(&(hparticles[0])));
    printf("Tau = %f\n", tau);

    char dir[] = PROJECT_DIR "/verification/gravity_drag/data/";
    for (float i = 1; i <= 10; i += 1) {
        timestep = tau * (i/10);
        log_step = timestep;

        sprintf(prefix, "gravity_drag");
        char c[50];
        float a = i/10.0;
        sprintf(c, "%.1f", a);
        char *token = strtok(c, ".");
        char *num[2];
        int j = 0;
        while (token){
            num[j++] = token;
            token = strtok(NULL, ".");
        }

        snprintf(folder, sizeof(folder), "%s%s%s%s%s", "gravity_drag_", num[0], "_", num[1], "_tau/");
        sprintf(dir, "%s%s", PROJECT_DIR "/verification/gravity_drag/data/", folder);
        hparticles[0].pos = (cl_float3) {0, 0, 0};
        hparticles[0].vel = (cl_float3) {0, 0, 0};

        runSim(hparticles, NUMPART, iterate_particle, particle_diameter, FALSE, domain_length,
               prefix, dir, sim_length, timestep, VERBOSE, LOG_DATA, TRUE, log_step, device, context);
    }

    timestep = tau * 0.001;
    log_step = timestep;
    snprintf(folder, sizeof(folder), "%s%s%s%s%s", "gravity_drag_", "0", "_", "001", "_tau/");
    sprintf(dir, "%s%s", PROJECT_DIR "/verification/gravity_drag/data/", folder);
    hparticles[0].pos = (cl_float3) {0, 0, 0};
    hparticles[0].vel = (cl_float3) {0, 0, 0};

    runSim(hparticles, NUMPART, iterate_particle, particle_diameter, FALSE, domain_length,
           prefix, dir, sim_length, timestep, VERBOSE, LOG_DATA, TRUE, log_step, device, context);

}