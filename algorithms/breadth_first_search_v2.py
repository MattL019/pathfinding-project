"""Revised implementation of breadth first search algorithm - v2"""

import queue, time

# Output requirements
# 1. A 2D list, each index contains a list of coordinates for that step
# 2. A list of coordinates that maps out the shortest path
# 3. Time elapsed to solve the maze

# Dict containing polar opposites of cardinal directions. Used to check if the algorithm is turning back on itself.
opposite_directions = { "L": "R", "R": "L", "U": "D", "D": "U" }

def resolve_path(path, start):
  """Translates cardinal path into coordinates respective of starting position"""
  offset_x = -path.count('L') + path.count('R')
  offset_y = -path.count('U') + path.count('D')
  return (start[0]+offset_x, start[1]+offset_y) # (x, y)

def valid_pos(maze, start, path):
  """Returns final (x, y) coords of path if path provided is considered valid by the algorithm"""

  # 1. Ensure the path is not turning back on itself (e.g UD, DU, RL, LR)
  if len(path) >= 2 and path[-2] == opposite_directions[path[-1]]: return False
  # 2. Calculate provided path's end coordinates
  x, y = resolve_path(path, start)

  if ( # 3. Ensure x and y coords are within the maze dimensions
    y < 0 or y >= len(maze) or x < 0 or x >= len(maze[0]) or 
    maze[y][x] == "#" # 4. Ensure end coordinate is not a wall
  ): return False

  return (x, y) # All checks passed. Position is valid

def find_start(maze):
  """Returns a tuple containing (x, y) starting position of provided maze"""
  for y in range(len(maze)):
    for x in range(len(maze[y])):
      if maze[y][x] == "O": return (x, y) # Check each point in maze, return coords with start position
  return False # False if we did not find a starting position

def solve(maze):
  """Solves provided maze, returning the visited coordinates, shortest path and time elapsed"""
  start = find_start(maze) # (x, y) starting position
  if not start: return False # Maze does not have a starting position

  q = queue.Queue() # Our path queue
  q.put("") # Begin with an empty path

  start_time = time.time() # Store the starting time
  shortest_path = "" # Stores the shortest path
  visited_coordinates = [] # 2D List where each index stores a list of visited coords (tuples) for each iteration

  # While we do not have a shortest path
  while len(shortest_path) == 0:
    current_path = q.get() # Retrieve oldest path from queue

    # A list that holds all new coordinates from potential paths for this iteration
    iteration_coordinates = []

    for dir in ['L', 'R', 'U', 'D']: # Loop through each direction
      potential_path = current_path + dir # Our potential path
      coords = valid_pos(maze, start, path=potential_path) # Coords of potential path if valid
      if not coords: continue # Path is not valid, skip this move.

      # If potential path leads to END of maze, set shortest path, which breaks while loop
      if maze[coords[1]][coords[0]] == "X": 
        shortest_path = potential_path
        break

      # Potential path is not shortest but is valid - add to queue
      q.put(potential_path)
      iteration_coordinates.append(coords) # Append coords to iteration coordinates
    
    visited_coordinates.append(iteration_coordinates) # Add iteration coords to overall coords

  return {
    "visited_coordinates": visited_coordinates,
    "shortest_path": shortest_path,
    "time_elapsed_ms": round((time.time() - start_time) * 1000, 3) # Calculate time elapsed
  }

# Example
"""print(solve([
  ["O"," ","#"],
  [" "," ","#"],
  ["#"," ","X"]
]))"""