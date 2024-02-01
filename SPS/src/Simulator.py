import time
import random

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