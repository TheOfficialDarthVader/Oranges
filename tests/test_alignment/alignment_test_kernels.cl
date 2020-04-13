__kernel void test_particle_struct_alignment(__global particle *particles, __global bool *correct) {
        int gid = get_global_id(0);

        if (!(particles[gid].pos.x == 20 &&
              particles[gid].pos.y == 21 &&
              particles[gid].pos.z == 22 &&
              particles[gid].vel.x == 23 &&
              particles[gid].vel.y == 24 &&
              particles[gid].vel.z == 25 &&
              particles[gid].forces.x == 26 &&
              particles[gid].forces.y == 27 &&
              particles[gid].forces.z == 28 &&
              particles[gid].fluid_vel.x == 29 &&
              particles[gid].fluid_vel.y == 30 &&
              particles[gid].fluid_vel.z == 31 &&
              particles[gid].id == 32 &&
              particles[gid].cv_array_idx == 33 &&
              particles[gid].diameter == 34 &&
              particles[gid].effect_diameter == 35 &&
              particles[gid].density == 36 &&
              particles[gid].fluid_viscosity == 37)) {
            *correct = false;
        }

        particles[gid].pos.x = 80;
        particles[gid].pos.y = 81;
        particles[gid].pos.z = 82;
        particles[gid].vel.x = 83;
        particles[gid].vel.y = 84;
        particles[gid].vel.z = 85;
        particles[gid].forces.x = 86;
        particles[gid].forces.y = 87;
        particles[gid].forces.z = 88;
        particles[gid].fluid_vel.x = 89;
        particles[gid].fluid_vel.y = 90;
        particles[gid].fluid_vel.z = 91;
        particles[gid].id = 92;
        particles[gid].cv_array_idx = 93;
        particles[gid].diameter = 94;
        particles[gid].effect_diameter = 95;
        particles[gid].density = 96;
        particles[gid].fluid_viscosity = 97;
}
