import os
from time import sleep
from Controller import Controller
from Simulator import Simulator

simulator = Simulator()

EPOCH = 24
WAIT_TIME = 10
MAX_SIM = 20
MAX_DAY = 2
P_LOT = 5
MAX_CAPACITY = 25
COMMAND1 = "glpsol --model SPS.mod --data SPS.dat --display SPS.out"
COMMAND2 = "glpsol --model SPS_CAR.mod --data SPS_CAR.dat --display SPS.out"
glpk_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GLPK'))

ct = 0
counter = 0
sim_count = 0
day = 1

while sim_count < MAX_SIM:
    distribution = simulator.generateDistribution(genType=4, distType=1, dLength=EPOCH)

    W_CAR = distribution

    controller = Controller(COMMAND1, glpk_folder_path, P_LOT, W_CAR[ct], MAX_CAPACITY)
    
    while ct < EPOCH:
        print('***********************************************\n')

        controller.createCars(doChange=True, new_car_num=W_CAR[ct])
        controller.writeData('SPS/GLPK/SPS.dat')
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