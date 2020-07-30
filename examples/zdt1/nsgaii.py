import os
import sys
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../../../geneticpython'))

import matplotlib.pyplot as plt
import numpy as np

from geneticpython.core.operators import TournamentSelection,\
    SBXCrossover, \
    PolynomialMutation
from geneticpython import Population, NSGAIIEngine
from geneticpython.core.individual import FloatIndividual
from geneticpython.utils.visualization import visualize_fronts, save_history_as_gif

class ZDT1Individual(FloatIndividual):

    def __init__(self, number_of_variables: int = 30):
        self.number_of_variables = number_of_variables
        super(ZDT1Individual, self).__init__(number_of_variables, [0, 1])


seed = 13
pop_size = 100
indv_temp = ZDT1Individual(30)
population = Population(indv_temp, pop_size)
selection = TournamentSelection(tournament_size=2)
crossover = SBXCrossover(pc=0.9, distribution_index=5)
mutation = PolynomialMutation(pm=1.0 / 30, distribution_index=0.20)


engine = NSGAIIEngine(population, selection=selection,
                      crossover=crossover,
                      mutation=mutation,
                      selection_size=100,
                      random_state=1)


@engine.minimize_objective
def objective1(indv):
    solution = indv.chromosome
    return solution[0]


@engine.minimize_objective
def objective2(indv):
    solution = indv.chromosome
    n = indv.number_of_variables

    def eval_g(solution, n):
        g = np.sum(solution) - solution[0]
        constant = 9.0 / (n - 1)
        return constant * g + 1.0

    def eval_h(f: float, g: float) -> float:
        return 1.0 - np.sqrt(f / g)

    g = eval_g(solution, n)
    h = eval_h(solution[0], g)
    return h * g


history = engine.run(generations=100)
# print(history.history)

pareto_front = engine.get_pareto_front()


def read_reference_points(filepath: str):
    return np.loadtxt(filepath)

referenced_points=read_reference_points(
    os.path.join(WORKING_DIR, 'data/ZDT1.pf'))

save_history_as_gif(history, referenced_points=referenced_points, gen_filter=lambda x : (x % 1 == 0))
print(len(pareto_front))
visualize_fronts({'nsgaii': pareto_front}, referenced_points=referenced_points)
