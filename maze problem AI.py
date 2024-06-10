#!/usr/bin/env python
# coding: utf-8

# In[1]:


import heapq
#import pyamaze
#from pyamaze import PyMaze
#from envs import Maze
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


# In[2]:


def display_maze(maze_layout):
    for row in maze_layout:
        print(" ".join(map(str, row)))


# In[3]:


def display_maze_with_paths(maze_layout, explored_nodes, optimal_path):
    for i in range(len(maze_layout)):
        for j in range(len(maze_layout[0])):
            current_location = (i, j)

            if current_location == starting_location:
                print("S", end=" ") 
            elif current_location == end_location:
                print("E", end=" ")  
            elif current_location in explored_nodes:
                print(".", end=" ") 
            elif current_location in optimal_path:
                print("-", end=" ")
            else:
                print("." if maze_layout[i][j] == 0 else "X", end=" ") 
        print()


# In[4]:


'''
def plot_maze_with_path(ax, maze_layout, optimal_path):
    pyamaze_layout = [['.' if cell == 0 else 'X' for cell in row] for row in maze_layout]

    maze = pyamaze.Maze(pyamaze_layout)

    maze.plot(ax=ax)

    for position in optimal_path:
        maze[position[0]][position[1]].set_path()

    ax.imshow(maze.to_image(), cmap='viridis', interpolation='nearest')
    ax.set_title("Maze with Path")
'''


# In[5]:


def calculate_manhattan_distance(node, destination):
    x1, y1 = node
    x2, y2 = destination
    return abs(x1 - x2) + abs(y1 - y2)


# In[6]:


def get_neighboring_nodes(node, rows, columns):
    neighbors = []
    for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_location = (node[0] + move[0], node[1] + move[1])
        if 0 <= new_location[0] < rows and 0 <= new_location[1] < columns and maze_layout[new_location[0]][new_location[1]] != 'X':
            neighbors.append(new_location)
    return neighbors


# In[7]:


def reconstruct_optimal_path(predecessors, start, end):
    current_location = end
    path = []

    while current_location != start:
        path.insert(0, current_location)
        current_location = predecessors[current_location]
    path.insert(0, start)
    return path


# In[8]:


def astar_pathfinding(maze_layout, start, goal):
    rows, columns = len(maze_layout), len(maze_layout[0])
    open_nodes = [(0, start)]  
    node_predecessors = {}  
    cost_to_reach = {start: 0} 

    explored_nodes = []

    while open_nodes:
        current_cost, current_location = heapq.heappop(open_nodes)

        explored_nodes.append(current_location)

        if current_location == goal:
            optimal_path = reconstruct_optimal_path(node_predecessors, start, goal)
            return optimal_path

        for neighbor_location in get_neighboring_nodes(current_location, rows, columns):
            new_cost = cost_to_reach[current_location] + 1

            if neighbor_location not in cost_to_reach or new_cost < cost_to_reach[neighbor_location]:
                cost_to_reach[neighbor_location] = new_cost
                priority = new_cost + calculate_manhattan_distance(neighbor_location, goal)
                heapq.heappush(open_nodes, (priority, neighbor_location))
                node_predecessors[neighbor_location] = current_location
        
        for location in explored_nodes:
            print(f"Explored Node: {location}")
    
    return None 


# In[9]:


def plot_maze_with_path(ax, maze_array, optimal_path):
    maze_array = np.array(maze_array)
    maze_array[maze_array == 'X'] = 1
    maze_array[maze_array == 'S'] = 2
    maze_array[maze_array == 'E'] = 3

    maze_array = maze_array.astype(int)

    for position in optimal_path:
        if maze_array[position[0]][position[1]] != '-':
            maze_array[position[0]][position[1]] = 4

    #ax.imshow(maze_array, cmap='magma', interpolation='nearest')
    #ax.set_title("Maze with Path")
    
    #custom_colors = ['grey', 'red', 'orange', 'yellow', 'blue']
    custom_colors = ['#000000', '#ff0000', '#ffd700', '#000000', '#0000ff']
    cmap = ListedColormap(custom_colors)

    ax.imshow(maze_array, cmap=cmap, interpolation='nearest')
    ax.set_title("Maze with Path")


# In[10]:


if __name__ == "__main__":
    maze_layout = [
        [0, 'X', 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 'X', 0, 'X', 0, 0],
        [0, 'X', 0, 0, 'X', 0],
        [0, 0, 0, 0, 'X', 'E'],
    ]

    starting_location = (0, 0)
    end_location = (4, 5)

    obstacle_locations = [(0, 1), (2, 1), (2, 3), (3, 1), (3, 4), (4, 4)]

    for obstacle in obstacle_locations:
        maze_layout[obstacle[0]][obstacle[1]] = 'X'

    maze_layout[starting_location[0]][starting_location[1]] = 'S'

    print("Original Maze:")
    display_maze(maze_layout)

    explored_nodes = []
    optimal_path = astar_pathfinding(maze_layout, starting_location, end_location)

    if optimal_path:
        print("\nShortest path from start to end:")
        print(optimal_path)
        print("\nMaze with paths:")
        display_maze_with_paths(maze_layout, explored_nodes, optimal_path)

        fig, ax = plt.subplots()
        plot_maze_with_path(ax, maze_layout, optimal_path)
        plt.show()
    else:
        print("\nNo path found.")


# In[11]:


import pygame
from pygame.locals import QUIT

pygame.init()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

cell_size = 100
width, height = len(maze_layout[0]) * cell_size, len(maze_layout) * cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pathfinding Visualization")

def draw_obstacles():

    for i in range(len(maze_layout)):
        for j in range(len(maze_layout[0])):
            rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
            if maze_layout[i][j] == 'X':
                pygame.draw.rect(screen, RED, rect)

def draw_start_and_end():

    for position, color in [(starting_location, BLUE), (end_location, BLUE)]:
        rect = pygame.Rect(position[1] * cell_size, position[0] * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, color, rect)

def draw_current_position(position):

    rect = pygame.Rect(position[1] * cell_size, position[0] * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, BLUE, rect)

running = True
current_position = starting_location

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(BLACK)
    draw_obstacles()
    draw_start_and_end()
    draw_current_position(current_position)

    pygame.display.flip()
    pygame.time.delay(500)

    if optimal_path:
        if len(optimal_path) > 1:
            current_position = optimal_path.pop(0)
        else:
            running = False
    else:
        running = False

pygame.quit()


# In[ ]:




