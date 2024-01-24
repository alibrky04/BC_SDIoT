# Define sets
set ParkingSpaces; # Parking spaces in the parking area
set WaitingCars; # Cars which wait to be assigned to a parking space

# Define parameters
param numPeopleInCar {i in WaitingCars}; # Number of people in a waiting car
param maxCarCapacity {i in ParkingSpaces}; # Maximum capacity of cars a parking space can hold
param parked_car_num {i in ParkingSpaces}; # Number of cars that parked in a parking space !!!!! THIS SHOULD BE A VARIABLE !!!!!
param initLoad {i in ParkingSpaces}; # Initial load of the parking spaces

# Define variables
var isCarAssigned {i in WaitingCars, j in ParkingSpaces}, binary; # if vehicle i is assigned in parking space j
var parkingSpaceLoad {i in ParkingSpaces}; # Number of people in a parking space
var minLoad; # Minimum load of all of the parking spaces

# Objective function: Minimize the sum of load gap between a load and the minimum load
minimize totalLoadGap: sum {j in ParkingSpaces} (parkingSpaceLoad[j] - minLoad + initLoad[j]);

# Constraints
subject to AssignmentConstraint {i in WaitingCars}:
    # Constraint 1: Each car is assigned to exactly one parking space
    sum {j in ParkingSpaces} isCarAssigned[i, j] = 1;

subject to CapacityConstraint {j in ParkingSpaces}:
    # Constraint 2: Capacity constraint - Sum of people in assigned cars to a space should not exceed the maximum capacity
    sum {i in WaitingCars} isCarAssigned[i, j] <= maxCarCapacity[j] - parked_car_num[j];

subject to minLoadConstraint {j in ParkingSpaces}:
    # Constraint 3: Defines the minLoad
    sum {i in WaitingCars} (numPeopleInCar[i] * isCarAssigned[i, j]) + initLoad[j] >= minLoad;

subject to loadConstraint1 {j in ParkingSpaces}:
    parkingSpaceLoad[j] >= sum {i in WaitingCars} (isCarAssigned[i, j] * numPeopleInCar[i]) + initLoad[j];

subject to loadConstraint2 {j in ParkingSpaces}:
    parkingSpaceLoad[j] <= sum {i in WaitingCars} (isCarAssigned[i, j] * numPeopleInCar[i]) + initLoad[j];

# Solve the optimization problem
solve;

# Display the results
display isCarAssigned;
display totalLoadGap;
display minLoad;
display parkingSpaceLoad;

end;