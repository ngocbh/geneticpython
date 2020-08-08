"""
File: run.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description: 
"""

from __future__ import absolute_import

from parameters import *

import single_hop_nsgaii
import multi_hop_nsgaii

import os
import joblib

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))


def run_single_hop_problem(model, input_dir, output_dir):
    print(f"Running single hop problem on model {model}")
    load_sh_model(model)
    datapath = os.path.join(WORKING_DIR, input_dir)

    test_list = []
    for file in os.listdir(datapath):
        if 'dem' not in file:
            continue
        filepath = os.path.join(datapath, file)
        test_list.append(filepath)

    print(test_list)

    joblib.Parallel(n_jobs=-1)(joblib.delayed(single_hop_nsgaii.solve)
                               (file, output_dir=output_dir, visualization=True) for file in test_list)


def run_multi_hop_problem(model, input_dir, output_dir):
    print(f"Running multi-hop problem on model {model}")
    load_mh_model(model)
    datapath = os.path.join(WORKING_DIR, input_dir)

    test_list = []

    for file in os.listdir(datapath):
        if 'dem' not in file:
            continue
        filepath = os.path.join(datapath, file)
        test_list.append(filepath)

    print(test_list)

    joblib.Parallel(n_jobs=-1)(joblib.delayed(multi_hop_nsgaii.solve)(
        file, output_dir=output_dir, visualization=True) for file in test_list)


if __name__ == "__main__":
    print("Running Test Model...")
    run_single_hop_problem("test", 'data/medium/single_hop', 'results/medium/single_hop')
    run_multi_hop_problem("test", 'data/medium/multi_hop', 'results/medium/multi_hop')
    print("Running 0.0.1 model")
    run_single_hop_problem('0.0.1', 'data/medium/single_hop', 'results/medium/single_hop')
    run_multi_hop_problem('0.0.1', 'data/medium/multi_hop', 'results/medium/multi_hop')
    print("Running 0.0.2 model")
    run_single_hop_problem('0.0.2', 'data/medium/single_hop', 'results/medium/single_hop')
    run_multi_hop_problem('0.0.2', 'data/medium/multi_hop', 'results/medium/multi_hop')
    print("Running small data")
    run_single_hop_problem("0.0.1",'data/small/single_hop', 'results/small/single_hop')
