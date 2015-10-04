"""
This program makes a maze using command-line interface.
"""

import random
from interface import MazeCli, MazePygame

# A small sample maze (used as input to the Maze class):
maze_str = """  x   
x   x 
  xx  
 x  xx
  x   
x   x 
"""

EMPTY = ' '

class Maze:
    """
    Create a maze instance from a string of x's and spaces which define the walls (x's)
    and hallways (spaces) of the maze. Print maze to the console and ask user for his
    next move using command-line input. User's current position (.) is updated, and play
    continues until the end ($) is reached.
    """
    moves = {'n': (-1, 0), 's': (1, 0), 'e': (0, 1), 'w': (0, -1)}

    def __init__(self, maze_str, cli, start, finish):
        """
        Create a matrix to store positions of walls and hallways of the maze.
        Initialize user's starting position at a random location.
        """
        self.maze = [list(string) for string in maze_str.splitlines()]
        self.setInterface(cli)
        self.solved = False
        self.start = start
        self.current_pos = None
        self.finish_pos = None
        self.setStartingPos()
        self.setFinishingPos(finish)

    def setInterface(self, isCli):
        if isCli:
            print('using command-line interface')
            self.interface = MazeCli()
        else:
            print('using pygame')
            self.interface = MazePygame(self)

    def setStartingPos(self):
        if self.start and self.isUnoccupied(*self.start):
            self.current_pos = self.start[:]
        else:
            self.setRandomPos('starting')

    def setFinishingPos(self, finish):
        if finish and self.isUnoccupied(*finish):
            self.finish_pos = finish[:]
        else:
            self.setRandomPos('finishing')

    def isUnoccupied(self, row, col):
        return self.maze[row][col] is EMPTY

    def setRandomPos(self, which):
        """
        Set the current position to a random (legal) location.
        """
        available = [[r,c] for r, row in enumerate(self.maze) for c, value in enumerate(row) if value == ' ']
        choice = random.choice(available)
        if which == 'starting':
            self.current_pos = choice
        elif which == 'finishing':
            self.finish_pos = choice

    def gameLoop(self):
        """
        Show map, ask user for his next move, and update position.
        Repeat until end is reached.
        """
        self.interface.gameLoop(self)

    def update_pos(self, move):
        """
        Use the supplied move to update the user's current position.
        """
        change = Maze.moves[move]
        self.current_pos[0] += change[0]
        self.current_pos[1] += change[1]

    def isSolved(self):
        self.solved = self.current_pos == self.finish_pos
        return self.solved

    def restart(self):
        """
        Move current position back to the start, and begin game loop again.
        """
        self.setRandomPos('starting')
        self.setRandomPos('finishing')
        self.gameLoop()

    def get_available_moves(self):
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

def parseSeq(seq, min=2, max=2):
    if seq is None:
        return seq
    output = seq.split(',')
    assert min <= len(output) and len(output) <= max
    return [int(i) for i in output]

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Create and solve mazes")
    parser.add_argument("-c", "--cli", help="Switch to CLI mode", action='store_true')
    parser.add_argument("-f", "--file", help="File to import map from")
    parser.add_argument("-s", "--start", help="Starting position in the maze")
    parser.add_argument("-e", "--end", help="Ending position in the maze")
    args = parser.parse_args()
    if args.file:
        with open(args.file, 'r') as f:
            maze_str = f.read()
    maze = Maze(maze_str, cli=args.cli, start=parseSeq(args.start), finish=parseSeq(args.end))
    maze.gameLoop()

