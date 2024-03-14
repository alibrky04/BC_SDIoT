import time
import random
import sys
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

class Simulator:
    def __init__(self, StartTime = time.time(), simulationDays = 1):
        self.StartTime = StartTime
        self.simulationDays = simulationDays
        self.hours = [i for i in range(1, self.simulationDays * 24 + 1)]
        self.half_hours = [i for i in range(1, self.simulationDays * 24 + 1) if i % (self.simulationDays * 2) == 0]
        self.p_lots = np.array([i for i in range(3, 9)]) # [3-8]
        self.data_num = 30
        self.reqSize = 300

    def GetUpTime(self):
        Uptime = time.time() - self.StartTime
        return int(Uptime)
    
    def SetTimeSlot(self):
        times = [[5, 15, 30, 60],[30, 60, 120, 180]]
        return random.choice(times[1])

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
                        title = 'Figure 1.a'
                        x = self.hours
                        y1 = gap
                        y2 = cars

                        x_label = 'Hours'
                        y1_label = 'Gap'
                        y2_label = 'Cars'

                    elif plot_type == "t_p":
                        title = 'Figure 1.b'
                        x = self.hours
                        y1 = people
                        y2 = cars

                        x_label = 'Hours'
                        y1_label = 'People'
                        y2_label = 'Cars'

                    plt.title(title)

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
                title = 'Figure 2.a'
                x = self.p_lots
                y1 = gap
                y2 = cars

                x_label = 'Parking Lots'
                y1_label = 'Gap'
                y2_label = 'Cars'

            elif plot_type == "t_p_2":
                title = 'Figure 2.b'
                x = self.p_lots
                y1 = people
                y2 = cars

                x_label = 'Parking Lots'
                y1_label = 'People'
                y2_label = 'Cars'

            fig, ax1 = plt.subplots()

            plt.title(title)

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

            for g in gap:
                for i, gapNumber in enumerate(g):
                    gapError[i] += abs(gapNumber - averages[0][i])

            averageGapErrors = [round(x / self.data_num) for x in gapError]

            if plot_type == 't_g':
                title = 'Figure 1.a'
                x = self.hours
                y1 = averages[0]
                y2 = averages[1]

                averageErrors = averageGapErrors

                x_label = 'Hours'
                y1_label = 'Gap'
                y2_label = 'Cars'

            elif plot_type == "t_p":
                title = 'Figure 1.b'
                x = self.hours
                y1 = averages[2]
                y2 = averages[1]

                x_label = 'Hours'
                y1_label = 'People'
                y2_label = 'Cars'

            fig, ax1 = plt.subplots()

            plt.title(title)

            line1, = ax1.plot(x, y1, marker='o', linestyle='-', color='blue', label=y1_label)
            ax1.set_ylabel(y1_label, color='blue')

            ax2 = ax1.twinx()

            line2, = ax2.plot(x, y2, marker='o', linestyle='-', color='red', label=y2_label)
            ax2.set_ylabel(y2_label, color='red')

            plt.xticks(self.half_hours)
            ax1.set_xlabel(x_label)

            ax1.errorbar(x, y1, yerr=averageErrors, ecolor='red', capsize=5)

            lines = [line1, line2]
            labels = [line.get_label() for line in lines]

            plt.legend(lines, labels, loc='upper left')
                        
            plt.show()
        
    def createTransactionPlots(self, distribution, title):
        epoch_size = 0
        total_size = []
        distList = []
        x_label = 'Hours'
        y_label = 'Ledger Size (Byte)'

        for _ in range(self.simulationDays):
            distList.append(distribution)

        for dist in distList:
            for req in dist:
                epoch_size += req * self.reqSize
                total_size.append(epoch_size)
        
        plt.title(title)
        
        plt.plot(self.hours, total_size, marker='o', linestyle='-', color='blue', label=y_label)

        plt.xticks(self.half_hours)

        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.show()

    def __del__(self):
        pass