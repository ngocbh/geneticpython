"""
File: parameters.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

import os
# "0.0.1" for run experimental arguments and "test" for testing
SH_MODEL = "test"
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

def load_sh_model(model):
    global SH_SEED, SH_POP_SIZE, SH_SLT_SIZE, SH_GENS
    global SH_TOURNAMENT_SIZE, SH_CRO_PROB, SH_CRO_DI, SH_MUT_DI, SH_MUT_PROB
    if model == 'test':                 
        SH_SEED = 42
        SH_POP_SIZE = 10
        SH_SLT_SIZE = 10
        SH_GENS = 2
        SH_TOURNAMENT_SIZE = 2
        SH_CRO_PROB = 0.9
        SH_CRO_DI = 5
        SH_MUT_PROB = 1.0/100
        SH_MUT_DI = 0.20
    elif model == '0.0.1':
        SH_SEED = 42
        SH_POP_SIZE = 300
        SH_SLT_SIZE = 100
        SH_GENS = 100
        SH_TOURNAMENT_SIZE = 2
        SH_CRO_PROB = 0.9
        SH_CRO_DI = 5
        SH_MUT_PROB = 1.0/100
        SH_MUT_DI = 0.20
    elif model == '0.0.2':
        SH_SEED = 42
        SH_POP_SIZE = 400
        SH_SLT_SIZE = 400
        SH_GENS = 400
        SH_TOURNAMENT_SIZE = 2
        SH_CRO_PROB = 0.9
        SH_CRO_DI = 5
        SH_MUT_PROB = 1.0/100
        SH_MUT_DI = 0.20

def load_mh_model(model):
    global MH_SEED, MH_POP_SIZE, MH_SLT_SIZE, MH_GENS
    global  MH_TOURNAMENT_SIZE, MH_CRO_PROB, MH_CRO_DI, MH_MUT_DI, MH_MUT_PROB
    if model == 'test':                 
        MH_SEED = 42
        MH_POP_SIZE = 10
        MH_SLT_SIZE = 10
        MH_GENS = 2
        MH_TOURNAMENT_SIZE = 2
        MH_CRO_PROB = 0.9
        MH_CRO_DI = 5
        MH_MUT_PROB = 1.0/100
        MH_MUT_DI = 0.20
    elif model == '0.0.1':
        mh_seed = 42
        mh_pop_size = 300
        mh_slt_size = 100
        mh_gens = 100
        mh_tournament_size = 2
        mh_cro_prob = 0.9
        mh_cro_di = 5
        mh_mut_prob = 1.0/100
        mh_mut_di = 0.20
    elif model == '0.0.2':
        mh_seed = 42
        mh_pop_size = 400
        mh_slt_size = 400
        mh_gens = 400
        mh_tournament_size = 2
        mh_cro_prob = 0.9
        mh_cro_di = 5
        mh_mut_prob = 1.0/100
        mh_mut_di = 0.20

load_sh_model(SH_MODEL)
load_mh_model(MH_MODEL)
