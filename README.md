# Fifteen Puzzle Solver
I programmed this 15 Puzzle solver in Python using A* algorithm to learn how A* works.

## A* Algorithm
A* algorithm is a pathfinding algorithm used on weighted graphs to find the shortest path given a starting node and a goal node. It extends Dijkstra’s algorithm with a best-first search by adding heuristics. The heuristic for any given board state of the 15 puzzle is found by counting how many spaces each tile is from its goal position.

While with Dijkstra’s algorithm we get the next node from the list with the shortest path to the starting node, with A* algorithm, we get the next node from the list that has the smallest combined distance from the starting node and estimated distance to the goal. With A* algorithm, the paths that are closer to the goal are prioritized, so not all the paths shorter than the shortest path to the goal node need to be explored before the shortest path to the goal can be found.

## 15 Puzzle
The puzzle consists of 15 numbered square tiles in a 4 by 4 frame, leaving 1 blank space. The goal of the puzzle is to move the board from its starting state to a goal state. Any adjacent square tile can slide freely along its row or column into the empty space to create a new board state.

## Implementation
This program creates a random board then prints out the shortest path that was found. For this solver, the goal board is assumed to be the tiles in numeric order. The starting board is a random board state found by randomly moving tiles from the solved board state. By generating the starting board in this way, the starting board can safely be assumed to be solvable. 
