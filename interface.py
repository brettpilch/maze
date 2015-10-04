from __future__ import division
import pygame as pg
from config import *


class MazeCli:
    def gameLoop(self, game):
        while not game.isSolved():
            self.show_status(game)
            move = self.get_next_move(game)
            game.update_pos(move)
        self._show_status(game)
        self.end(game)

    def get_next_move(self, game):
        """
        Get available (legal) moves, and ask user which one to make.
        """
        available_moves = game.get_available_moves()
        prompt = '\nChoose a direction ({}) or quit: '.format(
            ','.join(available_moves))
        choice = None
        while choice not in available_moves:
            choice = raw_input(prompt)
            if choice == 'quit': quit()
        return choice

    def show_status(self, game):
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
        Notify the user that they have finished.
        Ask if they want to play again.
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

    def __init__(self, game):
        pg.init()
        size = (WIDTH, HEIGHT)
        self.screen = pg.display.set_mode(size)
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()
        self.done = False
        self.playing = False
        self.message = WELCOME_MESSAGE
        self.font = pg.font.SysFont(TEXT_FONT, TEXT_SIZE, False, False)
        self.square_width = WIDTH / max(map(len,game.maze))
        self.square_height = HEIGHT / len(game.maze)

    def gameLoop(self, game):
        while not self.done:
            if self.playing:
                self.screen.fill(HALLWAY_COLOR)
                self.get_game_input(game)
                self.draw(game)
            else:
                self.get_intro_input(game)
                text = self.font.render(self.message, True, TEXT_COLOR)
                self.screen.blit(text, [WIDTH / 2 - text.get_rect().width / 2,
                    HEIGHT / 2 - text.get_rect().height / 2])
            pg.display.flip()
            self.clock.tick(FRAME_RATE)
        pg.quit()

    def get_game_input(self, game):
        available_moves = game.get_available_moves()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                for key, value in MazePygame.keymaps.items():
                    if event.key == key and value in available_moves:
                        game.update_pos(value)
                        self.playing = not game.isSolved()

    def get_intro_input(self, game):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.playing = True
                    self.message = FINISH_MESSAGE
                    game.restart()

    def draw(self, game):
        self.draw_squares(game)
        self.draw_finish(game)
        self.draw_player(game)

    def draw_player(self, game):
        r, c = game.current_pos
        x = c * self.square_width
        y = r * self.square_height
        pg.draw.ellipse(self.screen, PLAYER_COLOR,
            [x, y, self.square_width, self.square_height])

    def draw_finish(self, game):
        r, c = game.finish_pos
        x = c * self.square_width
        y = r * self.square_height
        pg.draw.ellipse(self.screen, FINISH_COLOR,
            [x, y, self.square_width, self.square_height])

    def draw_squares(self, game):
        for r, row in enumerate(game.maze):
            for c, value in enumerate(row):
                x = c * self.square_width
                y = r * self.square_height
                if value == WALL_CHAR:
                    pg.draw.rect(self.screen, WALL_COLOR,
                        [x, y, self.square_width, self.square_height])
