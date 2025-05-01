import torch
import numpy as np 
import csv
import random
import os
import matplotlib.pyplot as plt 


#User input for scalable grid size 
GRID_SIZE = int(input("Enter grid size (5 to 100): "))
assert 5 <= GRID_SIZE <= 100, "Grid size must be between 5 and 100"
INNER_GRID_SIZE = GRID_SIZE - 2

DENSITY = float(input("Enter goat density percentage (10 to 80): "))
assert 10 <= DENSITY <= 80, "Density must be between 10 and 80"
NUM_GOATS = int((INNER_GRID_SIZE ** 2) * (DENSITY / 100))
#need to add a DENSITY = code here for dynamic goat density

grid = torch.zeros((GRID_SIZE, GRID_SIZE), dtype=torch.int32, device="cuda")

#need to place exit randomly
#choose a random spot for the exit, 1-4 going clockwise starting from the bottom decides which side the exit is on 
#then a random number after decides which spot on that wall the exit will be
direction = random.randint(1, 4)
if direction == 1:
    exity = 1
    exitx = random.randint(2, GRID_SIZE-1)
elif direction == 2:
    exitx = 1
    exity = random.randint(2, GRID_SIZE-1)
elif direction == 3:
    exity = GRID_SIZE
    exitx = random.randint(2, GRID_SIZE-1)
else:  # direction == 4
    exitx = GRID_SIZE
    exity = random.randint(2, GRID_SIZE-1)

exit_pos = (exitx, exity)
exit_tensor = torch.tensor(exit_pos, device="cuda")

print(f"\n Exit is at: {exit_pos}")

#initialize goats (make sure in inner grid)
positions = set()
while len(positions) < NUM_GOATS:
    pos = (random.randint(2, GRID_SIZE-1), random.randint(2, GRID_SIZE-1))
    if pos != exit_pos:
        positions.add(pos)

goat_positions = torch.tensor(list(positions), dtype=torch.int32, device="cuda")
goat_active = torch.ones(NUM_GOATS, dtype=torch.bool, device="cuda")

#up, down, left, right
directions = torch.tensor([[0, 1], [0, -1], [-1, 0], [1, 0]], dtype=torch.int32, device="cuda")

#need movement log here-ish
goat_logs = [[tuple(pos.cpu().numpy())] for pos in goat_positions]
goat_paths = [[tuple(pos.cpu().numpy())] for pos in goat_positions]  # for print out

#begin iteration loop
MAX_STEPS = 300
for step in range(MAX_STEPS):  # This is an arbitrary value
    if not goat_active.any():
        break

    rand_dirs = directions[torch.randint(0, 4, (NUM_GOATS,), device="cuda")]
    new_positions = goat_positions + rand_dirs

    # this is to prevent goats from moving to border
    x_valid = (((new_positions[:, 0] > 1) & (new_positions[:, 0] < GRID_SIZE - 1)) or new_positions[:,:]==exit_pos)
    y_valid = (((new_positions[:, 1] > 1) & (new_positions[:, 1] < GRID_SIZE - 1)) or new_positions[:,:]==exit_pos)
    valid_move = x_valid & y_valid & goat_active
    # for i, pos in enumerate(new_positions):
    #     if((new_positions[i,0] <=1  or (new_positions[i,0] >= GRID_SIZE) and new_positions[i,0] != exitx) or (new_positions[i,1] <=1  or (new_positions[i,1] >= GRID_SIZE) and new_positions[i,1] != exity) ):
    #         print("I wanted to go to (", new_positions[i,0] ,", (", new_positions[i,1] , "). I am going back to (", goat_positions[i,0] ,", (" , goat_positions[i,1],")")
    #         new_positions[i,:]=goat_positions[i,:]
    # Check for collisions here
    occupied = set(tuple(pos.cpu().numpy()) for pos in goat_positions)
    move_mask = []
    for i, pos in enumerate(new_positions):
        new_pos = tuple(pos.cpu().numpy())
        if new_pos not in occupied and valid_move[i]:
            move_mask.append(True)
        else:
            move_mask.append(False)

    move_mask = torch.tensor(move_mask, dtype=torch.bool, device="cuda")

    # move goats
    goat_positions[move_mask] = new_positions[move_mask]

    #check for exit
    exited = (goat_positions == exit_tensor).all(dim=1)
    goat_active[exited] = False

    #log positions
    for i in range(NUM_GOATS):
        pos_tuple = tuple(goat_positions[i].cpu().numpy())
        goat_logs[i].append(pos_tuple)
        goat_paths[i].append(pos_tuple)

print(f"Simulation completed in {step+1} steps.")
#end iteration loop

#output
#make output folder
output_dir = "movement_logs"
os.makedirs(output_dir, exist_ok=True)
output_filename = os.path.join(output_dir, "goat_movements.txt")

# Write movement log to file
with open(output_filename, "w") as f:
    f.write(f"Exit: {exit_pos}\n")
    f.write(f"Grid Size: {GRID_SIZE}\n")
    for i, log in enumerate(goat_logs):
        line = f"{i+1}: {', '.join(f'({x},{y})' for x, y in log)}\n"
        f.write(line)

#output of goat paths
# print("\n Goat Movement Paths:")
# for i, path in enumerate(goat_paths):
#     print(f"Goat {i+1}: {path}")


#create visualization
