//
// Created by Elijah on 19/12/2017.
//

#include "test_alignment.h"

boolean test_particle_struct_alignment(cl_device_id device, cl_context context, boolean verbose) {
    particle *hparticles;
    cl_mem gparticles;
    cl_ulong NUMPART = 10;

    cl_int ret;
    cl_bool hcorrect = TRUE;
    cl_mem gcorrect;

    if (verbose) printf("\nTesting particle struct alignment.\n");

    cl_kernel kernel = getKernelWithUtils(device, context, PROJECT_DIR "/tests/test_alignment/alignment_test_kernels.cl",
                                          "test_particle_struct_alignment", verbose);
    cl_command_queue queue = getCommandQueue(context, device, verbose);

    hparticles = malloc(sizeof(particle) * NUMPART);

    for (cl_ulong i = 0; i < NUMPART; i++) {
        hparticles[i].pos = (cl_float3) {20, 21, 22};
        hparticles[i].vel = (cl_float3) {23, 24, 25};
        hparticles[i].forces = (cl_float3) {26, 27, 28};
        hparticles[i].fluid_vel = (cl_float3) {29, 30, 31};
        hparticles[i].id = 32;
        hparticles[i].cv_array_idx = 33;
        hparticles[i].diameter = 34;
        hparticles[i].effect_diameter = 35;
        hparticles[i].density = 36;
        hparticles[i].fluid_viscosity = 37;
    }

    gparticles = clCreateBuffer(context, CL_MEM_READ_WRITE, sizeof(particle) * NUMPART, NULL, &ret);
    gcorrect = clCreateBuffer(context, CL_MEM_READ_WRITE, sizeof(boolean), NULL, &ret);

    ret = particlesToDevice(queue, gparticles, &hparticles, NUMPART);
    ret = clEnqueueWriteBuffer(queue, gcorrect, CL_TRUE, 0, sizeof(boolean), &hcorrect, 0, NULL, NULL);

    ret = clSetKernelArg(kernel, 0, sizeof(cl_mem), &gparticles);
    ret = clSetKernelArg(kernel, 1, sizeof(cl_mem), &gcorrect);

    ret = clEnqueueNDRangeKernel(queue, kernel, 1, NULL, (size_t *) &NUMPART, 0, NULL, NULL, NULL);

    ret = particlesToHost(queue, gparticles, &hparticles, NUMPART);
    ret = clEnqueueReadBuffer(queue, gcorrect, CL_TRUE, 0, sizeof(boolean), &hcorrect, 0, NULL, NULL);

    ret = clFinish(queue);

    if (!hcorrect) {
        return FALSE;
    }

    for (int i = 0; i < NUMPART; i++) {
        particle p = hparticles[i];
        if (!(p.pos.x == 80 &&
              p.pos.y == 81 &&
              p.pos.z == 82 &&
              p.vel.x == 83 &&
              p.vel.y == 84 &&
              p.vel.z == 85 &&
              p.forces.x == 86 &&
              p.forces.y == 87 &&
              p.forces.z == 88 &&
              p.fluid_vel.x == 89 &&
              p.fluid_vel.y == 90 &&
              p.fluid_vel.z == 91 &&
              p.id == 92 &&
              p.cv_array_idx == 93 &&
              p.diameter == 94 &&
              p.effect_diameter == 95 &&
              p.density == 96 &&
              p.fluid_viscosity == 97)) {
            hcorrect = FALSE;
        }
    }
    return (boolean) hcorrect;
}
