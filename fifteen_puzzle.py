# fifteen_puzzle.py
# Solves the 15 Puzzle using A* algorithm
# 4x4 grid
# By Joseph Miller


import heapq
import random

class Node:
    def __init__(self, board, shortest_path_length, previous_node = None):
        self.board = board
        self.shortest_path_length = shortest_path_length
        self.previous_node = previous_node

    def __lt__(self, other):
        self_value = self.shortest_path_length + self.board.min_moves()
        other_value = other.shortest_path_length + other.board.min_moves()
        return self_value < other_value

class Board:
    GOAL = ((1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,0))
    ROWS = 4
    COLS = 4

    def __init__(self, board = GOAL):
        self.board = board

    def __str__(self):
        board_str = ""
        for row in self.board:
            for col in row:
                board_str += f"{col:>{3}}"
            board_str += '\n'
        return f"{board_str}"

    def min_moves(self):
        goal_coord = [
        (3,3),(0,0),(0,1),(0,2),(0,3),
        (1,0),(1,1),(1,2),(1,3),
        (2,0),(2,1),(2,2),(2,3),
        (3,0),(3,1),(3,2)
        ]
        coords = self.get_coords()
        moves = 0;
        for i in range(len(coords)):
            moves += abs(coords[i][0] - goal_coord[i][0])
            moves += abs(coords[i][1] - goal_coord[i][1])
        return moves

    def get_coords(self):
        coords = [(r,c) for c in range(self.COLS) for r in range(self.ROWS)]
        for row in range(self.ROWS):
            for col in range(self.COLS):
                element = self.board[row][col]
                coords[element] = (row, col)
        return coords

    def get_neighbors(self):
        neighbors = []
        # find the empty space
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.board[row][col] == 0:
                    blank_row = row
                    blank_col = col
        blank_coordinates = (blank_row, blank_col)
        # up 
        if blank_row > 0:
            row = blank_row - 1
            col = blank_col 
            new_board = self.swap((row, col), blank_coordinates)
            neighbors.append(new_board)
        # down
        if blank_row < self.ROWS - 1:
            row = blank_row + 1
            col = blank_col 
            new_board = self.swap((row, col), blank_coordinates)
            neighbors.append(new_board)
        # left 
        if blank_col > 0:
            row = blank_row
            col = blank_col - 1
            new_board = self.swap((row, col), blank_coordinates)
            neighbors.append(new_board)
        # right
        if blank_col < self.COLS - 1:
            row = blank_row
            col = blank_col + 1
            new_board = self.swap((row, col), blank_coordinates)
            neighbors.append(new_board)
        return neighbors

    def swap(self, element_coordinates, blank_coordinates):
        new_board = []
        element_row, element_col = element_coordinates
        element = self.board[element_row][element_col]
        blank_row, blank_col = blank_coordinates
        for row in range(self.ROWS):
            new_row = []
            for col in range(self.COLS):
                if row == blank_row and col == blank_col:
                    new_row.append(element)
                elif row == element_row and col == element_col:
                    new_row.append(0)
                else:
                    new_row.append(self.board[row][col])
            new_board.append(new_row)
        # convert to nested tuples
        row1 = (new_board[0][0], new_board[0][1], new_board[0][2], new_board[0][3])
        row2 = (new_board[1][0], new_board[1][1], new_board[1][2], new_board[1][3])
        row3 = (new_board[2][0], new_board[2][1], new_board[2][2], new_board[2][3])
        row4 = (new_board[3][0], new_board[3][1], new_board[3][2], new_board[3][3])
        tuple_board = (row1, row2, row3, row4)
        return tuple_board

    def solve(self):
        visited = []
        unvisited = []
        path_length = 0
        start_node = Node(self, path_length)
        heapq.heappush(unvisited, start_node)
        shortest_paths = {self: start_node}
        is_solved = False
        previous_node = None
        boards_checked = 0
        # Search until unvisited list is empty or goal board is found
        while len(unvisited) > 0:
            # visit the unvisited node with the shortest path length first
            node = heapq.heappop(unvisited)
            visited.append(node.board.board)
            boards_checked += 1
            # check neighbors not already visited
            neighbors = node.board.get_neighbors()
            for neighbor_board in neighbors:
                if neighbor_board not in visited:
                    neighbor = Board(neighbor_board)
                    path_length = node.shortest_path_length + 1
                    neighbor_node = Node(neighbor, path_length, node)
                    # put neigbors into list in order of smallest path
                    heapq.heappush(unvisited, neighbor_node)
                    shortest_paths[neighbor_node.board] = neighbor_node
            # Puzzle solved once goal board has been visited
            if self.GOAL in visited:
                is_solved = True
                break
        # don't return shortest paths if solution was not found
        if is_solved:
            goal_node = None
            # find the goal node
            for board in shortest_paths.keys():
                if board.board == self.GOAL:
                    goal_node = shortest_paths[board]
        # return all the goal node
        return (goal_node, boards_checked)

    def scramble(self, moves = 1):
        # get neighbors
        neighbors = self.get_neighbors()
        # pick random neighbor to set board to
        self.board = random.choice(neighbors)
        # if moves remaining, scramble again
        moves -= 1
        if moves > 0:
            self.scramble(moves)

if __name__ == '__main__':
    board = Board()
    board.scramble(20)
    print(board)
    # the miniumum moves are double counted (each swap is 2 moves)
    print("Min Moves:", int(board.min_moves()/2))

    goal_node, boards_checked = board.solve()
    print(f"Boards Checked: {boards_checked}")
    if goal_node:
        node = goal_node
        solved_path = []
        while node.previous_node:
            solved_path.append(node.board)
            node = node.previous_node
        solved_path.append(node.board)
        l = len(solved_path)
        print("Swaps: ", l-1)
        print("Shortest Solution Path:")
        for i in range(l):
            print(solved_path[(l-1) - i])
    else:
        print("Unsolvable")
    

