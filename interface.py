

class MazeCli:
    def gameLoop(self, game):
        game.check_if_solved()
        while not game.solved:
            self._show_status(game)
            move = self._get_next_move(game)
            game._update_pos(move)
            game.check_if_solved()
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
