from __future__ import division
import pygame as pg
from config import *


class MazeCli:
    def gameLoop(self, game):
        while not game.isSolved():
            self._show_status(game)
            move = self._get_next_move(game)
            game._update_pos(move)
        self._show_status(game)
        self.end(game)

    def _get_next_move(self, game):
        """
        Get available (legal) moves, and ask user which one to make.
        """
        available_moves = game._get_available_moves()
        prompt = '\nChoose a direction ({}) or quit: '.format(','.join(available_moves))
        choice = None
        while choice not in available_moves:
            choice = raw_input(prompt)
            if choice == 'quit': quit()
        return choice

    def _show_status(self, game):
        """
        Print the map.
        """
        print
        for r, row in enumerate(game.maze):
            print
            for c, value in enumerate(row):
                if game.current_pos == [r, c]:
                    print '@',
                elif game.finish_pos == [r, c]:
                    print '$',
                else:
                    print value,
        print

    def end(self, game):
        """
        Notify the user that they have finished. Ask if they want to play again.
        """
        print '\nCongratulations! You made it to the finish!'
        replay = None
        while replay not in ['y', 'n']:
            replay = raw_input('Play again? (y, n): ')
        if replay == 'y':
            game.restart()
        else:
            quit()

class MazePygame:
    keymaps = {pg.K_DOWN: 's', pg.K_UP: 'n', pg.K_LEFT: 'w', pg.K_RIGHT: 'e'}

    def __init__(self):
        pg.init()
        size = (WIDTH, HEIGHT)
        self.screen = pg.display.set_mode(size)
        pg.display.set_caption("Maze!")
        self.clock = pg.time.Clock()
        self.done = False

    def gameLoop(self, game):
        while not self.done:
            self._get_input(game)
            self._draw(game)
            pg.display.flip()
            self.clock.tick(FRAME_RATE)
        pg.quit()

    def _get_input(self, game):
        available_moves = game._get_available_moves()
        for event in pg.event.get(): # User did something
            if event.type == pg.QUIT: # If user clicked close
                self.done = True # Flag that we are done so we exit this loop
            elif event.type == pg.KEYDOWN:
                for key, value in MazePygame.keymaps.items():
                    if event.key == key and value in available_moves:
                        game._update_pos(value)
        self.done = game.isSolved()

    def _draw(self, game):
        self.screen.fill(BLACK)
        self.draw_squares(game)
        self.draw_finish(game)
        self.draw_player(game)

    def draw_player(self, game):
        r, c = tuple(game.current_pos)
        width = WIDTH / len(game.maze[0])
        height = HEIGHT / len(game.maze)
        x = c * width
        y = r * height
        pg.draw.ellipse(self.screen, PLAYER_COLOR, [x, y, width, height])

    def draw_finish(self, game):
        r, c = tuple(game.finish_pos)
        width = WIDTH / len(game.maze[0])
        height = HEIGHT / len(game.maze)
        x = c * width
        y = r * height
        pg.draw.ellipse(self.screen, FINISH_COLOR, [x, y, width, height])

    def draw_squares(self, game):
        for r, row in enumerate(game.maze):
            for c, value in enumerate(row):
                width = WIDTH / len(game.maze[0])
                height = HEIGHT / len(game.maze)
                x = c * width
                y = r * height
                if value == 'x':
                    pg.draw.rect(self.screen, WALL_COLOR, [x, y, width, height])
                elif value == ' ':
                    pg.draw.rect(self.screen, HALLWAY_COLOR, [x, y, width, height])
