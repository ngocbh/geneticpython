"""
File: visualization.py
Author: ngocjr7
Email: ngocjr7@gmail.com
Github: https://github.com/ngocjr7
Description:
"""

from __future__ import absolute_import

from typing import List, Union, Dict, Tuple
from ..callbacks import History
from ..core.population import Pareto
import matplotlib.pyplot as plt
import os
import glob
from PIL import Image
from _ctypes import PyObj_FromPtr
import re
import uuid
import numpy as np


def visualize_fronts(pareto_dict: Dict[str, Union[Pareto, List, Tuple]] = {},
                     filepath='./fronts.png',
                     title='pareto fronts',
                     objective_name: List[str] = ['obj1', 'obj2'],
                     save=False,
                     show=True,
                     referenced_points=None,
                     **kwargs):
    pareto_dict.update(kwargs)
    for name, pareto in pareto_dict.items():
        if not isinstance(pareto, Pareto) and (not isinstance(pareto, (list, tuple)) or
                                               not all(isinstance(solution, (list, tuple)) for solution in pareto) or
                                               not all(isinstance(value, (int, float)) for solution in pareto for value in solution)):
            raise ValueError(
                f'pareto value must be an instance of List[List[Union[int, float]]], \
                pareto {name} isnot')

        if isinstance(pareto, Pareto):
            pareto_dict[name] = pareto.all_objectives()

        for solution in pareto_dict[name]:
            if not len(solution) == 2:
                raise ValueError(
                    f"This method only supports two objectives,\
                    solution {solution} of pareto {name} has {len(solution)}")
        pareto_dict[name] = sorted(
            pareto_dict[name], key=lambda solution: tuple(solution))
    plt.figure()
    legends = []
    for name, pareto in pareto_dict.items():
        legends.append(name)
        obj1 = [solution[0] for solution in pareto]
        obj2 = [solution[1] for solution in pareto]
        plt.scatter(obj1, obj2)
        plt.plot(obj1, obj2)

    if referenced_points is not None:
        if isinstance(referenced_points, np.ndarray):
            if referenced_points.shape[1] != 2:
                raise ValueError(
                    'referenced_points must have shape like (number_of_points)*(numer_of_objectives) \
                    and save_history_as_gif method only supports two objective problems')
            plt.plot(referenced_points[:, 0],
                     referenced_points[:, 1], color='black')
        elif isinstance(referenced_points, (list, tuple)):
            if not all(isinstance(solution, (list, tuple)) for solution in referenced_points) or \
                    not all(isinstance(value, (int, float)) for solution in referenced_points for value in solution):
                raise ValueError(
                    f'referenced_points value must be an instance of List[List[Union[int, float]]]')
            f1_rp = [solution[0] for solution in referenced_points]
            f2_rp = [solution[0] for solution in referenced_points]
            plt.plot(f1_rp, f2_rp, color='black')

    plt.xlabel(objective_name[0])
    plt.ylabel(objective_name[1])
    plt.title(title)
    plt.legend(legends)
    if save:
        plt.savefig(filepath)

    if show:
        plt.show()

    plt.close('all')


def visualize_solutions(pareto, solutions,
                        filepath='./solutions.png',
                        title='Solutions',
                        objective_name: List[str] = ['obj1', 'obj2'],
                        show=True, save=False,
                        referenced_points=None,
                        xlim=None, ylim=None):
    plt.figure()
    pareto.sort(key=lambda solution: tuple(solution))
    obj1 = [solution[0] for solution in pareto]
    obj2 = [solution[1] for solution in pareto]
    plt.scatter(obj1, obj2, color='red', zorder=3)
    plt.plot(obj1, obj2, color='red', zorder=3)

    obj1 = [solution[0] for solution in solutions]
    obj2 = [solution[1] for solution in solutions]
    plt.scatter(obj1, obj2, color='blue', zorder=2)

    if referenced_points is not None:
        plt.plot(referenced_points[:, 0],
                 referenced_points[:, 1], color='black')

    if xlim is not None:
        plt.xlim(xlim[0], xlim[1])
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])

    plt.xlabel(objective_name[0])
    plt.ylabel(objective_name[1])
    plt.title(title)
    if save:
        plt.savefig(filepath)

    if show:
        plt.show()

    plt.close('all')


def __make_gif(fileexp, filename):
    # Create the frames
    frames = []
    imgs = glob.glob(fileexp)
    imgs = sorted(imgs)
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save(filename, format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=200, loop=0)


