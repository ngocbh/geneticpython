import matplotlib.pyplot as plt
import os
from PIL import Image
import glob
import json
from _ctypes import PyObj_FromPtr
import json
import re
import uuid

class NoIndent(object):
    def __init__(self, value):
        self.value = value

class NoIndentEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(NoIndentEncoder, self).__init__(*args, **kwargs)
        self.kwargs = dict(kwargs)
        del self.kwargs['indent']
        self._replacement_map = {}

    def default(self, o):
        if isinstance(o, NoIndent):
            key = uuid.uuid4().hex
            self._replacement_map[key] = json.dumps(o.value, **self.kwargs)
            return "@@%s@@" % (key,)
        else:
            return super(NoIndentEncoder, self).default(o)

    def encode(self, o):
        result = super(NoIndentEncoder, self).encode(o)
        for k, v in self._replacement_map.items():
            result = result.replace('"@@%s@@"' % (k,), v)
        return result

WORKING_DIR_UTILS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

def visualize_front(front, filepath, title='pareto front', show=True, f1_max=None, f2_max=None):
    plt.figure()
    # ax= fig.add_axes([0,0,1,1])

    f1 = [solution.objectives[0] for solution in front]
    f2 = [solution.objectives[1] for solution in front]    

    plt.scatter(f1, f2, color='r')

    if f1_max:
        plt.xlim(right=f1_max)
    if f2_max:
        plt.ylim(top=f2_max)

    plt.xlabel('f1')
    plt.ylabel('f2')
    plt.title(title)
    plt.savefig(filepath)
    if show:
        plt.show()

    plt.close('all')

def visualize_solutions(solutions, filepath, title='pareto front', show=True, f1_max=None, f2_max=None):
    plt.figure()
    # ax= fig.add_axes([0,0,1,1])

    f1_front = [solution.objectives[0] for solution in solutions if solution.nondominated_rank == 0]
    f2_front = [solution.objectives[1] for solution in solutions if solution.nondominated_rank == 0]    
    plt.scatter(f1_front, f2_front, color='b', zorder=2)

    f1 = [solution.objectives[0] for solution in solutions if solution.nondominated_rank != 0]
    f2 = [solution.objectives[1] for solution in solutions if solution.nondominated_rank != 0]   
    plt.scatter(f1, f2, color='r', zorder=1)

    if f1_max:
        plt.xlim(left=0,right=f1_max)
    if f2_max:
        plt.ylim(bottom=0,top=f2_max)
    
    plt.xlabel('f1')
    plt.ylabel('f2')
    plt.title(title)
    plt.savefig(filepath)
    if show:
        plt.show()

    plt.close('all')

def make_gif(fileexp, filename):
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

def remove_file(fileexp):
    # Get a list of all the file paths that ends with .txt from in specified directory
    fileList = glob.glob(fileexp)
    
    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)


def save_results(pareto_front, solutions, best_mr, out_dir, visualization=False):
    # save results
    print(f"saved in {out_dir}")
    pareto_dict = []
    for solution in pareto_front:
        solution_dict = {}
        network = solution.decode()
        solution_dict["chromosome"] = NoIndent(list(solution.chromosome))
        solution_dict["num_used_relays"] = network.num_used_relays
        solution_dict["energy_consumption"] = network.calc_max_energy_consumption()
        solution_dict["parent"] = NoIndent(network.parent)
        solution_dict["num_childs"] = NoIndent(network.num_childs)
        solution_dict["hop"] = network.max_depth
        solution_dict["nondominated_rank"] = solution.nondominated_rank
        solution_dict["crowding_distance"] = solution.crowding_distance

        pareto_dict.append(solution_dict)

    with open(os.path.join(out_dir, 'pareto-front.json'), mode='w') as f:
        pareto_json = json.dumps(pareto_dict, cls=NoIndentEncoder, sort_keys=True, indent=2)
        f.write(str(pareto_json))

    solutions_dict = []
    for solution in solutions:
        solution_dict = {}
        network = solution.decode()
        solution_dict["chromosome"] = NoIndent(list(solution.chromosome))
        solution_dict["num_used_relays"] = network.num_used_relays
        solution_dict["energy_consumption"] = network.calc_max_energy_consumption()
        solution_dict["parent"] = NoIndent(network.parent)
        solution_dict["num_childs"] = NoIndent(network.num_childs)
        solution_dict["hop"] = network.max_depth
        solution_dict["nondominated_rank"] = solution.nondominated_rank
        solution_dict["crowding_distance"] = solution.crowding_distance

        solutions_dict.append(solution_dict)

    with open(os.path.join(out_dir, 'solutions.json'), mode='w') as f:
        solutions_json = json.dumps(solutions_dict, cls=NoIndentEncoder, sort_keys=True, indent=2)
        f.write(str(solutions_json))

    sorted_best_mr = sorted(best_mr.items())
    with open(os.path.join(out_dir, 'best-mr.txt'), mode='w') as f:
        for i, value in sorted_best_mr:
            f.write(str(i) + " " + str(value) + "\n")

    if visualization:
        visualize_front(pareto_front, '{}/pareto-front.png'.format(out_dir),
            title='pareto-front', show=False)

        visualize_solutions(solutions, '{}/solutions.png'.format(out_dir),
            title='solution-front', show=False)

        gifexp = os.path.join(out_dir, 'solutions-gen-*.png')
        gifname = os.path.join(out_dir, 'solutions.gif')
        make_gif(gifexp, gifname)
        remove_file(gifexp)