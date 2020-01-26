"""Revised implementation of breadth first search algorithm - v2"""

import queue, time

# Output requirements
# 1. A 2D list, each index contains a list of coordinates for that step
# 2. A list of coordinates that maps out the shortest path
# 3. Time elapsed to solve the maze

def resolve_path(path, start):
  """Translates cardinal path into coordinates respective of starting position"""
  offset_x = -path.count('L') + path.count('R')
  offset_y = -path.count('U') + path.count('D')
  return (start[0]+offset_x, start[1]+offset_y) # (x, y)

def valid_pos(maze, start, path, new_move):
  """Returns True if new move provided is considered valid by the algorithm"""

  # 1. Ensure the path is not turning back on itself
  if len(path) >= 2 and path[-2] == new_move: return False
  # New move x and y coordinates
  x, y = new_move
  # 2. Check if the new coordinates are not already visited in this path
  for coord in path:
    if coord == new_move: 
      return False

  if ( # 3. Ensure x and y coords are within the maze dimensions
    y < 0 or y >= len(maze) or x < 0 or x >= len(maze[0]) or 
    maze[y][x] == "#" # 4. Ensure end coordinate is not a wall
  ): return False

  return True # All checks passed. Position is valid

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
  q.put([start]) # Begin at the start

  start_time = time.time() # Store the starting time
  shortest_path = [] # Stores the shortest path
  paths_tried = 0
  visited_coordinates = set()

  # While we do not have a shortest path
  while len(shortest_path) == 0:
    paths_tried += 1
    current_path = q.get() # Retrieve oldest path from queue

    for move in [(-1, 0), (1, 0), (0, 1), (0, -1)]: # Loop through each direction
      # our potential path, by adding the current move tuple

      potential_move = (current_path[-1][0] + move[0], current_path[-1][1] + move[1])
      # Check is new move coords are valid. Continue/skip if not..
      if not valid_pos(maze, start, path=current_path, new_move=potential_move): continue

      new_path = current_path + [potential_move] # Form our new valid path

      # If potential path leads to END of maze, set shortest path, which breaks while loop
      if maze[potential_move[1]][potential_move[0]] == "X":
        print("solved")
        shortest_path =  new_path
        break

      # Potential path is not shortest but is valid - add to queue
      q.put(new_path)
      visited_coordinates.add(potential_move) # Add new coords to visited coordinates
    
  return {
    "visited_coordinates": list(visited_coordinates),
    "paths_tried": paths_tried,
    "shortest_path": shortest_path,
    "time_elapsed_ms": round((time.time() - start_time) * 1000, 3) # Calculate time elapsed
  }

# Example
"""print(solve([
  ["O"," ","#"],
  [" "," ","#"],
  ["#"," ","X"]
]))"""