import time
import random
import numpy as np
from scipy.stats import norm, expon, uniform
import matplotlib.pyplot as plt

class Simulator:
    def __init__(self, StartTime = time.time()):
        self.StartTime = StartTime

    def GetUpTime(self):
        Uptime = time.time() - self.StartTime
        return int(Uptime)
    
    def SetTimeSlot(self):
        times = [5, 15, 30, 60]
        TimeSlot = random.randint(0, 3)
        return times[TimeSlot]

    def SetRemoveTime(self):
        RemoveTime = self.SetTimeSlot() + self.GetUpTime()
        return RemoveTime
    
    def normalDist(self, id, mean = 10, dev = 3):
        if id == 0:
            time = 18
            x = np.arange(1, time + 1)
            num_cars = np.ceil(norm.pdf(x, mean, dev) * 100)

            num_cars = [int(num) for num in num_cars]

            print(num_cars)

            plt.bar(x, num_cars, color='blue')
            plt.xlabel('Time')
            plt.ylabel('Cars')
            plt.title('Number of Cars')
            plt.grid(True)
            plt.show()

            return num_cars
        
        elif id == 1:
            time = 18
            x = np.arange(1, time + 1)
            num_people = np.ceil(norm.pdf(x, mean, dev) * 100)

            num_people = [int(num) for num in num_people]

            print(num_people)

            plt.bar(x, num_people, color='blue')
            plt.xlabel('Time')
            plt.ylabel('People')
            plt.title('Number of People')
            plt.grid(True)
            plt.show()

            return num_people

        return 0
    
    def uniformDist(self, id):
        pass

    def exponentialDist(self, id):
        pass