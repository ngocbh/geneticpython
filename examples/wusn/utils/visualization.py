import matplotlib.pyplot as plt
import os
from PIL import Image
import glob


WORKING_DIR_UTILS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

def visualize_front(front, filename, title='pareto front', show=True, f1_max=None, f2_max=None):
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
    plt.savefig(os.path.join(WORKING_DIR_UTILS, filename))
    if show:
        plt.show()

    plt.close('all')

def visualize_solutions(solutions, filename, title='pareto front', show=True, f1_max=None, f2_max=None):
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
    plt.savefig(os.path.join(WORKING_DIR_UTILS, filename))
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