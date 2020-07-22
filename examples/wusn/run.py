"""
File: run.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

from __future__ import absolute_import

import single_hop_nsgaii
import multi_hop_nsgaii

import os
import joblib

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))


def run_single_hop_problem():
    datapath = os.path.join(WORKING_DIR, 'data/medium/single_hop')

    test_list = []
    for file in os.listdir(datapath):
        if 'dem' not in file:
            continue
        filepath = os.path.join(datapath, file)
        test_list.append(filepath)

    print(test_list)

    joblib.Parallel(n_jobs=-1)(joblib.delayed(single_hop_nsgaii.solve)
                               (file, visualization=True) for file in test_list)


def run_multi_hop_problem():
    datapath = os.path.join(WORKING_DIR, 'data/medium/multi_hop')

    test_list = []

    for file in os.listdir(datapath):
        if 'dem' not in file:
            continue
        filepath = os.path.join(datapath, file)
        test_list.append(filepath)

    print(test_list)

    joblib.Parallel(n_jobs=-1)(joblib.delayed(multi_hop_nsgaii.solve)(
        file, visualization=True) for file in test_list)


if __name__ == "__main__":
    # run_single_hop_problem()
    run_multi_hop_problem()
