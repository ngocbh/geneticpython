#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
*  Filename : main.py
*  Description :
*  Created by ngocjr7 on [2020-06-06 20:46]
"""
from __future__ import absolute_import
import time
import random
import matplotlib.pyplot as plt
import numpy as np

from collections import defaultdict
from networks import WusnNetwork
from problems import SingleHopProblem
from utils import WusnInput, visualize_front, make_gif, visualize_solutions, remove_file, save_results
from parameters import *

from geneticpython.operators import TournamentSelection, SBXCrossover, PolynomialMutation
from geneticpython import Population
from geneticpython.individual import NetworkRandomKeys
from geneticpython.engines import NSGAIIEngine

import sys
import os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../../../geneticpython'))


class SingleHopIndividual(NetworkRandomKeys):
    def __init__(self, problem: SingleHopProblem):
        self.problem = problem
        network = WusnNetwork(problem)
        super(SingleHopIndividual, self).__init__(
            problem._num_encoded_edges, network=network)


def solve(filename, visualization=False):
    start_time = time.time()

    basename, _ = os.path.splitext(os.path.basename(filename))
    os.makedirs(os.path.join(
        WORKING_DIR, 'results/single_hop/{}'.format(basename)), exist_ok=True)
    print(basename)

    wusnfile = os.path.join(WORKING_DIR, filename)
    inp = WusnInput.from_file(wusnfile)
    problem = SingleHopProblem(inp)

    indv_temp = SingleHopIndividual(problem)
    # rand = random.Random(seed)
    # indv_temp.init(rand=rand)
    # network = indv_temp.decode()
    # print(network.num_used_relays)
    # print(network.calc_max_energy_consumption())
    # return
    population = Population(indv_temp, POPULATION_SIZE)
    selection = TournamentSelection(tournament_size=TOURNAMENT_SIZE)
    crossover = SBXCrossover(
        pc=CROSSOVER_PROB, distribution_index=CROSSOVER_DISTRIBUTION_INDEX)
    mutation = PolynomialMutation(
        pm=MUTATION_PROB, distribution_index=MUTATION_DISTRIBUTION_INDEX)

    engine = NSGAIIEngine(population, selection=selection,
                          crossover=crossover,
                          mutation=mutation,
                          selection_size=SELECTION_SIZE,
                          max_iter=MAX_ITER,
                          random_state=SEED)

    @engine.register_objective
    def objective1(indv):
        network = indv.decode()
        if network.is_valid:
            return network.num_used_relays
        else:
            return float('inf')

    best_mr = defaultdict(lambda: float('inf'))

    @engine.register_objective
    def objective2(indv):
        nonlocal best_mr
        network = indv.decode()
        if network.is_valid:
            mec = network.calc_max_energy_consumption()
            best_mr[int(network.num_used_relays)] = min(
                mec, best_mr[int(network.num_used_relays)])
            return mec
        else:
            return float('inf')

    f1_max = None
    f2_max = None
    if visualization:
        @engine.register_reporter
        def report(gen):
            if gen % 5 == 0 or gen < 20:
                nonlocal f1_max, f2_max
                solutions = engine.get_all_solutions()
                # print(solutions)
                f1_arr = [solution.objectives[0]
                          for solution in solutions if solution.objectives[0] != float('inf')]
                f2_arr = [solution.objectives[1]
                          for solution in solutions if solution.objectives[1] != float('inf')]

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
                                    'results/single_hop/{}/solutions-gen-{}.png'.format(
                                        basename, (3 - len(str(gen))) * '0' + str(gen)),
                                    title='solutions-gen-{}'.format(
                                        (3 - len(str(gen))) * '0' + str(gen)),
                                    show=False, f1_max=f1_max_temp, f2_max=f2_max_temp)

    engine.run()

    pareto_front = engine.get_pareto_front()
    solutions = engine.get_all_solutions()

    out_dir = os.path.join(WORKING_DIR,  f'results/single_hop/{basename}')
    end_time = time.time()

    with open(os.path.join(out_dir, 'time.txt'), mode='w') as f:
        f.write(f"running time : {end_time - start_time:}")

    save_results(pareto_front, solutions, best_mr,
                 out_dir, visualization=visualization)


if __name__ == '__main__':
    solve('data/medium/single_hop/ga-dem1_r25_1.json', visualization=True)
