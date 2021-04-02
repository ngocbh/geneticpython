from geneticpython.core.operators import RouletteWheelSelection, UniformCrossover, FlipBitMutation, RouletteWheelReplacement
from geneticpython import Population, GAEngine
from geneticpython.models import BinaryIndividual
from geneticpython.tools.visualization import plot_single_objective_history
from collections import namedtuple
import sys
import os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))


Item = namedtuple("Item", ['index', 'value', 'weight'])


class KnapsackProblem:
    def __init__(self, n, cap, items):
        self.n = n
        self.capacity = cap
        self.items = items


def read_input():
    # read input
    n, k = (0, 0)
    items = []

    with open(os.path.join(WORKING_DIR, 'data/ks_100_0'), mode='r') as f:
        n, k = list(map(int, f.readline().split()))
        for i in range(n):
            line = f.readline()
            v, w = list(map(int, line.split()))
            items.append(Item(i, v, w))
    return n, k, items


n, k, items = read_input()
prob = KnapsackProblem(n, k, items)
seed = 26
pop_size = 1000
indv_temp = BinaryIndividual(n)
population = Population(indv_temp, pop_size)
selection = RouletteWheelSelection()
crossover = UniformCrossover(pc=0.8, pe=0.5)
mutation = FlipBitMutation(pm=0.1)
replacement = RouletteWheelReplacement()

engine = GAEngine(population, selection=selection,
                  selection_size=100,
                  crossover=crossover,
                  mutation=mutation,
                  replacement=replacement)


@engine.maximize_objective
def fitness(indv):
    global prob
    solution = indv.chromosome
    svalue = 0
    sweight = 0
    for i in range(prob.n):
        if solution[i] == 1:
            svalue += prob.items[i].value
            sweight += prob.items[i].weight
    fitness = svalue
    if sweight > prob.capacity:
        fitness += (prob.capacity - sweight)*100000000
        # fitness = 0
    return fitness


# engine.create_seed(seed)
history = engine.run(generations=1000)
ans = engine.get_best_indv()
print(ans)
# print(engine.population)
plot_single_objective_history({'geneticpython': history})

