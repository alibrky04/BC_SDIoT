import random
import subprocess
import os
import re

class Controller:
    def __init__(self, COMMAND, glpk_folder_path, P_LOT = 5, W_CAR = 5, MAX_CAPACITY = 10):
        self.P_LOT = P_LOT
        self.W_CAR = W_CAR
        self.MAX_CAPACITY = MAX_CAPACITY
        self.COMMAND = COMMAND
        self.glpk_folder_path = glpk_folder_path

        self.parking_spaces = {f'p{i + 1}' : [0] * self.MAX_CAPACITY for i in range(self.P_LOT)}
        self.parking_spaces_loads = {f'p{i + 1}' : sum(self.parking_spaces[f'p{i + 1}']) for i in range(self.P_LOT)}
        self.number_of_cars = {f'p{i + 1}' : 0 for i in range(self.P_LOT)}
        self.waiting_cars = {f'Car{i + 1}': random.randint(1, 5) for i in range(self.W_CAR)}
    
    def createCars(self):
        cars = {f'Car{i + 1}': random.randint(1, 5) for i in range(self.W_CAR)}
        print('The cars in the queuing area')
        for i in range(self.W_CAR):
            print(f'Number of people in car {i + 1} is', cars[f'Car{i + 1}'])
        
        input('Solve?')

        return cars

    def createData(self):
        self.waiting_cars = self.createCars()

        data = f"""# Data section
data;

set ParkingSpaces := p1 p2 p3 p4 p5;
set WaitingCars := Car1 Car2 Car3 Car4 Car5;

param :
        initLoad :=
    p1      {self.parking_spaces_loads['p1']}
    p2      {self.parking_spaces_loads['p2']}
    p3      {self.parking_spaces_loads['p3']}
    p4      {self.parking_spaces_loads['p4']}
    p5      {self.parking_spaces_loads['p5']};

param :
        maxCarCapacity :=
    p1      {self.MAX_CAPACITY}
    p2      {self.MAX_CAPACITY}
    p3      {self.MAX_CAPACITY}
    p4      {self.MAX_CAPACITY}
    p5      {self.MAX_CAPACITY};

param :
        parked_car_num :=
    p1      {self.number_of_cars['p1']}
    p2      {self.number_of_cars['p2']}
    p3      {self.number_of_cars['p3']}
    p4      {self.number_of_cars['p4']}
    p5      {self.number_of_cars['p5']};

param :
        numPeopleInCar :=
    Car1        {self.waiting_cars['Car1']}
    Car2        {self.waiting_cars['Car2']}
    Car3        {self.waiting_cars['Car3']}
    Car4        {self.waiting_cars['Car4']}
    Car5        {self.waiting_cars['Car5']};"""
        
        return data

    def writeData(self):
        data = self.createData()
        with open('SPS/GLPK/SPS.dat', 'w') as file:
            file.write(data)
        
    def runSolver(self, doPrint = False):
        result = subprocess.run(self.COMMAND, shell=True, cwd=self.glpk_folder_path, capture_output=True, text=True)

        if doPrint:
            print("Output:", result.stdout)
            print("Error:", result.stderr)

    def takeOutput(self):
        try:
            with open(self.glpk_folder_path + "/SPS.out", 'r') as file:
                solver_output = file.read()
                
                car_assignments = {}
                parking_space_loads = {}

                car_assignments_pattern = re.compile(r'isCarAssigned\[(\w+),(\w+)\].val = (\d+)')
                parking_space_load_pattern = re.compile(r'parkingSpaceLoad\[(\w+)\].val = (\d+)')

                for line in solver_output.split('\n'):
                    if line.strip():
                        match = car_assignments_pattern.match(line)
                        if match:
                            car = match.group(1)
                            parking_space = match.group(2)
                            value = int(match.group(3))

                            if car not in car_assignments:
                                car_assignments[car] = {}

                            car_assignments[car][parking_space] = value
                        
                        load_match = parking_space_load_pattern.match(line)
                        if load_match:
                            parking_space = load_match.group(1)
                            load_value = int(load_match.group(2))

                            parking_space_loads[parking_space] = load_value

                assigned_parking_spaces = {}

                for car, spaces in car_assignments.items():
                    assigned_space = next((space for space, value in spaces.items() if value == 1), None)
                    assigned_parking_spaces[car] = assigned_space

                return assigned_parking_spaces, parking_space_loads
        except FileNotFoundError:
            print(f'The file "{self.glpk_folder_path}" does not exist.')
            return None
        
    def updateState(self):
        assigned_parking_spaces, parking_space_loads = self.takeOutput()

        for car, parking_space in assigned_parking_spaces.items():
            for i, lot in enumerate(self.parking_spaces[parking_space]):
                if lot == 0:
                    self.parking_spaces[parking_space][i] = 1
                    break

        for parking_space, value in parking_space_loads.items():
            if value is not None:
                self.parking_spaces_loads[parking_space] = value

        for car, parking_space in assigned_parking_spaces.items():
            if parking_space is not None:
                self.number_of_cars[parking_space] += 1
    
    def showData(self):
        for p, l in self.parking_spaces.items():
            print(f'{p} :', ''.join('#' if space == 1 else '' for space in l), f'({self.number_of_cars[p]})')

P_LOT = 5
W_CAR = 5
MAX_CAPACITY = 10
COMMAND = "glpsol --model SPS.mod --data SPS.dat --display SPS.out"
glpk_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GLPK'))

ct = True

controller = Controller(COMMAND, glpk_folder_path, P_LOT, W_CAR, MAX_CAPACITY)

while ct:
    controller.writeData()
    controller.runSolver()
    controller.updateState()
    controller.showData()
    input()