"""
This program makes a maze using command-line interface.
"""

import random
from interface import MazeCli

# A small sample maze (used as input to the Maze class):
maze_str = """  x   
x   x 
  xx  
 x  xx
  x   
x   x$
"""

class Maze:
    """
    Create a maze instance from a string of x's and spaces which define the walls (x's)
    and hallways (spaces) of the maze. Print maze to the console and ask user for his
    next move using command-line input. User's current position (.) is updated, and play
    continues until the end ($) is reached.
    """
    moves = {'n': (-1, 0), 's': (1, 0), 'e': (0, 1), 'w': (0, -1)}

    def __init__(self, maze_str, interface):
        """
        Create a matrix to store positions of walls and hallways of the maze.
        Initialize user's starting position at a random location.
        """
        self.maze = [list(string) for string in maze_str.splitlines()]
        self.setInterface(interface)
        self.solved = False
        self.current_pos = [0, 0]

    def setInterface(self, interface):
        if interface == 'cli':
            self.interface = MazeCli()

    def setRandomPos(self):
        """
        Set the current position to a random (legal) location.
        """
        available = [[r,c] for r, row in enumerate(self.maze) for c, value in enumerate(row) if value == ' ']
        self.current_pos = random.choice(available)

    def gameLoop(self):
        """
        Show map, ask user for his next move, and update position.
        Repeat until end is reached.
        """
        self.interface.gameLoop(self)

    def _update_pos(self, move):
        """
        Use the supplied move to update the user's current position.
        """
        change = Maze.moves[move]
        self.current_pos[0] += change[0]
        self.current_pos[1] += change[1]
        r, c = tuple(self.current_pos)
        if self.maze[r][c] == '$':
            self.solved = True

    def restart(self):
        """
        Move current position back to the start, and begin game loop again.
        """
        self.setRandomPos()
        self.solved = False
        self.gameLoop()

    def _get_available_moves(self):
        """
        Return a list of legal moves (neighbors that are not walls).
        """
        available = []
        r, c = tuple(self.current_pos)
        if r - 1 >= 0 and self.maze[r - 1][c] != 'x':
            available.append('n')
        if r + 1 < len(self.maze) and self.maze[r + 1][c] != 'x':
            available.append('s')
        if c - 1 >= 0 and self.maze[r][c - 1] != 'x':
            available.append('w')
        if c + 1 < len(self.maze[r]) and self.maze[r][c + 1] != 'x':
            available.append('e')
        return available


if __name__ == '__main__':
    maze = Maze(maze_str, 'cli')
    maze.setRandomPos()
    maze.gameLoop()

