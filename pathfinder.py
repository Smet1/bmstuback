from PIL import Image
import numpy as np


def init_maze(path_to_file):
    im = Image.open(path_to_file)
    tmp = np.array(im.convert('1')) # converts to wb mode

    maze = np.empty((tmp.shape[0], tmp.shape[1]), None)

    for i in range(len(tmp)):
        for j in range(len(tmp[i])):
            maze[i][j] = 1 if tmp[i][j] else 0

    return maze


def find_path(path_to_file, start, end):
    maze = init_maze(path_to_file)
    path = []
    max_step = 10



if __name__ == "__main__":
    find_path('bmstuplan.png', (484, 170), (94, 164))
