"""
This program makes a maze using command-line interface.
"""

import random
from interface import MazeCli, MazePygame

EMPTY = ' '

class Maze(object):
    """
    Create a maze instance from a string of x's and spaces which define the walls (x's)
    and hallways (spaces) of the maze. Print maze to the console and ask user for his
    next move using command-line input. User's current position (.) is updated, and play
    continues until the end ($) is reached.
    """
    moves = {'n': (-1, 0), 's': (1, 0), 'e': (0, 1), 'w': (0, -1)}

    def __init__(self, maze_string, cli, start, finish):
        """
        Create a matrix to store positions of walls and hallways of the maze.
        Initialize user's starting position at a random location.
        """
        self.maze = [list(string) for string in maze_string.splitlines()]
        self.set_interface(cli)
        self.solved = False
        self.start = start
        self.current_pos = None
        self.finish_pos = None
        self.set_starting_pos()
        self.set_finishing_pos(finish)

    def set_interface(self, cli):
        """
        Choose between CLI and pygame interface.
        """
        if cli:
            self.interface = MazeCli()
        else:
            self.interface = MazePygame(self)

    def set_starting_pos(self):
        """
        Move the player to the starting position given.
        """
        if self.start and self.is_unoccupied(*self.start):
            self.current_pos = self.start[:]
        else:
            self.set_random_pos('starting')

    def set_finishing_pos(self, finish):
        """
        Set the finishing position to the chosen location.
        """
        if finish and self.is_unoccupied(*finish):
            self.finish_pos = finish[:]
        else:
            self.set_random_pos('finishing')

    def is_unoccupied(self, row, col):
        """
        Return True if the selected square is a hallway.
        """
        return self.maze[row][col] is EMPTY

    def set_random_pos(self, which):
        """
        Set the current position to a random (legal) location.
        """
        available = [[r, c] for r, row in enumerate(self.maze)
                     for c, value in enumerate(row) if value == ' ']
        choice = random.choice(available)
        if which == 'starting':
            self.current_pos = choice
        elif which == 'finishing':
            self.finish_pos = choice

    def game_loop(self):
        """
        Show map, ask user for his next move, and update position.
        Repeat until end is reached.
        """
        self.interface.game_loop(self)

    def update_pos(self, move):
        """
        Use the supplied move to update the user's current position.
        """
        change = Maze.moves[move]
        self.current_pos[0] += change[0]
        self.current_pos[1] += change[1]

    def is_solved(self):
        """
        Check if player has reached the goal.
        """
        self.solved = self.current_pos == self.finish_pos
        return self.solved

    def restart(self):
        """
        Move current position back to the start, and begin game loop again.
        """
        self.set_random_pos('starting')
        self.set_random_pos('finishing')
        self.game_loop()

    def get_available_moves(self):
        """
        Return a list of legal moves (neighbors that are not walls).
        """
        available = []
        row, col = tuple(self.current_pos)
        if row - 1 >= 0 and self.maze[row - 1][col] != 'x':
            available.append('n')
        if row + 1 < len(self.maze) and self.maze[row + 1][col] != 'x':
            available.append('s')
        if col - 1 >= 0 and self.maze[row][col - 1] != 'x':
            available.append('w')
        if col + 1 < len(self.maze[row]) and self.maze[row][col + 1] != 'x':
            available.append('e')
        return available

def parse_seq(seq, mini=2, maxi=2):
    """
    Convert a comma-separated string of values into a list.
    """
    if seq is None:
        return seq
    output = seq.split(',')
    assert mini <= len(output) and len(output) <= maxi
    return [int(i) for i in output]

def run():
    """
    Parse the command-line arguments and run the program accordingly.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Create and solve mazes")
    parser.add_argument("-c", "--cli", help="Switch to CLI mode", action='store_true')
    parser.add_argument("-f", "--file", help="File to import map from")
    parser.add_argument("-s", "--start", help="Starting position in the maze")
    parser.add_argument("-e", "--end", help="Ending position in the maze")
    args = parser.parse_args()
    if args.file:
        myfile = args.file
    else:
        myfile = 'map1.txt'
    with open(myfile, 'r') as mapfile:
        maze_str = mapfile.read()
    maze = Maze(maze_str, cli=args.cli, start=parse_seq(args.start), finish=parse_seq(args.end))
    maze.game_loop()

if __name__ == '__main__':
    run()
    