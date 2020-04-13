typedef struct {
    float3 pos;
    float3 vel;
    float3 forces;
    float3 fluid_vel;
    ulong id;
    ulong cv_array_idx;
    float diameter;
    float effect_diameter;
    float density;
    float fluid_viscosity;
} __attribute__ ((aligned (128))) particle;

float get_particle_mass(particle p) {
    if (p.density == -1) {
        return -1;
    } else {
        return (float) p.density * M_PI_F * pow(p.diameter, 3) / 6;
    }
}

