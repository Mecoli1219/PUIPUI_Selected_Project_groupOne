from node import *
import maze as mz
import score
import interface
import time

import numpy as np
import pandas
import time
import sys
import os

maze = mz.Maze("data/final_map_109.csv")

# print(maze.BFS("1"))
# distance = maze.BFS_rec("1","4", ["1"],None, 0)
# print(maze.test_route)
# print(distance)
# distance = maze.shortest_path("1",["1"], None, 0)
# print(maze.test_path)
print(maze.strategy("1"))