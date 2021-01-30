from concorde.run import Problem

import numpy as np

problem = Problem.from_matrix([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
problem.to_tsp("foo")
