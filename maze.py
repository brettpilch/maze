"""
This program makes a maze using command-line interface.
"""

import random

# A small sample maze (used as input to the Maze class):
maze_str = """  x   
x   x 
  xx  
 x  xx
  x   
x   x$
"""

class Maze():
    """
    Create a maze instance from a string of x's and spaces which define the walls (x's)
    and hallways (spaces) of the maze. Print maze to the console and ask user for his
    next move using command-line input. User's current position (.) is updated, and play
    continues until the end ($) is reached.
    """
    moves = {'n': (-1, 0), 's': (1, 0), 'e': (0, 1), 'w': (0, -1)}

    def __init__(self, maze_str):
        """
        Create a matrix to store positions of walls and hallways of the maze.
        Initialize user's starting position at a random location.
        """
        self.maze = [list(string) for string in maze_str.splitlines()]
        self.solved = False
        self.setRandomPos()

    def setRandomPos(self):
        """
        Set the current position to a random (legal) location.
        """
        available = [[r,c] for r, row in enumerate(self.maze) for c, value in enumerate(row) if value == ' ']
        self.current_pos = random.choice(available)

    def begin(self):
        """
        Show map, ask user for his next move, and update position.
        Repeat until end is reached.
        """
        while not self.solved:
            self._show_status()
            move = self._get_next_move()
            self._update_pos(move)
        self._show_status()
        self.end()

    def end(self):
        """
        Notify the user that they have finished. Ask if they want to play again.
        """
        print '\nCongratulations! You made it to the finish!'
        replay = None
        while replay not in ['y', 'n']:
            replay = raw_input('Play again? (y, n): ')
        if replay == 'y':
            self.restart()
        else:
            quit()

    def restart(self):
        """
        Move current position back to the start, and begin game loop again.
        """
        self.setRandomPos()
        self.solved = False
        self.begin()

    def _get_next_move(self):
        """
        Get available (legal) moves, and ask user which one to make.
        """
        available_moves = self._get_available_moves()
        prompt = '\nChoose a direction ({}) or quit: '.format(','.join(available_moves))
        choice = None
        while choice not in available_moves:
            choice = raw_input(prompt)
            if choice == 'quit': quit()
        return choice

    def _show_status(self):
        """
        Print the map.
        """
        print
        for r, row in enumerate(self.maze):
            print
            for c, value in enumerate(row):
                if self.current_pos == [r, c]:
                    print '@',
                else:
                    print value,
        print

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
    maze = Maze(maze_str)
    maze.begin()

