# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import numpy as np


class data_processing():
    def __init__(self, root):
        self.root = root
        self.tau = (997*0.05**2)/(18*0.1)
        self.g = 9.81
        self.v = 0
        self.time = []
        self.time_nd = []
        self.x_pos = []
        self.y_pos = []
        self.z_pos = []
        self.x_vel = []
        self.y_vel = []
        self.z_vel = []
        self.u_analytic_nd = []
        self.u_error = []
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
            else:
                pass

    def analytic_solution(self):
        for i in range(len(self.time)):
            self.u_analytic_nd.append((self.tau * (self.g+self.v/self.tau) *
                                      (1-np.exp(-self.time[i]/self.tau))) /
                                      (self.tau*self.g))
        return(self.u_analytic_nd)

    def numerical_solution(self):
        self.y_vel_nd = [i/(-self.g*self.tau) for i in self.y_vel]
        return(self.y_vel_nd)

    def error(self):
        for i in range(len(self.time)):
            self.u_error.append(np.sqrt((self.u_analytic_nd[i] -
                                         self.y_vel_nd[i])**2))
            self.u_avg_error = (sum(self.u_error)/len(self.time))*100
        return(self.u_avg_error)


folders = [name for name in os.listdir('data')]
num_folders = len(folders)
timestep_sizes = [float(folders[i].split('_')[-3] + '.' +
                        folders[i].split('_')[-2]) for i in range(num_folders)]

time_data = []
u_analytic_data = []
u_numeric_data = []
error_data = []

for i in range(num_folders):
    root = 'data//' + folders[i]
    f = data_processing(root)
    f.sort_files()
    f.read_files()
    time_data.append(f.time_nd)
    u_analytic_data.append(f.analytic_solution())
    u_numeric_data.append(f.numerical_solution())
    error_data.append(f.error())

# Data plotting #
params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large'}
plt.rcParams.update(params)

f1 = plt.figure()
ax1 = f1.add_subplot(111)
ax1.plot(time_data[0], u_analytic_data[0], 'k-', label='Analytic U')
for i in range(1, len(u_numeric_data)):
    ax1.plot(time_data[i], u_numeric_data[i], '--',
             label=r'U for $\Delta t =$' + str(timestep_sizes[i]))
plt.xlim(0)
plt.ylim(0)
plt.xlabel(r'$t/\tau_d$')
plt.ylabel(r'$u/u_{terminal}$')
plt.title('Non-dimensionalised Particle Velocity for '
          'Particle Falling Under Gravity')
plt.legend(loc='lower right')

f2 = plt.figure()
ax2 = f2.add_subplot(111)
ax2.plot(timestep_sizes, error_data, '--', label='Error data')
plt.xlim(0, int(np.ceil(np.max(timestep_sizes))))
plt.ylim(0)
plt.xlabel(r'$\Delta t/\tau$')
plt.ylabel(r'Average Percentange Error')
plt.title('Average Percentage Error for Different Sized Timesteps')
plt.legend(loc='lower right')

# Exports processed data to text files for plotting elsewhere #
processed_data_loc = 'processed_data//'

# Analytic line #
with open(processed_data_loc + 'gravity_drag_0_001_tau_nd.txt', 'w') as f:
    time_data[0][::-1]
    f.write('time_nd' + ' ' + 'an_y_vel_nd' + '\n')
    for i in range(len(time_data[0])):
        f.write(str(time_data[0][i]) + ' ' + str(u_analytic_data[0][i]) + '\n')
time_data[0][::-1]

# Numeric lines #
for i in range(num_folders):
    with open(processed_data_loc + folders[i] + '_nd.txt', 'w') as f:
        time_data[i][::-1]
        f.write('time_nd' + ' ' + 'num_y_vel_nd' + '\n')
        for j in range(len(time_data[i])):
            f.write(str(time_data[i][j]) + ' ' +
                    str(u_numeric_data[i][j]) + '\n')
    time_data[i][::-1]

# Error line #
with open(processed_data_loc + 'error_data_for_gravity_drag.txt', 'w') as f:
    timestep_sizes[::-1]
    f.write('timestep' + ' ' + 'error' + '\n')
    for i in range(len(timestep_sizes)):
        f.write(str(timestep_sizes[i]) + ' ' + str(error_data[i]) + '\n')
timestep_sizes[::-1]
