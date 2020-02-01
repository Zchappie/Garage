import sys
import numpy as np

# Use as many helper functions as you like
#------------------------------------------------------------------------------
def find_all_enemies(input_matrix, symbol_e):
    enemy_list = []
    for i in range(len(input_matrix)):
        for j in range(len(input_matrix[i])):
            if input_matrix[i][j] == symbol_e:
                enemy_list.extend([[i, j]])            
    
    return enemy_list
# TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST
#input_matrix = [['X','X','X','X','X'],
#                ['.','.','X','.','X'],
#                ['X','.','X','X','X'],
#                ['X','X','.','.','X'],
#                ['X','X','X','X','X']]
#enemy_list = find_all_enemies(input_matrix, ".")
#print(enemy_list)
# TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST

#------------------------------------------------------------------------------
def find_enemy_at_boundary(enemy_list, right_bound, lower_bound):
    enemy_at_boundary = []
    for enemy in enemy_list:
        if enemy[0] == 0 or enemy[1] == 0 or enemy[0] == lower_bound or enemy[1] == right_bound:
            enemy_at_boundary.extend([[enemy[0], enemy[1]]])
    return enemy_at_boundary
# TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST
#right_bound = len(input_matrix[0])
#lower_bound = len(input_matrix)
#enemy_at_boundary = find_enemy_at_boundary(enemy_list, right_bound, lower_bound)
#print(enemy_at_boundary)
# TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST

#------------------------------------------------------------------------------
def valid_surrounding(current_position, input_matrix, explored_cells, frontier):
    rows, cols = np.array(input_matrix).shape
    waiting_list = []
    directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
    
    for direc in directions:
        surrounding_cell = np.add(np.array(direc), np.array(current_position)).tolist()
        in_frontier = surrounding_cell in frontier
        in_explored = surrounding_cell in explored_cells
        
        if(surrounding_cell[0]>=rows or surrounding_cell[1]>=cols 
           or surrounding_cell[0]<0 or surrounding_cell[1]<0  # can't go outside the map
           or in_frontier or in_explored): 
            continue
        if(input_matrix[surrounding_cell[0]][surrounding_cell[1]] == "."):
            waiting_list.append(surrounding_cell)
    return waiting_list
#------------------------------------------------------------------------------
def region_growing(enemy, input_matrix):
    # breadth-first search
    enemy_region = []
    frontier = []
    frontier.append(enemy) # initialize the frontier
    explored = []
    
    while frontier: # not empty
        current_pos = frontier[0]
        explored.append(frontier[0])
        enemy_region.append(frontier[0])
        del frontier[0]
        
        val_neighbors = valid_surrounding(current_pos, input_matrix, explored, frontier)
        for i in val_neighbors:
            frontier.append(i)
    
    return enemy_region
# TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST
#enemy_regions = []
#while enemy_at_boundary: # not empty
#    enemy_regions.append(region_growing(enemy_at_boundary[0], input_matrix))
#    
#    for enemy_region in enemy_regions[-1]:
#        for enemy in enemy_region:
#            if enemy in enemy_at_boundary:
#                enemy_at_boundary.remove(enemy)
#    del enemy_at_boundary[0]
#print(enemy_regions)
# TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST
#------------------------------------------------------------------------------
#def turn_to_allies(enemy_region, output_matrix):
#    for enemy in enemy_region:
#        output_matrix[enemy[0]][enemy[1]] = 'X'
#    return output_matrix
# TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST
#output_matrix = input_matrix # used for drawing
#for enemy_region in enemy_regions:
#    output_matrix = turn_to_allies(enemy_region, output_matrix)
#print(output_matrix)
# TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST--TEST
#------------------------------------------------------------------------------
def solve_task2(input_matrix):
    input_matrix = input_matrix.tolist()
    #print(input_matrix)
    # input_matrix = input_matrix # only for test case
    right_bound = len(input_matrix[0]) - 1
    lower_bound = len(input_matrix) - 1
    output_matrix = input_matrix # used for drawing
    
    # find all enemies in the map
    enemy_list = find_all_enemies(input_matrix, ".")
    
    # find all enemies at the boundary
    enemy_at_boundary = find_enemy_at_boundary(enemy_list, right_bound, lower_bound)
    
    # group the enemies at the boundary into regions
    enemy_regions = []
    while enemy_at_boundary: # not empty
        enemy_regions.append(region_growing(enemy_at_boundary[0], input_matrix))
        
        for enemy_region in enemy_regions[-1]:
            for enemy in enemy_region:
                if enemy in enemy_at_boundary:
                    enemy_at_boundary.remove(enemy) # avoid duplicated searching
        del enemy_at_boundary[0]
    
    # remove the enemy near the boundary
    for enemy_region in enemy_regions:
        for enemy in enemy_region:
            if enemy in enemy_list:
                enemy_list.remove(enemy)
    # print('enemy list', enemy_list)
            
    # turn the enemies not in enemy regions to ally
    for enemy in enemy_list:
        output_matrix[enemy[0]][enemy[1]] = 'X'
    return output_matrix

#------------------------------------------------------------------------------
#print(solve_task2(input_matrix))
# Get input from command prompt and run the program
input_arg = sys.argv[1]
def run_program(filename = input_arg):
    # Read the input matrix
    input_matrix = np.genfromtxt(filename, dtype='str')
    
    # Your main function to solve the matrix
    output = solve_task2(input_matrix)

    # print the matrix to a txt file
    np.savetxt('output_for_task2.txt', output, fmt="%s")


run_program()


# To test the result yourself,
# Open the command line tool, navigate to the folder and execute:
# python Solution2.py input_for_task2.txt
