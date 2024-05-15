# Sets
set WaitingCars;  # Set of waiting cars
set ParkingLots;  # Set of parking lots

# Parameters
param maxCarCapacity{ParkingLots};  # Maximum capacity of parking lot j
param initNumOfCar{ParkingLots};  # Current number of cars in parking lot j

# Variables
var x{WaitingCars, ParkingLots}, binary; # 1 if car i is assigned to parking lot j, 0 otherwise
var numOfCar{ParkingLots} >= 0; # Number of cars in parking lot j after assignments
var minNumOfCar >= 0; # Minimum number of cars in any parking lot after assignments

# Objective: Minimize the total differences of the amount of cars in each parking lot from the lowest amount of cars in any parking lot
minimize Total_of_Differences:
    sum{j in ParkingLots} (numOfCar[j] - minNumOfCar);

# Constraints

# Every car must be assigned to exactly one parking lot
s.t. Assign_Car{i in WaitingCars}:
    sum{j in ParkingLots} x[i, j] = 1;

# The number of cars assigned to each parking lot must not exceed its capacity
s.t. Capacity{j in ParkingLots}:
    initNumOfCar[j] + sum{i in WaitingCars} x[i, j] <= maxCarCapacity[j];

# Define y[j] as the total number of cars in parking lot j after assignments
s.t. Define_y{j in ParkingLots}:
    numOfCar[j] = initNumOfCar[j] + sum{i in WaitingCars} x[i, j];

# Ensure z is the minimum number of cars in any parking lot after assignments
s.t. Min_z{j in ParkingLots}:
    minNumOfCar <= numOfCar[j];

# Solve the problem
solve;

# Display results
display x; 
display numOfCar;
display minNumOfCar;
display Total_of_Differences;

end;