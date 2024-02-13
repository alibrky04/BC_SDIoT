import os
from time import sleep
from Controller import Controller

P_LOT = 3
MAX_CAPACITY = 20
W_CAR = 5
COMMAND = "glpsol --model SPS.mod --data SPS.dat --display SPS.out"
glpk_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GLPK'))

ct = 0
counter = 0

controller = Controller(COMMAND, glpk_folder_path, P_LOT, W_CAR, MAX_CAPACITY)
controller.createData()

while ct < 5:
    print('***********************************************\n')

    controller.createCars()
    controller.writeData()
    controller.runSolver()
    controller.updateState()
    controller.showData()

    while counter < 10:
        controller.removeCars()
        sleep(1)
        counter += 1

    counter = 0
    ct += 1
    print()