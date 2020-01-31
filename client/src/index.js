import('../styles/reset.scss')
import('../styles/main.scss')

import MazeCanvas from 'maze-canvas'
import { getRandomMaze, solveMaze } from './api'

let mazeDimensions, canvasMaxWidth, basicMaze, solveSpeed
if (window.location.pathname === '/editor.html') { // Editor version
  let width = 60
  
  let cellSize = window.innerWidth/width // PX in width & height for cell
  let height = Math.round((window.innerHeight-cellSize*2)/cellSize) // Height of cells

  mazeDimensions = [width, height]
  canvasMaxWidth = window.innerWidth
  solveSpeed = 10
  basicMaze = [['O', 'X']]
} else { // Display version
  mazeDimensions = [9,9]
  canvasMaxWidth = 600
  solveSpeed = 50

  // Starting maze
  basicMaze = [
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
}

const mazeCanvas = new MazeCanvas("maze-canvas", {
  mazeDimensions,
  canvasMaxWidth,
  solveSpeed
})


mazeCanvas.loadMaze(basicMaze)

// DOM Elements
const mazeStatus = document.getElementById('maze__status') // <p> that displays maze status

// Button controllers

/**
 * @desc Calls the API to solve the current maze and visually represents it on the maze canvas
 */
document.getElementById('btn__solve').onclick = async () => {
  if (mazeCanvas.solved) return // Only solve if not already solving!
  
  const currentMaze = mazeCanvas.getMazeStringArray() // Current maze string array
  let selector = document.getElementById('select__algorithm')
  const algorithm = selector.options[selector.selectedIndex].value // selected algorithm

  mazeCanvas.loading = true
  const solvedMaze = await solveMaze(algorithm, currentMaze) // Call API for solved maze

  // If the maze does not have an error (timeout or impossible) then visualize the solve
  if (!solvedMaze.error) mazeCanvas.solveMaze(solvedMaze) // Solve the maze

  mazeCanvas.loading = false
  setStatus(solvedMaze) // set maze status
}
/**
 * @desc Resets the maze to default.
 */
document.getElementById('btn__reset').onclick = () => {
  if (mazeCanvas.solved) mazeCanvas.cancelSolve() // If maze is being solved, cancel the solve
  mazeCanvas.resetMaze()
  mazeCanvas.loadMaze(basicMaze)
  
  clearStatus() // Clear maze status
}
/**
 * @desc Scrambles the maze
 */
document.getElementById('btn__scramble').onclick = async () => {
  if (mazeCanvas.solved) {
    // Stop solving
    mazeCanvas.cancelSolve()
  }
  
  mazeCanvas.resetMaze() // Clear solve
  mazeCanvas.loading = true
  const randomMaze = await getRandomMaze(9)
  mazeCanvas.loading = false
  mazeCanvas.loadMaze(randomMaze)

  clearStatus() // clear maze status
}

/**
 * @desc Sets the maze status with the current solution's info
 * @param { object } solutionInfo 
 */
function setStatus(solutionInfo) {
  if (solutionInfo.error) {
    mazeStatus.innerText = `Error! ${ solutionInfo.error }`
  } else {
    mazeStatus.innerText = `Solved in ${ Math.round(solutionInfo.time_elapsed_ms) } ms. Tried ${ solutionInfo.paths_tried } paths. Shortest path is ${ solutionInfo.shortest_path.length } cells.`
  }
}

/**
 * @desc Clears the maze's status.
 */
function clearStatus() {
  mazeStatus.innerText = ''
}