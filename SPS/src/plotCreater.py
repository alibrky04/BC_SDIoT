import numpy as np
from Simulator import Simulator

s = Simulator(days=1, weeks=1, months=1)

epsilon = 1e-6
weight_pairs = [(w, 1 - w) for w in np.linspace(epsilon, 1 - epsilon, 100)]
lot_capacities = [25, 25, 25, 25, 25]

# s.createStandartPlots('t_g')

# s.createAveragePlots('t_g')

# s.createBarPlots('t_p_2')

# s.createTransactionPlots('normal', distType=1)

# s.createNormalDistPlots('mu')

# s.createComparisonPlots(comparisonType='car-near')

s.createFairnessPlots(weight_pairs, lot_capacities)

#s.createFairnessPlotsForDifMetrics(weight_pairs, lot_capacities)

# s.createFairnessWeightsPlot(weight_pairs, lot_capacities)