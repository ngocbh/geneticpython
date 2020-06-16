
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Filename: multi_hop_nsgaii.py
# Description:
# Created by ngocjr7 on [14-06-2020 21:22:52]
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
from utils import visualize_front, make_gif, visualize_solutions, remove_file
from problems import MultiHopProblem
from networks import WusnNetwork
from random import Random

import numpy as np
import matplotlib.pyplot as plt
import random

class MultiHopIndividual(NetworkRandomKeys):
    def __init__(self, problem : MultiHopProblem):
        self.problem = problem
        network = WusnNetwork(problem)
        super(MultiHopIndividual, self).__init__(problem._num_encoded_edges, network=network)
        

f1_max = None
f2_max = None
best_mr = [float('inf')] * 80

def solve(filename):
    basename, _ = os.path.splitext(os.path.basename(filename))
    os.makedirs(os.path.join(WORKING_DIR, 'results/multi_hop/{}'.format(basename)), exist_ok=True)
    print(basename)

    wusnfile = os.path.join(WORKING_DIR, filename)
    inp = WusnInput.from_file(wusnfile)
    problem = MultiHopProblem(inp)

    seed = 42
    pop_size = 100
    indv_temp = MultiHopIndividual(problem)

    def init_bias_genes(length, n_relays_edges, rand : Random = Random()):
        genes = np.zeros(length)
        for i in range(length):
            u = rand.betavariate(alpha=2, beta=6)
            if i < n_relays_edges:
                genes[i] = 1 - u
            else:
                genes[i] = u
        return genes
    
    rand = random.Random()
    # for i in range(10000):
    #     genes = init_bias_genes(problem._num_encoded_edges, problem.num_rl2ss_edges, rand)
    #     print(len(genes), problem._num_encoded_edges, problem.num_rl2ss_edges)
    #     indv_temp.update_genes(genes)
    #     network = indv_temp.decode()
    #     print(network.num_used_relays, network.max_depth)
    #     print(network.calc_max_energy_consumption())
    #     print(i, network.is_valid)
    #     if network.is_valid:
    #         break
    # return
    population = Population(indv_temp, pop_size)

    @population.register_initialization
    def init_population(rand : Random = Random()):
        print("Initializing population")
        ret = []
        for i in range(population.size):
            new_indv = population.individual_temp.clone()
            for j in range(1000):
                genes = init_bias_genes(problem._num_encoded_edges, problem.num_rl2ss_edges, rand)
                new_indv.update_genes(genes=genes)
                network = new_indv.decode()
                if network.is_valid:
                    print("init sucessfullly indv number {} in {} loops".format(i,j))
                    break
            ret.append(new_indv)
        return ret


    selection = TournamentSelection(tournament_size=5)
    crossover = SBXCrossover(pc=0.9, distribution_index=20)
    mutation = PolynomialMutation(pm= 0.01, distribution_index=5)

    engine = NSGAIIEngine(population,selection=selection,
                            crossover=crossover,
                            mutation=mutation,
                            selection_size=100,
                            max_iter=400,
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
        if gen % 5 == 0 or gen < 20:   
            global f1_max, f2_max
            solutions = engine.get_all_solutions()
            # print(solutions)
            f1_arr = [solution.objectives[0] for solution in solutions if solution.objectives[0] != float('inf')]
            f2_arr = [solution.objectives[1] for solution in solutions if solution.objectives[1] != float('inf')]

            if f1_max:
                f1_arr.append(f1_max)
            if f2_max:
                f2_arr.append(f2_max)
            if len(f1_arr) > 0:
                f1_max = max(f1_arr)
                f1_max_temp = f1_max * 1.05
            else:
                f1_max_temp = None
            if len(f2_arr) > 0:
                f2_max = max(f2_arr)
                f2_max_temp = f2_max * 1.05
            else:
                f2_max_temp = None

            visualize_solutions(solutions, 
                'results/multi_hop/{}/solutions-gen-{}.png'.format(basename, (3 - len(str(gen))) * '0' + str(gen)), 
                title='solutions-gen-{}'.format((3 - len(str(gen))) * '0' + str(gen)), 
                show=False, f1_max=f1_max_temp, f2_max=f2_max_temp)

    engine.run()

    pareto_front = engine.get_pareto_front()
    # save results
    with open(os.path.join(WORKING_DIR, 'results/multi_hop/{}/pareto-front.txt'.format(basename)), mode='w') as f:
        f.write(str(pareto_front))

    visualize_front(pareto_front, 'results/multi_hop/{}/pareto-front.png'.format(basename),
        title='pareto-front', show=False)

    global best_mr
    # for i, value in enumerate(best_mr):
    #         print(str(i) + " " + str(value) + "\n")
    print(best_mr)

    with open(os.path.join(WORKING_DIR, 'results/multi_hop/{}/best-mr.txt'.format(basename)), mode='w') as f:
        for i, value in enumerate(best_mr):
            f.write(str(i) + " " + str(value) + "\n")

    solutions = engine.get_all_solutions()
    with open(os.path.join(WORKING_DIR, 'results/multi_hop/{}/solutions.txt'.format(basename)), mode='w') as f:
        for solution in solutions:
            f.write(str(solution.objectives) + '\n')
    visualize_solutions(solutions, 'results/multi_hop/{}/solutions.png'.format(basename),
        title='solution-front', show=False)

    gifexp = os.path.join(WORKING_DIR, 'results/multi_hop/{}/solutions-gen-*.png'.format(basename))
    gifname = os.path.join(WORKING_DIR, 'results/multi_hop/{}/solutions.gif'.format(basename))
    make_gif(gifexp, gifname)
    remove_file(gifexp)

if __name__ == '__main__':
    solve('data/multi_hop/uu-dem1_r25_1_40.json')

    



