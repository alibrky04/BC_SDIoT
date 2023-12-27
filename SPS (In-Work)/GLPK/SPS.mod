# Define sets
set Parking_Spaces;
set Parked_Cars;
set Queue_Cars;

# Define parameters
param parking_space_load {i in Parking_Spaces};
param minimum_load := min {i in Parking_Spaces} parking_space_load[i];

param num_of_people_parked {i in Parked_Cars};
param p_slot_parked {i in Parked_Cars};
param p_space_parked {i in Parked_Cars};

param num_of_people_queue {i in Queue_Cars};

# Define variables
var is_parked {i in Queue_Cars}, binary;

# Objective function
minimize g: sum {i in Parking_Spaces} parking_space_load[i] - minimum_load;

# Constraints


# solve;


# Display the results


# Enter the Data
# data;


# Example data


# End the Program
# end;