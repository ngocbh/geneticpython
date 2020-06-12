#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
*  Filename : main.py
*  Description : 
*  Created by ngocjr7 on [2020-06-06 20:46]	
"""
from __future__ import absolute_import

import sys, os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../../../geneticpython'))

from geneticpython.engine import NSGAIIEngine
from geneticpython.individual import NetworkRandomKeys
from geneticpython import Population
from geneticpython.operators import TournamentSelection, SBXCrossover, PolynomialMutation

from utils import WusnInput
from problems import SingleHopProblem
from networks import SingleHopNetwork

import numpy as np
import matplotlib.pyplot as plt
import random

class SingleHopIndividual(NetworkRandomKeys):
    def __init__(self, problem : SingleHopProblem):
        self.problem = problem
        network = SingleHopNetwork(problem)
        super(SingleHopIndividual, self).__init__(problem._num_encoded_edges, network=network)
        
        
def visualize_front(front, filename):
    plt.figure()
    # ax= fig.add_axes([0,0,1,1])

    f1 = [solution.objectives[0] for solution in front]
    f2 = [solution.objectives[1] for solution in front]    

    plt.scatter(f1, f2, color='r')
    
    plt.xlabel('f1')
    plt.ylabel('f2')
    plt.title('Front Plot')
    # plt.imshow()
    plt.savefig(os.path.join(WORKING_DIR, filename))
    plt.show()

best_mr = [float('inf')] * 80

def solve(filename):
    wusnfile = os.path.join(WORKING_DIR, filename)
    inp = WusnInput.from_file(wusnfile)
    problem = SingleHopProblem(inp)

    seed = 42
    pop_size = 1000
    indv_temp = SingleHopIndividual(problem)
    # rand = random.Random(seed)
    # indv_temp.init(rand=rand)
    # network = indv_temp.decode()
    # print(network.num_used_relays)
    # print(network.calc_max_energy_consumption())
    # return
    population = Population(indv_temp, pop_size)
    selection = TournamentSelection(tournament_size=2)
    crossover = SBXCrossover(pc=0.9, distribution_index=0.20)
    mutation = PolynomialMutation(pm= 1.0 / 30, distribution_index=0.20)

    engine = NSGAIIEngine(population,selection=selection,
                            crossover=crossover,
                            mutation=mutation,
                            selection_size=100,
                            max_iter=1,
                            random_state=1)


    
    @engine.register_objective
    def objective1(indv):
        network = indv.decode()
        if network.is_valid:
            return network.num_used_relays
        else:
            return float('inf')

    @engine.register_objective
    def objective2(indv):
        global best_mr
        network = indv.decode()
        if network.is_valid:
            mec = network.calc_max_energy_consumption()
            best_mr[int(network.num_used_relays)] = min(mec, best_mr[int(network.num_used_relays)])
            return mec
        else:
            return float('inf')

    engine.run()

    pareto_front = engine.get_pareto_front()
    print(len(pareto_front))
    with open(os.path.join(WORKING_DIR, 'results/pareto-front2.txt'), mode='w') as f:
        f.write(str(pareto_front))

    visualize_front(pareto_front, 'results/pareto-front2.png')

    solutions = engine.get_all_solutions()
    print(len(solutions))
    global best_mr
    print(best_mr)
    with open(os.path.join(WORKING_DIR, 'results/solutions2.txt'), mode='w') as f:
        for solution in solutions:
            f.write(str(solution.objectives) + '\n')
    visualize_front(solutions, 'results/solutions2.png')






if __name__ == '__main__':
    solve('data/single_hop/ga-dem10_r25_1.json')
    



