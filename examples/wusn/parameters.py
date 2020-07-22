"""
File: parameters.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

import os

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

SEED = 42

POPULATION_SIZE = 10

SELECTION_SIZE = 10

MAX_ITER = 2

TOURNAMENT_SIZE = 5

CROSSOVER_PROB = 0.9

CROSSOVER_DISTRIBUTION_INDEX = 20

MUTATION_PROB = 1.0/30

MUTATION_DISTRIBUTION_INDEX = 5

ALPHA = 2

BETA = 6
