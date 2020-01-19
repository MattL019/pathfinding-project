import queue, time
"""Simple implementation of Breadth First Search algorithm"""

opposite_directions = { "L": "R", "R": "L", "U": "D", "D": "U" }

def resolve_path(path, start):
  """Translates the given path into the respective coordinates"""
  offset_x = -path.count('L') + path.count('R')
  offset_y = -path.count('U') + path.count('D')
  return (start[0]+offset_x, start[1]+offset_y)

def valid_pos(maze, path, start):
  """Returns True if the path leads to a valid position in the maze"""

  # Check if we are going backwards, e.g LR, RL, UD, DU as these are contradicting moves
  if len(path) >= 2 and path[-2] == opposite_directions[path[-1]]: return False
  
  x, y = resolve_path(path, start) # Get path's final coordinates
  return True if (y >= 0 and y < len(maze)) and (x >= 0 and x < len(maze[0])) and [" ", "X", "O"].count(maze[y][x]) > 0 else False

def end_pos(maze, path, start):
  """Returns True if the path leads to the end position in the maze"""
  x, y = resolve_path(path, start)
  return True if maze[y][x] == "X" else False

def find_start(maze):
  """Returns the starting position coordinates of the maze, or False if none"""
  for y in range(len(maze)): # Find starting position
    for x in range(len(maze[y])):
      if maze[y][x] == "O": return (x, y)
  return False

def solve(maze):
  """Solves the maze"""
  start = find_start(maze)
  if not start: return "Maze does not have a starting position." # Ensure maze has a starting position
  q = queue.Queue() # Create a blank Queue 
  q.put("") # with an empty path
  newest_path = "" # Start with a blank newest path
  start_time = time.time() # Start a timer
  visited_paths = [] # A list of all visisted coorindates - for visual representation
  timed_out = False

  while not end_pos(maze, newest_path, start): # While the newest path does not lead to the end
    # Timeout if cannot find goal after 5 seconds
    if time.time() - start_time > 100: 
      timed_out = True
      break

    newest_path = q.get()
    for dir in ['L', 'R', 'U', 'D']:

      # Check if the current direction is valid
      potential_path = newest_path + dir
      if valid_pos(maze, potential_path, start): 
        q.put(potential_path) # If our potential new path is valid, add it to the queue
        visited_paths.append(potential_path)

  # If our loop has ended then "newest_path" must be the shortest possible path leading to the end

  elapsed_time = round((time.time() - start_time) * 1000, 3) # Get elapsed time

  visited_coordinates = [] # A list of visited coordinates
  for i, path in enumerate(visited_paths):
    coords = resolve_path(path, start) # Get coords of current path
    try: 
      visited_coordinates.index(coords) # Check if coords have already been visited
      continue # skip if coord found
    except: visited_coordinates.append(coords)

  return "Took too long to find path, timed out" if timed_out else {
    "shortest_path": newest_path,
    "elapsed_time_ms": elapsed_time,
    "visited_paths": visited_paths,
    "visited_coordinates": visited_coordinates
  }


#Example
"""print(solve([
  ["O"," ","#"],
  [" "," ","#"],
  ["#"," ","X"]
]))"""
