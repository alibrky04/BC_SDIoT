import os
from time import sleep
from Controller import Controller
from Simulator import Simulator

simulator = Simulator()

P_LOT = 5
MAX_CAPACITY = 20
W_CAR = simulator.normalDist(0)
COMMAND = "glpsol --model SPS.mod --data SPS.dat --display SPS.out"
glpk_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GLPK'))

ct = 0
counter = 0

controller = Controller(COMMAND, glpk_folder_path, P_LOT, W_CAR[0], MAX_CAPACITY)
controller.createData()

while ct < 18:
    print('***********************************************\n')

    controller.createCars(doChange=True, new_car_num=W_CAR[ct])
    controller.writeData()
    controller.runSolver()
    controller.updateState()
    controller.showData()

    while counter < 5:
        controller.removeCars()
        sleep(1)
        counter += 1

    counter = 0
    ct += 1
    print()