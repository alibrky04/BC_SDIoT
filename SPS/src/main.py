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
COMMAND2 = "glpsol --model SPS_CAR.mod --data SPS_CAR.dat --display SPS_CAR.out"
DATAFILE = 'SPS/GLPK/SPS_CAR.dat'
glpk_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GLPK'))

ct = 0
counter = 0
sim_count = 0
day = 1
deviation = 7

while True:
    while sim_count < MAX_SIM:
        distribution = simulator.generateDistribution(dMean=6, dDev=deviation, genType=3, distType=1, dLength=EPOCH)

        W_CAR = distribution

        controller = Controller(COMMAND2, glpk_folder_path, P_LOT, W_CAR[ct], MAX_CAPACITY)
        
        while ct < EPOCH:
            print('***********************************************\n')

            controller.createCars(doChange=True, new_car_num=W_CAR[ct])
            controller.writeData(DATAFILE, model=2)
            controller.runSolver()
            controller.updateState(model=2)
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

        controller.storeData(1, start_hour=EPOCH * (MAX_DAY - 1), sim_count=sim_count)

        print('Data is recorded.')
        print('Next simulation will start in 5 seconds.\n')

        ct = 0
        day = 1

        sleep(5)
        
        sim_count += 1
    
    with open('SPS/Datas/SimData.txt', 'a') as file:
        file.write(f'Deviation: {deviation}\nEND\n\n')

    deviation += 1
    sim_count = 0