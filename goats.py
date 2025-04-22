import torch
import numpy as np 
import csv
import random
import matplotlib.pyplot as plt 


#User input for scalable grid size 
GRID_SIZE=int(input("Enter grid size (5 to 100): "))
assert 5 <= GRID_SIZE <= 100, "Grid size must be in range"
INNER_GRID_SIZE= GRID_SIZE -2 
NUM_GOATS = (INNER_GRID_SIZE ** 2)

grid = torch.zeros((GRID_SIZE, GRID_SIZE), dtype=torch.int32, device="cuda")
