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

#need to place random exit

#initialize goat positions

#iteration loop
#check for collision
occupied = set(tuple(pos.cpu().numpy()) for pos in goat_positions)
  move_mask = []
  for i, pos in enumerate(new_positions):
      new_pos = tuple(pos.cpu().numpy())
      if new_pos not in occupied and valid_move[i]:
          move_mask.append(True)
      else:
          move_mask.append(False)
move_mask = torch.tensor(move_mask, dtype=torch.bool, device=device)
goat_positions[move_mask] = new_positions[move_mask]

exited = (goat_positions == exit_tensor).all(dim=1)
goat_active[exited] = False
