#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
*  Filename : main.py
*  Description :
*  Created by ngocjr7 on [2020-06-06 20:46]
"""
from __future__ import absolute_import

import sys
import os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../../../geneticpython'))

import time
import random
import matplotlib.pyplot as plt
import numpy as np

from collections import defaultdict
from networks import WusnNetwork
from problems import SingleHopProblem
from utils import WusnInput, visualize_front, make_gif, visualize_solutions, remove_file, save_results
from parameters import *

from geneticpython.core.operators import TournamentSelection, SBXCrossover, PolynomialMutation
from geneticpython import Population
from geneticpython.core.individual import NetworkRandomKeys
from geneticpython.engines import NSGAIIEngine
from geneticpython.utils.visualization import save_history_as_gif

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
    population = Population(indv_temp, SH_POP_SIZE)
    selection = TournamentSelection(tournament_size=SH_TOURNAMENT_SIZE)
    crossover = SBXCrossover(
        pc=SH_CRO_PROB, distribution_index=SH_CRO_DI)
    mutation = PolynomialMutation(
        pm=SH_MUT_PROB, distribution_index=SH_MUT_DI)

    engine = NSGAIIEngine(population, selection=selection,
                          crossover=crossover,
                          mutation=mutation,
                          selection_size=SH_SLT_SIZE,
                          random_state=SH_SEED)

    @engine.minimize_objective
    def objective1(indv):
        network = indv.decode()
        if network.is_valid:
            return network.num_used_relays
        else:
            return float('inf')

    best_mr = defaultdict(lambda: float('inf'))

    @engine.minimize_objective
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

    history = engine.run(generations=SH_GENS)

    pareto_front = engine.get_pareto_front()
    solutions = engine.get_all_solutions()

    out_dir = os.path.join(WORKING_DIR,  f'results/single_hop/{basename}')
    end_time = time.time()

    with open(os.path.join(out_dir, 'time.txt'), mode='w') as f:
        f.write(f"running time : {end_time - start_time:}")

    save_results(pareto_front, solutions, best_mr,
                 out_dir, visualization=False)
    
    save_history_as_gif(history, 
                        title="NSGAII", 
                        objective_name=['relays', 'energy'], 
                        gen_filter=lambda x : (x % 1 == 0), 
                        out_dir=out_dir)


if __name__ == '__main__':
    solve('data/medium/single_hop/ga-dem1_r25_1.json', visualization=True)
