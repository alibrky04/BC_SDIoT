import os
import random
from time import sleep
from Controller import Controller
from Simulator import Simulator

simulator = Simulator()

EPOCH = 24
WAIT_TIME = 10
MAX_SIM = 30
MAX_DAY = 2
P_LOT = 5
MAX_CAPACITY = 25
COMMAND = "glpsol --model SPS.mod --data SPS.dat --display SPS.out"
glpk_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GLPK'))

ct = 0
counter = 0
sim_count = 0
day = 1

while sim_count < MAX_SIM:
    dSlice1 = simulator.exponentialDist(start=2, end=6, length=8)
    dSlice2 = simulator.exponentialDist(start=4, end=12, length=8)
    dSlice3 = simulator.exponentialDist(start=2, end=6, length=8)
    fullDay = dSlice1 + dSlice2 + dSlice3

    # distribution = simulator.exponentialDist(start=2, end=random.choice([10, 11]))

    distribution = fullDay

    W_CAR = distribution

    controller = Controller(COMMAND, glpk_folder_path, P_LOT, W_CAR[ct], MAX_CAPACITY)
    
    while ct < EPOCH:
        print('***********************************************\n')

        controller.createCars(doChange=True, new_car_num=W_CAR[ct])
        controller.writeData()
        controller.runSolver()
        controller.updateState()
        controller.showData()

        while counter < WAIT_TIME:
            controller.removeCars()
            sleep(1)
            counter += 1

        counter = 0
        ct += 1

        if ct == day * EPOCH and day < MAX_DAY:
            ct = 0
            day += 1
        
        print()

    print(f'Simulation {sim_count + 1} has ended.')

    controller.storeData(1, start_hour=EPOCH * (MAX_DAY - 1))

    print('Data is recorded.')
    print('Next simulation will start in 5 seconds.\n')

    ct = 0
    day = 1

    sleep(5)
    
    sim_count += 1