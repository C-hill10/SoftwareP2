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

#need to place exit randomly

#initialize goats (make sure in inner grid)
positions = set()
while len(positions) < NUM_GOATS:
    pos = (random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2))
    if pos != exit_pos:
        positions.add(pos)

goat_positions = torch.tensor(list(positions), dtype=torch.int32, device=device)
goat_active = torch.ones(NUM_GOATS, dtype=torch.bool, device=device)

directions = torch.tensor([[0, 1], [0, -1], [-1, 0], [1, 0]], dtype=torch.int32, device=device)

#need movement log here-ish

#begin iteration loop
for _ in range(500):  # This is an arbitrary value
    if not goat_active.any():
        break

    rand_dirs = directions[torch.randint(0, 4, (NUM_GOATS,), device=device)]
    new_positions = goat_positions + rand_dirs

    # this is to prevent goats from moving to border
    x_valid = (new_positions[:, 0] > 0) & (new_positions[:, 0] < GRID_SIZE - 1)
    y_valid = (new_positions[:, 1] > 0) & (new_positions[:, 1] < GRID_SIZE - 1)
    valid_move = x_valid & y_valid & goat_active

    # Check for collisions here
    occupied = set(tuple(pos.cpu().numpy()) for pos in goat_positions)
    move_mask = []
    for i, pos in enumerate(new_positions):
        new_pos = tuple(pos.cpu().numpy())
        if new_pos not in occupied and valid_move[i]:
            move_mask.append(True)
        else:
            move_mask.append(False)

    move_mask = torch.tensor(move_mask, dtype=torch.bool, device=device)

    # move goats
    goat_positions[move_mask] = new_positions[move_mask]

    #check for exit

    #log positions
#end iteration loop

#output
