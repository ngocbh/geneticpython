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

from utils import WusnInput, visualize_front, make_gif, visualize_solutions, remove_file
from problems import SingleHopProblem
from networks import WusnNetwork

import numpy as np
import matplotlib.pyplot as plt
import random

class SingleHopIndividual(NetworkRandomKeys):
    def __init__(self, problem : SingleHopProblem):
        self.problem = problem
        network = WusnNetwork(problem)
        super(SingleHopIndividual, self).__init__(problem._num_encoded_edges, network=network)

f1_max = None
f2_max = None
best_mr = [float('inf')] * 80

def solve(filename):
    basename, _ = os.path.splitext(os.path.basename(filename))
    os.makedirs(os.path.join(WORKING_DIR, 'results/single_hop/{}'.format(basename)), exist_ok=True)
    print(basename)

    wusnfile = os.path.join(WORKING_DIR, filename)
    inp = WusnInput.from_file(wusnfile)
    problem = SingleHopProblem(inp)

    seed = 42
    pop_size = 100
    indv_temp = SingleHopIndividual(problem)
    # rand = random.Random(seed)
    # indv_temp.init(rand=rand)
    # network = indv_temp.decode()
    # print(network.num_used_relays)
    # print(network.calc_max_energy_consumption())
    # return
    population = Population(indv_temp, pop_size)
    selection = TournamentSelection(tournament_size=2)
    crossover = SBXCrossover(pc=0.9, distribution_index=20)
    mutation = PolynomialMutation(pm= 1.0 / 30, distribution_index=5)

    engine = NSGAIIEngine(population,selection=selection,
                            crossover=crossover,
                            mutation=mutation,
                            selection_size=100,
                            max_iter=100,
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

    @engine.register_reporter
    def report(gen):
        if gen % 1 == 0:
            global f1_max, f2_max
            solutions = engine.get_all_solutions()
            f1_arr = [solution.objectives[0] for solution in solutions if solution.objectives[0] != float('inf')]
            f2_arr = [solution.objectives[1] for solution in solutions if solution.objectives[1] != float('inf')]

            if f1_max:
                f1_arr.append(f1_max)
            if f2_max:
                f2_arr.append(f2_max)
                
            f1_max = max(f1_arr)
            f2_max = max(f2_arr)

            solutions = engine.get_all_solutions()
            visualize_solutions(solutions, 
                'results/single_hop/{}/solutions-gen-{}.png'.format(basename, (3 - len(str(gen))) * '0' + str(gen)), 
                title='solutions-gen-{}'.format((3 - len(str(gen))) * '0' + str(gen)), 
                show=False, f1_max=f1_max*1.05, f2_max=f2_max*1.05)

    engine.run()

    pareto_front = engine.get_pareto_front()
    # save results
    with open(os.path.join(WORKING_DIR, 'results/single_hop/{}/pareto-front.txt'.format(basename)), mode='w') as f:
        f.write(str(pareto_front))

    visualize_front(pareto_front, 'results/single_hop/{}/pareto-front.png'.format(basename),
        title='final-pareto-front', show=False)

    
    global best_mr
    print(best_mr)

    with open(os.path.join(WORKING_DIR, 'results/single_hop/{}/best-mr.txt'.format(basename)), mode='w') as f:
        for i, value in enumerate(best_mr):
            f.write(str(i) + " " + str(value) + "\n")

    solutions = engine.get_all_solutions()
    with open(os.path.join(WORKING_DIR, 'results/single_hop/{}/solutions.txt'.format(basename)), mode='w') as f:
        for solution in solutions:
            f.write(str(solution.objectives) + '\n')
    visualize_solutions(solutions, 'results/single_hop/{}/solutions.png'.format(basename),
        title='final-solution', show=False)

    gifexp = os.path.join(WORKING_DIR, 'results/single_hop/{}/solutions-gen-*.png'.format(basename))
    gifname = os.path.join(WORKING_DIR, 'results/single_hop/{}/solutions.gif'.format(basename))
    make_gif(gifexp, gifname)
    remove_file(gifexp)

if __name__ == '__main__':
    solve('data/single_hop/ga-dem1_r50_1.json')

    



