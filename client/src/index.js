import('../styles/reset.scss')
import('../styles/main.scss')

import MazeCanvas from 'maze-canvas'
import { getRandomMaze, solveMaze } from './api'

const mazeCanvas = new MazeCanvas("maze-canvas", {
  mazeDimensions: [9, 9],
  canvasMaxWidth: 600
})

// Starting maze
let basicMaze = [
  ['#','#','#','#','#','#','#','#','#'],
  ['#','O',' ',' ',' ',' ',' ',' ','#'],
  ['#',' ',' ',' ',' ',' ',' ',' ','#'],
  ['#',' ',' ',' ',' ',' ',' ',' ','#'],
  ['#',' ',' ',' ',' ',' ',' ',' ','#'],
  ['#',' ',' ',' ',' ',' ',' ',' ','#'],
  ['#',' ',' ',' ',' ',' ',' ',' ','#'],
  ['#',' ',' ',' ',' ',' ',' ','X','#'],
  ['#','#','#','#','#','#','#','#','#']
]
mazeCanvas.loadMaze(basicMaze)

// DOM Elements
const mazeStatus = document.getElementById('maze__status') // <p> that displays maze status

// Button controllers

/**
 * @desc Calls the API to solve the current maze and visually represents it on the maze canvas
 */
document.getElementById('btn__solve').onclick = async () => {
  if (mazeCanvas.solving) return // Only solve if not already solving!
  
  const currentMaze = mazeCanvas.getMazeStringArray() // Current maze string array
  let selector = document.getElementById('select__algorithm')
  const algorithm = selector.options[selector.selectedIndex].value // selected algorithm

  mazeCanvas.loading = true
  const solvedMaze = await solveMaze(algorithm, currentMaze) // Call API for solved maze
  mazeCanvas.loading = false
  mazeCanvas.solveMaze(solvedMaze) // Solve the maze

  mazeStatus.innerText = `Solved in ${ Math.round(solvedMaze.time_elapsed_ms) } ms.`
}
/**
 * @desc Resets the maze to default.
 */
document.getElementById('btn__reset').onclick = () => {
  if (mazeCanvas.solving) mazeCanvas.cancelSolve() // If maze is being solved, cancel the solve
  mazeCanvas.resetMaze()
  mazeCanvas.loadMaze(basicMaze)
  mazeStatus.innerText = ''
}
/**
 * @desc Scrambles the maze
 */
document.getElementById('btn__scramble').onclick = async () => {
  if (mazeCanvas.solving) {
    // Stop solving
    mazeCanvas.cancelSolve()
  }
  
  mazeCanvas.resetMaze() // Clear solve
  mazeCanvas.loading = true
  const randomMaze = await getRandomMaze(9)
  mazeCanvas.loading = false
  mazeCanvas.loadMaze(randomMaze)
  mazeStatus.innerText = ''
}