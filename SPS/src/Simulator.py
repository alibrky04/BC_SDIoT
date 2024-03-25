import time
import random
import sys
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

class Simulator:
    def __init__(self, StartTime = time.time(), simulationDays = [1,1,1]):
        self.StartTime = StartTime
        self.simulationDays = simulationDays
        self.hours = [i for i in range(1, self.simulationDays[0] * 24 + 1)]
        self.week = [i for i in range(1, self.simulationDays[1] * 24 + 1)]
        self.month = [i for i in range(1, self.simulationDays[2] * 24 + 1)]
        self.half_hours = [i for i in range(1, self.simulationDays[0] * 24 + 1) if i % (self.simulationDays[0] * 2) == 0]
        self.p_lots = np.array([i for i in range(3, 9)]) # [3-8]
        self.week_days = [i * 24 for i in range(1,8)]
        self.month_weeks = [i * 180 for i in range(1,5)]
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
    
    def normalDist(self, mean = 12, dev = 4, length = 24):
        x = np.arange(1, length + 1)
        normalDist = np.ceil(norm.pdf(x, mean, dev) * 100)

        normalDist = [int(num) for num in normalDist]

        print(f"Distribution: Normal Distribution\nArrangement: {normalDist}")

        return normalDist
    
    def uniformDist(self, l_bound = 1, u_bound = 10, length = 24):
        uniformdDist = []
        for _ in range(length):
            uniformdDist.append(random.randint(l_bound, u_bound))

        print(f"Distribution: Uniform Distribution\nArrangement: {uniformdDist}")

        return uniformdDist

    def exponentialDist(self, start = 1, end = 12, length = 24):
        factor = (end / start) ** (1 / (length - 1))
        exponentialDist = [round(start * (factor ** i)) for i in range(length)]

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
                        x = self.hours
                        y1 = gap
                        y2 = cars

                        x_label = 'Hours'
                        y1_label = 'Gap'
                        y2_label = 'Cars'

                    elif plot_type == "t_p":
                        x = self.hours
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

                    plt.xticks(self.half_hours)
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
                x = self.p_lots
                y1 = gap
                y2 = cars

                x_label = 'Parking Lots'
                y1_label = 'Gap'
                y2_label = 'Cars'

            elif plot_type == "t_p_2":
                x = self.p_lots
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

            plt.xticks(self.p_lots)
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

            averages = [[round(sum(nums) / len(nums)) for nums in group] for group in transposed_lists]
            
            if plot_type == 't_g':
                x = self.hours
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
                x = self.hours
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

            plt.xticks(self.half_hours)
            ax1.set_xlabel(x_label)

            ax1.errorbar(x, y1, yerr=averageErrors, ecolor='black', capsize=5, linewidth=0.1)

            lines = [line1, line2]
            labels = [line.get_label() for line in lines]

            plt.legend(lines, labels, loc='upper left')
            ax1.grid(linewidth=0.25)
                        
            plt.show()
        
    def createTransactionPlots(self, distribution):
        epoch_size = 0
        day_total_size = []
        week_total_size = []
        month_total_size = []
        dayDistList = []
        weekDistList = []
        monthDistList = []
        x1_label = '1 Day'
        x2_label = '1 Week'
        x3_label = '1 Month'
        y_label = 'Ledger Size (MB)'

        if distribution == 'normal':
            for _ in range(self.simulationDays[0]):
                dayDistList.append(self.normalDist(dev=random.choice( [3, 3.25, 3.5, 3.75, 4] )))

            for _ in range(self.simulationDays[1]):
                weekDistList.append(self.normalDist(dev=random.choice( [3, 3.25, 3.5, 3.75, 4] )))

            for _ in range(self.simulationDays[2]):
                monthDistList.append(self.normalDist(dev=random.choice( [3, 3.25, 3.5, 3.75, 4] )))
        elif distribution == 'expo':
            for _ in range(self.simulationDays[0]):
                dayDistList.append(self.exponentialDist(start=random.choice( [1, 2, 3] ), end= random.choice( [10, 11, 12] )))

            for _ in range(self.simulationDays[1]):
                weekDistList.append(self.exponentialDist(start=random.choice( [1, 2, 3] ), end= random.choice( [10, 11, 12] )))

            for _ in range(self.simulationDays[2]):
                monthDistList.append(self.exponentialDist(start=random.choice( [1, 2, 3] ), end= random.choice( [10, 11, 12] )))

        for dist in dayDistList:
            for req in dist:
                epoch_size += req * self.reqSize + self.blockSize
                day_total_size.append(epoch_size)

        epoch_size = 0
        
        for dist in weekDistList:
            for req in dist:
                epoch_size += req * self.reqSize + self.blockSize
                week_total_size.append(epoch_size)
        
        epoch_size = 0
        
        for dist in monthDistList:
            for req in dist:
                epoch_size += req * self.reqSize + self.blockSize
                month_total_size.append(epoch_size)

        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        axs[0].plot(self.hours, day_total_size, marker='o', linestyle='-', color='blue', label=y_label)
        axs[0].set_xticks(self.half_hours)
        axs[0].set_xlabel(x1_label)
        axs[0].set_ylabel(y_label)

        axs[1].plot(self.week, week_total_size, marker='o', markevery = (0, 7), linestyle='-', color='red', label=y_label)
        axs[1].set_xticks(self.week_days)
        axs[1].set_xticklabels([f'Day {i}' for i in range(1, 8)])
        axs[1].set_xlabel(x2_label)
        axs[1].set_ylabel(y_label)

        axs[2].plot(self.month, month_total_size, marker='o', markevery = (0, 30), linestyle='-', color='green', label=y_label)
        axs[2].set_xticks(self.month_weeks)
        axs[2].set_xticklabels([f'Week {i}' for i in range(1, 5)])
        axs[2].set_xlabel(x3_label)
        axs[2].set_ylabel(y_label)

        for i in range(3):
            axs[i].legend()
            axs[i].grid()

        plt.show()

    def __del__(self):
        pass