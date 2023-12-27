# Define sets
set ParkingSpaces;
set WaitingCars;

# Define parameters
param parkingSpaceLoad {i in ParkingSpaces};
param minLoad := min {i in ParkingSpaces} parkingSpaceLoad[i];
param numPeopleInCar {i in WaitingCars};
param maxCapacity {i in ParkingSpaces};
param parked_car_num {i in ParkingSpaces};

# Define binary decision variables
var isCarAssigned {i in WaitingCars, j in ParkingSpaces}, binary;

# Objective function: Minimize the sum of load gaps
minimize totalLoadGap: sum {i in WaitingCars, j in ParkingSpaces} isCarAssigned[i, j] * (parkingSpaceLoad[j] - minLoad);

# Constraints
subject to AssignmentConstraint {i in WaitingCars}:
    # Constraint 1: Each car is assigned to exactly one parking space
    sum {j in ParkingSpaces} isCarAssigned[i, j] = 1;

subject to CapacityConstraint {j in ParkingSpaces}:
    # Constraint 2: Capacity constraint - Sum of people in assigned cars to a space should not exceed the maximum capacity
    sum {i in WaitingCars} isCarAssigned[i, j] <= maxCapacity[j] - parked_car_num[j];

# Solve the optimization problem
solve;

# Display the results
display isCarAssigned;
display totalLoadGap;
display minLoad;
display parkingSpaceLoad;

# Data section (provide actual data values)
data;

set ParkingSpaces := p1 p2 p3 p4;
set WaitingCars := Car1 Car2 Car3 Car4 Car5;

param :
        parkingSpaceLoad :=
    p1          4
    p2          5
    p3          3
    p4          4;
param :
        numPeopleInCar :=
    Car1        1
    Car2        2
    Car3        3
    Car4        4
    Car5        5;
param :
        maxCapacity :=
    p1      10
    p2      10
    p3      10
    p4      10;

param :
        parked_car_num :=
    p1      3
    p2      2
    p3      1
    p4      4;

end;