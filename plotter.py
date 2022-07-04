#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import datetime
import os
from matplotlib import pyplot as plt
import pandas as pd


class Experiment:

    def __init__(self, path):
        self.Path = path
        self.list = path.split('_')
        self.method = self.list[0]
        self.length = self.list[1] 
        self.pop = self.list[2]
        self.ratio = self.list[3]
        self.timestamp = self.list[4].split('.')[0]
        self.dataframe = None
        self.time = None
        self.fitness = None
        self.iterations = None
        self.x = None

    def convert_time(self, t):
        try:
            b = datetime.datetime.strptime(t, "%H:%M:%S.%f")
            res = 3600 * b.hour + 60 * b.minute + b.second + 1e-6 * b.microsecond
        except:
            b = datetime.datetime.strptime(t, "%H:%M:%S")
            res = 3600 * b.hour + 60 * b.minute + b.second
        return res

    def data(self):
        self.dataframe = pd.read_csv(self.Path)
        self.time = self.dataframe.time.apply(lambda t: self.convert_time(t))
        self.fitness = self.dataframe.fitness
        self.x = self.dataframe.iteration
        # print(self.iterations)
        # self.x = np.linspace(0, int(self.iterations), int(self.iterations))


class Plotter:

    def __init__(self):
        self.paths = list(filter(lambda x: x.endswith('.csv'), os.listdir('./')))
        self.experiments = list(Experiment(el) for el in self.paths)
        self.experiments_to_plot = None
        

    def fitness_vs_time(self, length):
        self.experiments.sort(key=lambda x: x.length, reverse=False)
        self.experiments_to_plot = list(filter(lambda x: int(x.length) == length, self.experiments))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        ax1.axhline(y=length, color='g', linestyle='-', label='target')
        ax1.set(xlabel='time, [s]', ylabel='fitness')
        ax1.set_title("Fitness vs. Time")
        ax2.axhline(y=length, color='g', linestyle='-', label='target')
        ax2.set(xlabel='iterations', ylabel='fitness')
        ax2.set_title("Fitness vs. Iterations")
        colors = ['b', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown', 'pink', 'gray', 'cyan', 'olive', 'maroon']

        for exp in self.experiments_to_plot:
            labels = str(exp.Path).rsplit('_', 1)[0]
            color = colors[0]
            colors.remove(color)
            exp.data()
            ax1.plot(exp.time, exp.fitness, color=color, label=labels)
            ax2.plot(exp.x, exp.fitness, color=color, label=labels)

        ax1.legend(loc='best', shadow=True, fontsize=10)
        ax2.legend(loc='best', shadow=True, fontsize=10)
        name = 'Fitness_vs_time_'+str(length)+'.png'
        plt.savefig(name)
        plt.show()

