
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Filename: multi_hop_nsgaii.py
# Description:
# Created by ngocjr7 on [14-06-2020 21:22:52]
"""
from __future__ import absolute_import

import sys
import os

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../../../geneticpython'))

import time
import json
import random
import matplotlib.pyplot as plt
import numpy as np

from collections import defaultdict
from random import Random
from networks import WusnNetwork
from problems import MultiHopProblem
from utils import visualize_front, make_gif, visualize_solutions, remove_file, save_results
from utils import WusnInput
from parameters import *

from geneticpython.core.operators import TournamentSelection, SBXCrossover, PolynomialMutation
from geneticpython import Population
from geneticpython.core.individual import NetworkRandomKeys
from geneticpython.engines import NSGAIIEngine
from geneticpython.utils.visualization import save_history_as_gif, visualize_fronts


class MultiHopIndividual(NetworkRandomKeys):
    def __init__(self, problem: MultiHopProblem):
        self.problem = problem
        network = WusnNetwork(problem)
        super(MultiHopIndividual, self).__init__(
            problem._num_encoded_edges, network=network)


def solve(filename, output_dir='results/multi_hop', visualization=False):
    start_time = time.time()

    basename, _ = os.path.splitext(os.path.basename(filename))
    os.makedirs(os.path.join(
        WORKING_DIR, '{}/{}'.format(output_dir, basename)), exist_ok=True)
    print(basename)

    wusnfile = os.path.join(WORKING_DIR, filename)
    inp = WusnInput.from_file(wusnfile)
    problem = MultiHopProblem(inp)

    indv_temp = MultiHopIndividual(problem)

    def init_bias_genes(length, n_relays_edges, rand: Random = Random()):
        genes = np.zeros(length)
        for i in range(length):
            u = rand.betavariate(alpha=ALPHA, beta=BETA)
            if i < n_relays_edges:
                genes[i] = 1 - u
            else:
                genes[i] = u
        return genes

    # rand = random.Random()
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

    population = Population(indv_temp, MH_POP_SIZE)

    @population.register_initialization
    def init_population(rand: Random = Random()):
        print("Initializing population")
        ret = []
        for i in range(population.size):
            new_indv = population.individual_temp.clone()
            for j in range(1000):
                genes = init_bias_genes(
                    problem._num_encoded_edges, problem.num_rl2ss_edges, rand)
                new_indv.update_genes(genes=genes)
                network = new_indv.decode()
                if network.is_valid:
                    print("init sucessfullly indv number {} in {} loops".format(i, j))
                    break
            ret.append(new_indv)
        return ret

    selection = TournamentSelection(tournament_size=MH_TOURNAMENT_SIZE)
    crossover = SBXCrossover(
        pc=MH_CRO_PROB, distribution_index=MH_CRO_DI)
    mutation = PolynomialMutation(
        pm=MH_MUT_PROB, distribution_index=MH_MUT_DI)

    engine = NSGAIIEngine(population, selection=selection,
                          crossover=crossover,
                          mutation=mutation,
                          selection_size=MH_SLT_SIZE,
                          random_state=MH_SEED)

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

    history = engine.run(generations=MH_GENS)

    pareto_front = engine.get_pareto_front()
    solutions = engine.get_all_solutions()

    end_time = time.time()

    out_dir = os.path.join(WORKING_DIR,  f'{output_dir}/{basename}')

    with open(os.path.join(out_dir, 'time.txt'), mode='w') as f:
        f.write(f"running time: {end_time-start_time:}")

    save_results(pareto_front, solutions, best_mr,
                 out_dir, visualization=False)

    visualize_fronts({'nsgaii': pareto_front}, show=False, save=True,
                     title=f'pareto fronts {basename}',
                     filepath=os.path.join(out_dir, 'pareto_fronts.png'),
                     objective_name=['relays', 'energy consumption'])

    save_history_as_gif(history, 
                        title="NSGAII - multi-hop", 
                        objective_name=['relays', 'energy'], 
                        gen_filter=lambda x : (x % 5 == 0), 
                        out_dir=out_dir)

if __name__ == '__main__':
    solve('data/medium/multi_hop/uu-dem1_r25_1_40.json', visualization=True)
