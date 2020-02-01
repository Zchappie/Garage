
# coding: utf-8

# In[1]:


import sys
import numpy as np
from numpy import linalg as LA


# In[2]:


# Get input from command prompt and run the program
input_arg = sys.argv[1]


# In[7]:


def find_location(symbol, input_matrix):
    location = [0,0]
    for row in range(len(input_matrix)):
        for column in range(len(input_matrix[row])):
            if(symbol == input_matrix[row][column]):
                location[0] = row
                location[1] = column
                break
    return location


# In[8]:


#matrix = [['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'X'], ['_', '*', '*', '_', '*', '*', '_', '*', '*', '_', '*', '*', '_', '*', '*', '_', '*', '*'], ['_', '*', '_', '_', '*', '_', '_', '*', '_', '_', '*', '_', '_', '*', '_', '_', '*', '_'], ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_'], ['_', '*', '*', '_', '*', '*', '_', '*', '*', '*', '*', '*', '_', '*', '*', '_', '*', '*'], ['_', '*', '_', '_', '*', '_', '_', '*', '_', '*', '*', '_', '_', '*', '_', '_', '*', '_'], ['_', '_', '_', '_', '_', '_', '_', '*', '*', '*', '_', '_', '_', '_', '_', '_', '_', '_'], ['_', '*', '*', '_', '*', '*', '_', '*', '*', '_', '*', '*', '_', '*', '*', '_', '*', '*'], ['_', '*', '_', '_', '*', '_', '_', '*', '_', '_', '*', '_', '_', '*', '_', '_', '*', '_'], ['_', '_', '_', '_', '_', '_', '_', '_', 'R', '_', '_', '_', '_', '_', '_', '_', '_', '_'], ['_', '*', '*', '_', '*', '*', '_', '*', '*', '_', '*', '*', '_', '*', '*', '_', '*', '*'], ['_', '*', '_', '_', '*', '_', '_', '*', '_', '_', '*', '_', '_', '*', '_', '_', '*', '_']]
# symbol = 'R'
# current_position = find_location(symbol, matrix)
# goal_position = find_location("X", matrix)
# print(current_position, goal_position)


# In[9]:


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
        if(input_matrix[surrounding_cell[0]][surrounding_cell[1]] != "*"):
            waiting_list.append(surrounding_cell)        
    return waiting_list


# In[10]:


# evaluation = []
# path_cost = []
# frontier = []
# explored_cells = current_position
# waiting_list = valid_surrounding(current_position, matrix, explored_cells, frontier)
# print(waiting_list)


# In[37]:


def evaluation_function(current_position, goal_position, frontier, path_cost, evaluation, valid_neighbors, current_cost):
    heuristic = []
    
    # compute the cost of each possible step
    move_step = []
    step_cost = []
    for cell in frontier:
        heuristic.append(LA.norm(np.array(cell) - np.array(goal_position))) # heuristic
        
    for cell in valid_neighbors:
        move_step.append([abs(x) for x in (np.array(cell) - np.array(current_position))])
        diag = min(move_step[-1])
        verti_horizon = [move_step[-1][0] - diag, move_step[-1][1] - diag]
        step_cost.append(diag*10 + np.dot(verti_horizon, [6,5])) # single step path cost
    
    # only update the nodes newly added into the frontier
    for i in range(len(frontier) - len(valid_neighbors), len(frontier)):
        path_cost[i] += step_cost[i-(len(frontier) - len(valid_neighbors))] + current_cost # path cost

    evaluation = [a+b for a, b in zip(heuristic, path_cost)] 
    
    # sort the frontier according to cost
    frontier = [x for _,x in sorted(zip(evaluation, frontier))]
    path_cost = [x for _,x in sorted(zip(evaluation, path_cost))]
    sorted(evaluation)
    
    return frontier, path_cost, evaluation


# In[33]:


# frontier = waiting_list
# path_cost = len(frontier)*[0]
# valid_neighbors = waiting_list
# evaluation = [0]*len(waiting_list)
# current_cost = path_cost[0]
# frontier, path_cost, evaluation= evaluation_function(current_position, goal_position, 
#                                                      waiting_list, path_cost, evaluation, valid_neighbors, current_cost)
# print(frontier, path_cost, evaluation)


# In[34]:


def goal_test(node, goal_position):
    if(node[0]==goal_position[0] and node[1]==goal_position[1]):
        return True
    else:
        return False


# ### Searching

# In[44]:


def search_path(input_matrix):

    # find the starting(goal) position
    rob_position = find_location("R", input_matrix)
    goal_position = find_location("X", input_matrix)
    
    # initialization
    explored_cells = []
    a = rob_position
    explored_cells.append(a)
        
    explored_his = [] # [x, y, evaluation, path_cost, heuristic]
    frontier = []
    waiting_list = valid_surrounding(rob_position, input_matrix, explored_cells, frontier)
    frontier = waiting_list
    path_cost = len(frontier)*[0]
    valid_neighbors = waiting_list
    evaluation = [0]*len(waiting_list)
    current_cost = 0
    
    # sort the valid_surrounding according to the evaluation 
    frontier, path_cost, evaluation = evaluation_function(rob_position, goal_position, 
                                                          frontier, path_cost, evaluation,
                                                          valid_neighbors, current_cost)
    
    while(len(frontier) != 0):
       
        # pop the first one, save it into reached_list
        current_position = frontier[0]
        explored_cells = explored_cells
        explored_cells.append(current_position)
        explored_his.append([current_position[0], current_position[1]])
        
        explored_his[-1].append(evaluation[0])
        explored_his[-1].append(path_cost[0])
        
        if(goal_test(current_position, goal_position)):
            return path_cost[0]
        
        del frontier[0]
        del evaluation[0]
        current_cost = path_cost[0]
        del path_cost[0]
        
        waiting_list = valid_surrounding(current_position, input_matrix, explored_cells, frontier)
        for i in waiting_list:
            frontier.append(i)
        path_cost = path_cost + len(waiting_list)*[0]
        valid_neighbors = waiting_list
        # sort
        frontier, path_cost, evaluation = evaluation_function(current_position, goal_position, 
                                                              frontier, path_cost, evaluation,
                                                              valid_neighbors, current_cost)
#         print("current_position", current_position)
#         print("frontier", frontier)
#         print("path_cost", path_cost)
#         print("evaluation", evaluation)
        print("explored_cells", explored_cells)
    # if no solution
    return False


# ### Main function

# In[46]:


def solve_task1(input_matrix):
    # Enter your code here.
    # Return the minimum cost or return No path found!
    
    answer = search_path(input_matrix)
    
    if(answer > 0):
        return(answer)
    else:
        return "No path found!"


# ### Load the problem, and automatic solving

#print(solve_task1(matrix))
# In[ ]:


def run_program(file_name = input_arg):
    # Read the input matrix
    input_matrix = np.genfromtxt(file_name, dtype='str')
    input_matrix = input_matrix.tolist()
    # print(input_matrix)
    # Your main function to solve the matrix
    print(solve_task1(input_matrix))


run_program()

# To test the result yourself,
# Open the command line tool, navigate to the folder and execute:
# python Solution1.py input_for_task1.txt

