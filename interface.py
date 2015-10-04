"""
Implements user interfaces for a maze game.
MazeCli is a command-line interface.
MazePygame is a gui interface using Pygame.
"""

from __future__ import division
import pygame as pg
import config as cfg

KEYMAPS = {pg.K_DOWN: 's', pg.K_UP: 'n', pg.K_LEFT: 'w', pg.K_RIGHT: 'e'}

class MazeCli(object):
    """
    Command-line interface for maze game.
    """
    def __init__(self):
        pass

    def game_loop(self, game):
        """
        Get move from command-line input.
        Update and print the game board.
        """
        while not game.is_solved():
            self.show_status(game)
            move = self.get_next_move(game)
            game.update_pos(move)
        self.show_status(game)
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
            if choice == 'quit':
                quit()
        return choice

    def show_status(self, game):
        """
        Print the map.
        """
        print
        for row, rowlist in enumerate(game.maze):
            print
            for col, value in enumerate(rowlist):
                if game.current_pos == [row, col]:
                    print cfg.PLAYER_CHAR,
                elif game.finish_pos == [row, col]:
                    print cfg.FINISH_CHAR,
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

class MazePygame(object):
    """
    Pygame GUI interface for a maze game.
    """
    def __init__(self, game):
        pg.init()
        size = (cfg.WIDTH, cfg.HEIGHT)
        self.screen = pg.display.set_mode(size)
        pg.display.set_caption(cfg.GAME_TITLE)
        self.clock = pg.time.Clock()
        self.done = False
        self.playing = False
        self.message = cfg.WELCOME_MESSAGE
        self.font = pg.font.SysFont(cfg.TEXT_FONT, cfg.TEXT_SIZE, False, False)
        self.square_width = cfg.WIDTH / max([len(row) for row in game.maze])
        self.square_height = cfg.HEIGHT / len(game.maze)

    def game_loop(self, game):
        """
        Draw the game board and wait for player movements.
        Display welcome message between games.
        """
        while not self.done:
            if self.playing:
                self.screen.fill(cfg.HALLWAY_COLOR)
                self.get_game_input(game)
                self.draw(game)
            else:
                self.get_intro_input(game)
                text = self.font.render(self.message, True, cfg.TEXT_COLOR)
                xval = cfg.WIDTH / 2 - text.get_rect().width / 2
                yval = cfg.HEIGHT / 2 - text.get_rect().height / 2
                self.screen.blit(text, [xval, yval])
            pg.display.flip()
            self.clock.tick(cfg.FRAME_RATE)
        pg.quit()

    def get_game_input(self, game):
        """
        If an arrow key is pressed, move the player in that direction.
        """
        available_moves = game.get_available_moves()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                for key, value in KEYMAPS.items():
                    if event.key == key and value in available_moves:
                        game.update_pos(value)
                        self.playing = not game.is_solved()

    def get_intro_input(self, game):
        """
        If ENTER is pressed, start a new game with random positions.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.playing = True
                    self.message = cfg.FINISH_MESSAGE
                    game.restart()

    def draw(self, game):
        """
        draw the board, the player, and finish line.
        """
        self.draw_squares(game)
        self.draw_finish(game)
        self.draw_player(game)

    def draw_player(self, game):
        """
        draw the player at the appropriate place on the board.
        """
        row, col = game.current_pos
        xval = col * self.square_width
        yval = row * self.square_height
        pg.draw.ellipse(self.screen, cfg.PLAYER_COLOR,
                        [xval, yval, self.square_width, self.square_height])

    def draw_finish(self, game):
        """
        draw the finish line at the appropriate place on the board.
        """
        row, col = game.finish_pos
        xval = col * self.square_width
        yval = row * self.square_height
        pg.draw.ellipse(self.screen, cfg.FINISH_COLOR,
                        [xval, yval, self.square_width, self.square_height])

    def draw_squares(self, game):
        """
        Iterate through each square of the grid, and draw it if it is a wall.
        """
        for row, rowlist in enumerate(game.maze):
            for col, value in enumerate(rowlist):
                xval = col * self.square_width
                yval = row * self.square_height
                if value == cfg.WALL_CHAR:
                    pg.draw.rect(self.screen, cfg.WALL_COLOR,
                                 [xval, yval, self.square_width,
                                  self.square_height])