def __remove_file(fileexp):
    # Get a list of all the file paths that ends with .txt from in specified directory
    fileList = glob.glob(fileexp)

    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)


def plot_single_objective_history(history_dict: Dict[str, Union[History, List[Union[int, float]]]] = {},
                                  filepath='./history.png',
                                  title='history',
                                  objective_name='objective',
                                  save=False,
                                  show=True,
                                  **kwargs):
    history_dict.update(kwargs)
    for name, history in history_dict.items():
        if isinstance(history, History):
            if not all('best_objective' in data for data in history.history):
                raise ValueError('plot_single_objective_history only supports single objective history.\
                                 The best_objective logs is required')
            history_dict[name] = [logs['best_objective']
                                  for logs in history.history]
    plt.figure()
    legends = []
    for name, history in history_dict.items():
        legends.append(name)
        gen = [i for i in range(len(history))]
        plt.plot(gen, history)

    plt.xlabel('generation')
    plt.ylabel(objective_name)
    plt.title(title)
    plt.legend(legends)
    if save:
        plt.savefig(filepath)

    if show:
        plt.show()

    plt.close('all')


def save_history_as_gif(history: History,
                        title='solutions',
                        referenced_points=None,
                        objective_name: List[str] = ['obj1', 'obj2'],
                        gen_filter=lambda x: True,
                        out_dir='./'):
    for data in history.history:
        if 'pareto_front' not in data or 'solutions' not in data:
            raise ValueError('save_history_as_gif only supports multiobjective history.\
                             it requires pareto_front and solutions logs in each generation')
        if not all(len(solution) == 2 for solution in data['pareto_front'] + data['solutions']):
            raise ValueError(
                'save_history_as_gif only supports two objective problems')

    xmin = float('inf')
    xmax = -float('inf')
    ymin = float('inf')
    ymax = -float('inf')
    for gen, data in enumerate(history.history):
        xmin = min( [xmin] + 
            [solution[0] for solution in (data['pareto_front'] + data['solutions']) if solution[0] != -float('inf')])
        xmax = max( [xmax] +
            [solution[0] for solution in (data['pareto_front'] + data['solutions']) if solution[0] != float('inf')])
        ymin = min( [ymin] +
            [solution[1] for solution in (data['pareto_front'] + data['solutions']) if solution[1] != -float('inf')])
        ymax = max( [ymax] +
            [solution[1] for solution in (data['pareto_front'] + data['solutions']) if solution[1] != float('inf')])

    if referenced_points is not None:
        if isinstance(referenced_points, np.ndarray):
            xmin = min(xmin, min(referenced_points[:, 0]))
            xmax = max(xmax, max(referenced_points[:, 0]))
            ymin = min(ymin, min(referenced_points[:, 1]))
            ymax = max(ymax, max(referenced_points[:, 1]))
        elif isinstance(referenced_points, (list, tuple)) and \
                all(isinstance(solution) for solution in referenced_points):
            xmin = min(xmin, min(
                [solution[0] for solution in referenced_points]))
            xmax = max(xmax, max(
                [solution[0] for solution in referenced_points]))
            ymin = min(ymin, min(
                [solution[1] for solution in referenced_points]))
            ymax = min(ymax, max(
                [solution[1] for solution in referenced_points]))
        else:
            raise ValueError("Unknow referenced_points")
    
    xmin, xmax, ymin, ymax = xmin * 0.95, xmax * 1.05, ymin * 0.95, ymax * 1.05 
    xlim = [xmin, xmax] if abs(xmin) != float('inf') and abs(xmax) != float('inf') else None
    ylim = [ymin, ymax] if abs(ymin) != float('inf') and abs(ymax) != float('inf') else None
    
    for gen, data in enumerate(history.history):
        if gen_filter(gen):
            gen_str = (3 - len(str(gen))) * '0' + str(gen)
            gen_title = title + ' ' + str(gen)
            filepath = os.path.join(out_dir, f'{title}-gen-{gen_str}.png')
            visualize_solutions(data['pareto_front'], data['solutions'], title=gen_title, save=True,
                                show=False, filepath=filepath, objective_name=objective_name,
                                referenced_points=referenced_points, xlim=xlim, ylim=ylim)
    gifexp = os.path.join(out_dir, f'{title}-gen-*.png')
    gifname = os.path.join(out_dir, f'{title}.gif')
    __make_gif(gifexp, gifname)
    __remove_file(gifexp)
