import time
import random
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

class Simulator:
    def __init__(self, StartTime = time.time()):
        self.StartTime = StartTime

    def GetUpTime(self):
        Uptime = time.time() - self.StartTime
        return int(Uptime)
    
    def SetTimeSlot(self):
        times = [[5, 15, 30, 60],[30, 60, 120, 180]]
        TimeSlot = random.randint(0, 3)
        return times[1][TimeSlot]

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
    
    def createPlots(self, plot_type):
        hours = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        half_hours = [2,4,6,8,10,12,14,16,18,20,22,24]
        p_lots = [3,4,5,6,7,8]

        max_gap = []
        max_cars = []
        max_people = []

        fig_type = ''

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
                    if line.startswith('fig2'):
                        fig_type = 'fig2'
                        if line.startswith('g:'):
                            max_gap.append(max([int(num) for num in line.split()[1:] if num.isdigit()]))
                        elif line.startswith('c:'):
                            max_cars.append(max([int(num) for num in line.split()[1:] if num.isdigit()]))
                        elif line.startswith('p:'):
                            max_people.append(max([int(num) for num in line.split()[1:] if num.isdigit()]))
                    elif line.startswith('fig3'):
                        fig_type = 'fig3'
                else:
                    fig, ax1 = plt.subplots()

                    if fig_type == 'fig1':
                        if plot_type == 't_g':
                            title = 'Figure 1.a'
                            x = hours
                            y1 = gap
                            y2 = cars

                            x_label = 'Hours'
                            y1_label = 'Gap'
                            y2_label = 'Cars'

                        elif plot_type == "t_p":
                            title = 'Figure 1.b'
                            x = hours
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

                        plt.xticks(half_hours)
                        ax1.set_xlabel(x_label)

                        lines = [line1, line2]
                        labels = [line.get_label() for line in lines]

                        plt.legend(lines, labels, loc='upper left')
                        
                        plt.show()
                    elif fig_type == 'fig2':
                        if plot_type == "t_g":
                            title = 'Figure 2.a'
                            x = hours
                            y1 = gap
                            y2 = cars

                            x_label = 'Hours'
                            y1_label = 'Gap'
                            y2_label = 'Cars'
                        elif plot_type == "t_p":
                            pass
                    elif fig_type == 'fig3':
                        if plot_type == "t_g":
                            pass
                        elif plot_type == "t_p":
                            pass
        
    def createAveragePlots(self, plot_type):
        hours = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        half_hours = [2,4,6,8,10,12,14,16,18,20,22,24]
        gap = []
        cars = []
        people = []
        gapError = [0] * 24
        data_num = 30

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

            averageGapErrors = [round(x / data_num) for x in gapError]

            if plot_type == 't_g':
                title = 'Figure 1.a'
                x = hours
                y1 = averages[0]
                y2 = averages[1]

                averageErrors = averageGapErrors

                x_label = 'Hours'
                y1_label = 'Gap'
                y2_label = 'Cars'

            elif plot_type == "t_p":
                title = 'Figure 1.b'
                x = hours
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

            plt.xticks(half_hours)
            ax1.set_xlabel(x_label)

            ax1.errorbar(x, y1, yerr=averageErrors, ecolor='red', capsize=5)

            lines = [line1, line2]
            labels = [line.get_label() for line in lines]

            plt.legend(lines, labels, loc='upper left')
                        
            plt.show()

    def __del__(self):
        pass