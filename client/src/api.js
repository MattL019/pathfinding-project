// Get a random maze
export async function getRandomMaze(size) {
  return fetch(`http://localhost:5000/random_maze?width=${size}&height=${size}`)
    .then(response => response.json())
    .then(json => json.maze)
}

// Solve the maze and return the solved maze
export async function solveMaze(algorithm, maze) {
  return fetch(`http://localhost:5000/solve/${algorithm}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ maze })
  }).then(response => response.json())
}