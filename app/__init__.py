from flask import Flask, Response, request
from flask_cors import CORS
from algorithms import breadth_first_search
from algorithms.maze_generator import generate_maze

app = Flask(__name__)
CORS(app)

# Main API route to solve a maze
@app.route('/solve/<algo>', methods=['POST'])
def solve(algo):
  if not request.is_json: # Ensure request is JSON
    return Response("Please send a JSON maze.", 400)

  try: # Try to extract maze from JSON
    maze = request.get_json()['maze']
  except:
    return Response("Maze not found in request data.", 400)

  return globals()[algo].solve(maze, timeout=20)

# Returns a random maze generated by our maze generator
@app.route('/random_maze', methods=['GET'])
def random_maze():
  # Get our width, height and complexity from URL parameters
  width, height, complexity = request.args.get('width'), request.args.get('height'), request.args.get('complexity')
  # If no width or no height is provided, return an error
  if width == None or height == None: return Response("Please provide both a width and a height", 400)
  # Return our generated maze
  return { "maze": generate_maze(int(width), int(height), int(complexity or "10")) }

app.config.from_object('config')
# if app.config['FLASK_ENV'] == 'development': CORS(app) # Enable cross-origin requests for dev environment