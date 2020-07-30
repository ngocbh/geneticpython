"""
File: parameters.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

import os

SH_MODEL = "0.0.1"
MH_MODEL = "test"

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

SH_SEED = 42
SH_POP_SIZE = 10
SH_SLT_SIZE = 10
SH_GENS = 2
SH_TOURNAMENT_SIZE = 5
SH_CRO_PROB = 0.9
SH_CRO_DI = 20
SH_MUT_PROB = 1.0/30
SH_MUT_DI = 5

MH_SEED = 42
MH_POP_SIZE = 10
MH_SLT_SIZE = 10
MH_GENS = 2
MH_TOURNAMENT_SIZE = 5
MH_X_PROB = 0.9
MH_CRO_DI = 20
MH_MUT_PROB = 1.0/30
MH_MUT_DI = 5
ALPHA = 2
BETA = 6

def __load_sh_model(model):
    global SH_SEED, SH_POP_SIZE, SH_SLT_SIZE, SH_GENS
    global SH_TOURNAMENT_SIZE, SH_CRO_PROB, SH_CRO_DI, SH_MUT_DI, SH_MUT_PROB
    if model == 'test':                 
        SH_SEED = 42
        SH_POP_SIZE = 10
        SH_SLT_SIZE = 10
        SH_GENS = 2
        SH_TOURNAMENT_SIZE = 5
        SH_CRO_PROB = 0.9
        SH_CRO_DI = 20
        SH_MUT_PROB = 1.0/30
        SH_MUT_DI = 5
    elif model == '0.0.1':
        SH_SEED = 42
        SH_POP_SIZE = 100
        SH_SLT_SIZE = 100
        SH_GENS = 100
        SH_TOURNAMENT_SIZE = 5
        SH_CRO_PROB = 0.9
        SH_CRO_DI = 20
        SH_MUT_PROB = 1.0/30
        SH_MUT_DI = 5

def __load_mh_model(model):
    global MH_SEED, MH_POP_SIZE, MH_SLT_SIZE, MH_GENS
    global  MH_TOURNAMENT_SIZE, MH_CRO_PROB, MH_CRO_DI, MH_MUT_DI, MH_MUT_PROB
    if model == 'test':                 
        MH_SEED = 42
        MH_POP_SIZE = 10
        MH_SLT_SIZE = 10
        MH_GENS = 2
        MH_TOURNAMENT_SIZE = 5
        MH_CRO_PROB = 0.9
        MH_CRO_DI = 20
        MH_MUT_PROB = 1.0/30
        MH_MUT_DI = 5
    elif model == '0.0.1':
        MH_SEED = 42
        MH_POP_SIZE = 100
        MH_SLT_SIZE = 100
        MH_GENS = 100
        MH_TOURNAMENT_SIZE = 5
        MH_CRO_PROB = 0.9
        MH_CRO_DI = 20
        MH_MUT_PROB = 1.0/30
        MH_MUT_DI = 5

__load_sh_model(SH_MODEL)
__load_mh_model(MH_MODEL)
