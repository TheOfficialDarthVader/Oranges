# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import numpy as np


class data_processing():
    def __init__(self, root, tau):
        self.root = root
        self.tau = tau
        self.g = 9.81
        self.time = []
        self.time_nd = []
        self.x_pos = []
        self.y_pos = []
        self.z_pos = []
        self.x_vel = []
        self.y_vel = []
        self.z_vel = []
        self.x_fluid_vel = []
        self.y_fluid_vel = []
        self.z_fluid_vel = []
        self.ang_bar = []
        self.x_vel_bar = []
        self.y_vel_bar = []
        self.z_vel_bar = []
        self.num_particles = 0

    def sort_files(self):
        def key_func(x):
            return int(x.strip('.txt').split('_')[-1])

        self.files = [f for f in os.listdir(self.root)
                      if os.path.isfile(os.path.join(self.root, f))]
        if any("setup" in filename for filename in self.files):
            a = [x for x in self.files if "setup" in x]
        try:
            self.files.remove(a[0])
        except ValueError:
            print("No setup file")

        self.files.sort(key=key_func)  # sort files into "natural order"

    def read_files(self):
        for file in self.files:
            if file.endswith('.txt'):
                with open(os.path.join(self.root, file), 'r') as f:
                    self.time.append(int(file.strip('.txt')
                                     .split('_')[-1])/1000000)
                    self.time_nd.append(int(file.strip('.txt')
                                        .split('_')[-1])/1000000/self.tau)
                    text = f.readlines()
                    self.num_particles = len(text)
                    for i in range(len(text)):
                        self.x_pos.append(float(text[i].strip('\n')
                                          .split(',')[0]))
                        self.y_pos.append(float(text[i].strip('\n')
                                          .split(',')[1]))
                        self.z_pos.append(float(text[i].strip('\n')
                                          .split(',')[2]))
                        self.x_vel.append(float(text[i].strip('\n')
                                          .split(',')[3]))
                        self.y_vel.append(float(text[i].strip('\n')
                                          .split(',')[4]))
                        self.z_vel.append(float(text[i].strip('\n')
                                          .split(',')[5]))
                        self.x_fluid_vel.append(float(text[i].strip('\n')
                                                .split(',')[6]))
                        self.y_fluid_vel.append(float(text[i].strip('\n')
                                                .split(',')[7]))
                        self.z_fluid_vel.append(float(text[i].strip('\n')
                                                .split(',')[8]))
            else:
                pass

    def unit_vector(self, vector):
        """ Returns the unit vector of the vector.  """
        all_zeros = not np.any(vector)
        small_magnitude = np.isclose([vector], [0.000001, 0.000001, 0.000001],
                                     atol=0.000002)
        if all_zeros is True:
            return([0, 0, 0])
        # e.g. if (0.000000,0.000000,0.000001) then return (0,0,0)
        if all(small_magnitude[0]) is True:
            return([0, 0, 0])
        else:
            return(vector/np.linalg.norm(vector))

    def angle_between(self, v1, v2):
        """ Returns the angle in radians between vectors 'v1' and 'v2'::

                >>> angle_between((1, 0, 0), (0, 1, 0))
                1.5707963267948966
                >>> angle_between((1, 0, 0), (1, 0, 0))
                0.0
                >>> angle_between((1, 0, 0), (-1, 0, 0))
                3.141592653589793
        """
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        all_zeros_1 = not np.any(v1_u)
        all_zeros_2 = not np.any(v2_u)
        if all_zeros_1 and all_zeros_2 is True:
            return(0)
        else:
            return(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

    def avg_angs_vels(self):
        i = 0
        while i < len(self.x_vel):
            self.ang_bar.append(sum([180/np.pi*(self.angle_between(
                               [self.x_vel[i], self.y_vel[i], self.z_vel[i]],
                               [self.x_fluid_vel[i], self.y_fluid_vel[i],
                                self.z_fluid_vel[i]]))
                           for i in range(i, i+self.num_particles)]) /
                                          self.num_particles)

            self.x_vel_bar.append(sum([(self.x_vel[i]-self.x_fluid_vel[i])
                                  for i in range(i, i+self.num_particles)]) /
                                  self.num_particles)
            self.y_vel_bar.append(sum([(self.y_vel[i]-self.y_fluid_vel[i])
                                  for i in range(i, i+self.num_particles)]) /
                                  self.num_particles)
            self.z_vel_bar.append(sum([(self.z_vel[i]-self.z_fluid_vel[i])
                                  for i in range(i, i+self.num_particles)]) /
                                  self.num_particles)

            i += self.num_particles
        return()


folders = [name for name in os.listdir('data')]
num_folders = len(folders)


def get_stks_num(f_name):
    return(float(f_name.split('_')[-2] + '.' + f_name.split('_')[-1]))


folders.sort(key=get_stks_num)
stks_nums = [get_stks_num(folders[i]) for i in range(num_folders)]

time_data = []
u_data = []
v_data = []
w_data = []
u_fluid_data = []
v_fluid_data = []
w_fluid_data = []
ang_bar_data = []
mu = [10.4, 1.04, 0.104]

for i in range(num_folders):
    root = 'data//' + folders[i]
    tau = (2000*0.05**2)/(18*mu[i])
    f = data_processing(root, tau)
    f.sort_files()
    f.read_files()
    f.avg_angs_vels()
    time_data.append(f.time_nd)
    u_data.append(f.x_vel_bar)
    v_data.append(f.y_vel_bar)
    w_data.append(f.z_vel_bar)
    u_fluid_data.append(f.x_fluid_vel)
    v_fluid_data.append(f.y_fluid_vel)
    w_fluid_data.append(f.z_fluid_vel)
    ang_bar_data.append(f.ang_bar)

# Data plotting #
params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large'}
plt.rcParams.update(params)

f1 = plt.figure()
f1.subplots_adjust(hspace=0.4)
for i in range(num_folders):
    ax = f1.add_subplot(3, 1, i+1)
    ax.plot(time_data[i], u_data[i], 'ro', label='U')
    ax.plot(time_data[i], v_data[i], 'go', label='V')
    ax.plot(time_data[i], w_data[i], 'bo', label='W')
    ax.set_xlim(0)
    plt.xlabel(r't/$\tau$')
    plt.ylabel(r'$\bar{\dot{x}}_i$ ($m/s$)')
    plt.title('Mean Relative Particle Speeds for a Stokes Number of '
              + str(stks_nums[i]))
    plt.legend(loc='upper right')

f2 = plt.figure()
f2.subplots_adjust(hspace=0.4)
for i in range(num_folders):
    ax = f2.add_subplot(3, 1, i+1)
    ax.plot(time_data[i], ang_bar_data[i], 'ro', label=r'$\theta$')
    ax.set_xlim(0)
    plt.xlabel(r't/$\tau_d$')
    plt.ylabel(r'$\bar{\theta}$ ($\degree$)')
    plt.title('Mean Relative Angle Between Particles and Fluid for a ' +
              'Stokes Number of ' + str(stks_nums[i]))
    plt.legend(loc='upper right')

# Exports processed data to text files for plotting elsewhere #
processed_data_loc = 'processed_data//'

for i in range(num_folders):
    with open(processed_data_loc + 'tgv_rel_vel_stk_' +
              folders[i].split('_')[-2] + '_' + folders[i].split('_')[-1] +
              '_verification.txt', 'w') as f:
        time_data[i][::-1]
        f.write('time' + ' ' + 'x_vel_bar' + ' ' + 'y_vel_bar' + ' ' +
                'z_vel_bar' + ' ' + '\n')
        for j in range(len(time_data[i])):
            f.write(str(time_data[i][j]) + ' ' + str(u_fluid_data[i][j]) + ' '
                    + str(v_fluid_data[i][j]) + ' ' + str(w_fluid_data[i][j]) +
                    ' ' + '\n')
    time_data[::-1]

    with open(processed_data_loc + 'tgv_rel_theta_stk_' +
              folders[i].split('_')[-2] + '_' +
              folders[i].split('_')[-1] + '_verification.txt', 'w') as f:
        time_data[i][::-1]
        f.write('time' + ' ' + 'ang_bar' + ' ' + '\n')
        for j in range(len(time_data[i])):
            f.write(str(time_data[i][j]) + ' ' + str(ang_bar_data[i][j]) + ' '
                    + '\n')
    time_data[::-1]
