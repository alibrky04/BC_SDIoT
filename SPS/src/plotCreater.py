from Simulator import Simulator

s = Simulator(days=1, weeks=1, months=1)

weight_pairs = [(i / 10, 1 - (i / 10)) for i in range(1, 10)]
lot_capacities = [25, 25, 25, 25, 25]

# s.createStandartPlots('t_g')

# s.createAveragePlots('t_g')

# s.createBarPlots('t_p_2')

# s.createTransactionPlots('normal', distType=1)

# s.createNormalDistPlots('mu')

# s.createComparisonPlots(comparisonType='car-near')

s.createFairnessPlots(weight_pairs, lot_capacities)

# s.createFairnessWeightsPlot(weight_pairs, lot_capacities)