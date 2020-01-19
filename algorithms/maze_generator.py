from random import randrange
import algorithms.breadth_first_search as bfs

"""Generates a maze"""
horizontal_wall = ["#" for i in range(10)]

def generate_maze(width, height, complexity=None):
  # Our template maze that we use to generate different paths
  template_maze = [horizontal_wall]
  for i in range(height-2):
    row = ["#"]
    row.extend([" " for i in range(width-2)])
    row.append("#")
    template_maze.append(row)
  template_maze.append(horizontal_wall)

  # Our final maze that we will write to
  final_maze = [["#" for x in range(width)] for y in range(height)]

  if complexity == None: complexity = round(((width-1)*(height-1))/20) # Get a good complexity amount

  start_x, start_y = get_random_coords(width, height) # Get start position coordinates
  template_maze[start_y][start_x] = "O" # Populate our maze with our starting position
  final_maze[start_y][start_x] = "O" # Our final maze will have same starting position

  for run in range(complexity):
    while True: # Generate end coordinates, and make sure they are not identical to the start position
      end_x, end_y = get_random_coords(width, height)
      if end_x != start_x and end_y != start_y: break

    template_maze[end_y][end_x] = "X" # Populate our maze with our end position

    solved_maze = bfs.solve(template_maze) # Create a BFS instance for our maze
    shortest_path = solved_maze['shortest_path'] # Find the shortest path
    for i in range(1, len(shortest_path)+1): # Cycle through each step
      x, y = bfs.resolve_path(shortest_path[0:i], (start_x, start_y)) # Get coordinate of new step
      final_maze[y][x] = " " # Update final maze to have a space
    
    template_maze[end_y][end_x] = " " # Reset template maze end point
    if run == complexity-1: final_maze[end_y][end_x] = "X" # Set end point on our final maze 
  return final_maze

def get_random_coords(width, height):
  """Returns a random set of coordinates within the Maze outer walls"""
  return randrange(1, width-2), randrange(1, height-2)