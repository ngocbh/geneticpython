import sys, os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../../../geneticpython'))

from geneticpython.individual import FloatIndividual
from geneticpython import Population, NSGAIIEngine
from geneticpython.operators import TournamentSelection,\
    SBXCrossover, \
    PolynomialMutation

import numpy as np
import matplotlib.pyplot as plt

class ZDT1Individual(FloatIndividual):

    def __init__(self, number_of_variables: int=30):
        self.number_of_variables = number_of_variables
        super(ZDT1Individual, self).__init__(number_of_variables, [0,1])


seed = 13
pop_size = 100
indv_temp = ZDT1Individual(30)
population = Population(indv_temp, pop_size)
selection = TournamentSelection(tournament_size=2)
crossover = SBXCrossover(pc=0.9, distribution_index=5)
mutation = PolynomialMutation(pm= 1.0 / 30, distribution_index=0.20)


engine = NSGAIIEngine(population,selection=selection,
                        crossover=crossover,
                        mutation=mutation,
                        selection_size=100,
                        max_iter=200,
                        random_state=1)

@engine.register_objective
def objective1(indv):
    solution = indv.chromosome
    return solution[0]

@engine.register_objective
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

engine.run()

pareto_front = engine.get_pareto_front()

def visualize_front(front, reference_front=None):
    fig = plt.figure()
    ax= fig.add_axes([0,0,1,1])

    f1 = [solution.objectives[0] for solution in front]
    f2 = [solution.objectives[1] for solution in front]    
 
    if reference_front is not None:
        ax.scatter(reference_front[:, 0], reference_front[:, 1], color='black')
    ax.scatter(f1, f2, color='r')
    
    ax.set_xlabel('f1')
    ax.set_ylabel('f2')
    ax.set_title('Front Plot')
    plt.show()

def read_reference_points(filepath: str):
    return np.loadtxt(filepath)

print(len(pareto_front))
visualize_front(pareto_front, read_reference_points(os.path.join(WORKING_DIR,'data/ZDT1.pf')))
