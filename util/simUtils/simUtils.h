//
// Created by Elijah on 15/02/2018.
//

#ifndef DEMORANGES_SIMUTILS_H
#define DEMORANGES_SIMUTILS_H

#include "../../structures/particle.h"
#include <stdbool.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <stdio.h>
#include <malloc.h>
#include <string.h>

#if defined(_MSC_VER)

#include <sys/stat.h>

#elif defined(__GNUC__) || defined(__GNUG__) || defined(__MINGW_GCC_VERSION)
#include <dirent.h>
#include <errno.h>
#endif

#if defined(_MSC_VER)

#include <Windows.h>

#endif

// If boolean is not correctly defined.
#if !defined(boolean)
#define boolean bool
#if !defined(_MSC_VER)
#define TRUE true
#define FALSE false
#endif
#endif

int writeParticles(particle *particles, float time, char *prefix, char *dir, cl_ulong NUMPART, boolean log_vel);

int writeSetupData(char prefix[], char dir[], cl_ulong NUMPART, cl_float timestep, cl_float sim_length,
                   cl_float domain_length,
                   cl_float particle_diameter, cl_float effect_diameter, cl_float particle_density,
                   cl_float fluid_viscosity);

int writeTime(char prefix[], char dir[], cl_ulong NUMPART, char label[]);

boolean checkDirExists(char dir[]);

float getFluidViscFromStks(float diameter, float density, float flow_speed, float length, float stks);

float getRestitutionFromSy(float eff_len, float k_c, float u, float mass, float sy);

float getCohesionFromSy(float eff_len, float restitution, float u, float mass, float sy);

#endif //DEMORANGES_SIMUTILS_H
