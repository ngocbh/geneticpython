import sys, os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../../../geneticpython'))

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

from geneticpython.individual import Solution, BinaryIndividual, Gene, Chromosome
from geneticpython import Population, GeneticEngine
from geneticpython.operators import RouletteWheelSelection, UniformCrossover, FlipBitMutation

class KnapsackProblem:
    def __init__(self, n, cap, items):
        self.n = n
        self.capacity = cap
        self.items = items

class KnapsackIndividual(BinaryIndividual):
    # override
    def decode(self):
        """
            convert chromosome sequence to solution
        """
        mask = [gene.value for gene in self.chromosome.genes]
        return mask

    # override
    def encode(self, solution):
        """
            return chromosome sequence
        """
        pass

def read_input():
    # read input
    n, k = (0,0)
    items = []

    with open(os.path.join(WORKING_DIR,'data/ks_200_0'),mode='r') as f:
        n, k = list(map(int,f.readline().split()))
        for i in range(n):
            line = f.readline()
            v, w = list(map(int, line.split()))
            items.append(Item(i,v,w))
    return n, k, items

n, k, items = read_input()
prob = KnapsackProblem(n,k,items)
seed = 24
pop_size = 100
indiv_temp = KnapsackIndividual(n)
population = Population(indiv_temp, pop_size)
selection = RouletteWheelSelection()
crossover = UniformCrossover(pc=0.8, pe=0.5)
mutation = FlipBitMutation(pm=0.1)
engine = GeneticEngine(population,selection=selection,crossover=crossover,mutation=mutation,max_iter=100)

@engine.register_fitness
def fitness(indv):
    global prob
    solution = indv.decode()
    svalue = 0
    sweight = 0
    for i in range(prob.n):
        if solution[i] == 1:
            svalue += prob.items[i].value
            sweight += prob.items[i].weight
    fitness = svalue 
    if sweight > prob.capacity:
        fitness += (prob.capacity - sweight)*10
        # fitness = 0
    return fitness

engine.create_seed(seed)
engine.run()
ans = engine.population.get_best_indv(engine.fitness)
print(ans)
# print(engine.population)


