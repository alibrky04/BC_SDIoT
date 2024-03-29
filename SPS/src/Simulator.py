import time
import random
import sys
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

class Simulator:
    def __init__(self, StartTime = time.time(), days = 1, weeks = 1, months = 1):
        self.StartTime = StartTime
        self.weeks = weeks
        self.months = months
        self.simDays = {'days' : days,
                        'weekDays' : self.weeks * 7,
                        'monthDays' : self.months * 30}
        
        self.xAxises = {'hours' : [i for i in range(1, self.simDays['days'] * 24 + 1)],
                        'weeks' : [i for i in range(1, self.simDays['weekDays'] * 24 + 1)],
                        'months' : [i for i in range(1, self.simDays['monthDays'] * 24 + 1)],
                        'pLots' : [i for i in range(3, 9)]}
        
        self.xAxisTicks = {'halfHours' : [i for i in range(1, self.simDays['days'] * 24 + 1) if i % (self.simDays['days'] * 2) == 0],
                            'pLots' : [i for i in range(3, 9)],
                            'weekDays' : [i * 24 for i in range(1, self.simDays['weekDays'] + 1)],
                            'monthWeeks' : [i * 180 for i in range(1, self.months * 4 + 1)]}
        self.data_num = 30
        self.reqSize = 0.29
        self.blockSize = 0.05

    def GetUpTime(self):
        Uptime = time.time() - self.StartTime
        return int(Uptime)
    
    def SetTimeSlot(self):
        return random.randint(30,180)

    def SetRemoveTime(self):
        RemoveTime = self.SetTimeSlot() + self.GetUpTime()
        return RemoveTime
    
    def normalDist(self, mean = 8, dev = 4, length = 24):
        """
        x = np.arange(1, length + 1)
        normalDist = np.ceil(norm.pdf(x, mean, dev) * 100)

        normalDist = [int(num) for num in normalDist]
        """

        normalDist = np.round(np.abs(np.random.normal(mean, dev, size=length)))

        normalDist = list(normalDist)

        normalDist = [int(num) for num in normalDist]

        for i in range(len(normalDist)):
            if normalDist[i] > 11:
                normalDist[i] = 11
            elif normalDist[i] == 0:
                normalDist[i] = 1

        print(f"Distribution: Normal Distribution\nArrangement: {normalDist}")

        return normalDist
    
    def uniformDist(self, l_bound = 1, u_bound = 10, length = 24):
        uniformdDist = []
        for _ in range(length):
            uniformdDist.append(random.randint(l_bound, u_bound))

        print(f"Distribution: Uniform Distribution\nArrangement: {uniformdDist}")

        return uniformdDist

    def exponentialDist(self, start = 1, end = 12, length = 24):
        """
        factor = (end / start) ** (1 / (length - 1))
        exponentialDist = [round(start * (factor ** i)) for i in range(length)]
        """
        
        exponentialDist = np.round(np.abs(np.random.exponential(size=length)))

        print(f"Distribution: Exponential Distribution\nArrangement: {exponentialDist}")

        return exponentialDist
    
    def createStandartPlots(self, plot_type):
        gap = []
        cars = []
        people = []

        with open('SPS/Datas/SimData.txt', 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                if not line.startswith('-'):
                    fig_type = 'fig1'
                    if line.startswith('g:'):
                        gap = [int(num) for num in line.split()[1:] if num.isdigit()]
                    elif line.startswith('c:'):
                        cars = [int(num) for num in line.split()[1:] if num.isdigit()]
                    elif line.startswith('p:'):
                        people = [int(num) for num in line.split()[1:] if num.isdigit()]
                else:
                    fig, ax1 = plt.subplots()

                    if plot_type == 't_g':
                        x = self.xAxises['hours']
                        y1 = gap
                        y2 = cars

                        x_label = 'Hours'
                        y1_label = 'Gap'
                        y2_label = 'Cars'

                    elif plot_type == "t_p":
                        x = self.xAxises['hours']
                        y1 = people
                        y2 = cars

                        x_label = 'Hours'
                        y1_label = 'People'
                        y2_label = 'Cars'

                    line1, = ax1.plot(x, y1, marker='o', linestyle='-', color='blue', label=y1_label)
                    ax1.set_ylabel(y1_label, color='blue')

                    ax2 = ax1.twinx()

                    line2, = ax2.plot(x, y2, marker='o', linestyle='-', color='red', label=y2_label)
                    ax2.set_ylabel(y2_label, color='red')

                    plt.xticks(self.xAxisTicks['halfHours'])
                    ax1.set_xlabel(x_label)

                    lines = [line1, line2]
                    labels = [line.get_label() for line in lines]

                    plt.legend(lines, labels, loc='upper left')
                    ax1.grid()
                    ax2.grid()
                        
                    plt.show()
    
    def createBarPlots(self, plot_type):
        gap = []
        cars = []
        people = []

        bar_width = 0.2

        with open('SPS/Datas/SimData.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                if line.startswith('g:'):
                    gap.append(max([int(num) for num in line.split()[1:] if num.isdigit()]))
                elif line.startswith('c:'):
                    cars.append(max([int(num) for num in line.split()[1:] if num.isdigit()]))
                elif line.startswith('p:'):
                    people.append(max([int(num) for num in line.split()[1:] if num.isdigit()]))

            if plot_type == 't_g_2':
                x = self.xAxises['pLots']
                y1 = gap
                y2 = cars

                x_label = 'Parking Lots'
                y1_label = 'Gap'
                y2_label = 'Cars'

            elif plot_type == "t_p_2":
                x = self.xAxises['pLots']
                y1 = people
                y2 = cars

                x_label = 'Parking Lots'
                y1_label = 'People'
                y2_label = 'Cars'

            fig, ax1 = plt.subplots()

            ax1.bar(x - bar_width/2, y1, bar_width, color='blue', alpha=0.7, label=y1_label)
            ax1.set_ylabel(y1_label, color='blue')

            ax2 = ax1.twinx()

            ax2.bar(x + bar_width, y2, bar_width, color='red', alpha=0.7, label=y2_label)
            ax2.set_ylabel(y2_label, color='red')

            plt.xticks(self.xAxisTicks['pLots'])
            ax1.set_xlabel(x_label)
                        
            plt.show()
        
    def createAveragePlots(self, plot_type):
        gap = []
        cars = []
        people = []
        gapError = [0] * 24
        peopleError = [0] * 24

        with open('SPS/Datas/SimData.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                if line.startswith('g:'):
                    gap.append([int(num) for num in line.split()[1:] if num.isdigit()])
                elif line.startswith('c:'):
                    cars.append([int(num) for num in line.split()[1:] if num.isdigit()])
                elif line.startswith('p:'):
                    people.append([int(num) for num in line.split()[1:] if num.isdigit()])
                
            transposed_lists = zip(*gap), zip(*cars), zip(*people)

            # gap, cars, people
            averages = [[round(sum(nums) / len(nums)) for nums in group] for group in transposed_lists]
            
            if plot_type == 't_g':
                x = self.xAxises['hours']
                y1 = averages[0]
                y2 = averages[1]

                for g in gap:
                    for i, gapNumber in enumerate(g):
                        gapError[i] += abs(gapNumber - averages[0][i])

                averageErrors = [round(x / self.data_num) for x in gapError]

                x_label = 'Hours'
                y1_label = 'Gap'
                y2_label = 'Cars'

            elif plot_type == "t_p":
                x = self.xAxises['hours']
                y1 = averages[2]
                y2 = averages[1]

                for p in people:
                    for i, peopleNumber in enumerate(p):
                        peopleError[i] += abs(peopleNumber - averages[1][i])

                averageErrors = [round(x / self.data_num) for x in peopleError]

                x_label = 'Hours'
                y1_label = 'People'
                y2_label = 'Cars'

            fig, ax1 = plt.subplots(figsize=(6,4), dpi=150)

            line1, = ax1.plot(x, y1, marker='o', linestyle='-', color='blue', label=y1_label)
            ax1.set_ylabel(y1_label, color='blue')

            ax2 = ax1.twinx()

            line2, = ax2.plot(x, y2, marker='o', linestyle='-', color='red', label=y2_label)
            ax2.set_ylabel(y2_label, color='red')

            plt.xticks(self.xAxisTicks['halfHours'])
            ax1.set_xlabel(x_label)

            ax1.errorbar(x, y1, yerr=averageErrors, ecolor='black', capsize=2.5, capthick=0.5, linewidth=0.15)

            lines = [line1, line2]
            labels = [line.get_label() for line in lines]

            plt.legend(lines, labels, loc='upper left')
            ax1.grid(linewidth=0.25)
                        
            plt.show()
        
    def createTransactionPlots(self, distribution):
        epoch_size = 0
        totalSizes = {'dayTotalSize' : [],
                      'weekTotalSize' : [],
                      'monthTotalSize' : []}
        
        distLists = {'dayDistList': [],
                     'weekDistList' : [],
                     'monthDistList' : []}
        
        xLabels = {'x1Label' : '1 Day',
                   'x2Label' : '1 Week',
                   'x3Label' : '1 Month'}
        
        y_label = 'Ledger Size (MB)'

        if distribution == 'normal':
            for d, dl in zip(self.simDays.values(), distLists.values()):
                for _ in range(d):
                    dl.append(self.normalDist(dev=random.choice( [3.75, 4] )))
        elif distribution == 'expo':
            for d, dl in zip(self.simDays.values(), distLists.values()):
                for _ in range(d):
                    dl.append(self.exponentialDist(start=random.choice( [1, 2, 3] ), end= random.choice( [10, 11] )))

        for dist, size in zip(distLists.values(), totalSizes.values()):
            for req in dist:
                for r in req:
                    epoch_size += r * self.reqSize + self.blockSize
                    size.append(epoch_size)
                
            epoch_size = 0

        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        axs[0].scatter(self.xAxises['hours'], totalSizes['dayTotalSize'], color='blue', s=20, label=y_label)
        axs[0].set_xticks(self.xAxisTicks['halfHours'])
        axs[0].set_xlabel(xLabels['x1Label'])
        axs[0].set_ylabel(y_label)

        axs[1].scatter(self.xAxises['weeks'], totalSizes['weekTotalSize'], color='red', s=5, label=y_label)
        axs[1].set_xticks(self.xAxisTicks['weekDays'])
        axs[1].set_xticklabels([f'Day {i}' for i in range(1, 8)])
        axs[1].set_xlabel(xLabels['x2Label'])
        axs[1].set_ylabel(y_label)

        axs[2].scatter(self.xAxises['months'], totalSizes['monthTotalSize'], color='green', s=5, label=y_label)
        axs[2].set_xticks(self.xAxisTicks['monthWeeks'])
        axs[2].set_xticklabels([f'Week {i}' for i in range(1, 5)])
        axs[2].set_xlabel(xLabels['x3Label'])
        axs[2].set_ylabel(y_label)

        for i in range(3):
            axs[i].legend()
            axs[i].grid(linewidth=0.25)

        plt.show()

    def __del__(self):
        pass