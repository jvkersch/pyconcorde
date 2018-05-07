from os.path import dirname, join as pjoin

import numpy as np


BERLIN_TOUR = np.array(
    [0, 48, 31, 44, 18, 40,  7,  8,  9, 42, 32, 50, 10, 51, 13, 12, 46,
     25, 26, 27, 11, 24,  3,  5, 14,  4, 23, 47, 37, 36, 39, 38, 35, 34,
     33, 43, 45, 15, 28, 49, 19, 22, 29,  1,  6, 41, 20, 16,  2, 17, 30,
     21])
BERLIN_OPT_VALUE = 7542


SOLUTION_DATA = {
    'berlin52': (BERLIN_TOUR, BERLIN_OPT_VALUE)
}


def get_dataset_path(tspname):
    basedir = dirname(__file__)
    return pjoin(basedir, "data", tspname + '.tsp')


def get_solution_data(tspname):
    return SOLUTION_DATA[tspname]
