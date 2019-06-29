import pygame


class Connect4:
    def __init__(self, board_width, board_height):
        print("Setting up the board.")
        board = self.generate_grid_dict(board_width, board_height)

        self.red = 250
        self.blue = 0

        pygame.init()

        # set the screen size, gridsize and chipsize (radius)
        self.squaresize = 80
        self.width = board_width * self.squaresize
        self.height = board_height * self.squaresize
        self.radius = int(self.squaresize / 4)
        self.squaremid = int(self.squaresize / 2)
        self.screen = pygame.display.set_mode((self.width, self.height))

        # fill the screen with a white background
        background = pygame.Surface(self.screen.get_size())
        background.fill((255, 255, 255))
        self.background = background.convert()

        # build the grid
        for i in range(0, self.width, self.squaresize):
            pygame.draw.rect(self.background, (0, 0, 0), (i, 0, 0, self.width))
            pygame.draw.rect(self.background, (0, 0, 0), (0, i, self.width, 0))
        self.screen.blit(self.background, (0, 0))

        self.playerOne = True
        self.run_game(board)

    def generate_grid_dict(self, height, width):
        board = {}
        for i in range(height):
            for j in range(width):
                position = (i, j)
                board[position] = 0
        return board

    def run_game(self, board):
        # start program
        runprogram = True

        while runprogram:
            for event in pygame.event.get():
                if pygame.mouse.get_pressed():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # get position of mouse
                        (x, y) = pygame.mouse.get_pos()

                        # set circle position in the middle of the gridsquare
                        draw_x = x - (x % self.squaresize) + self.squaremid

                        x = x // 80

                        if self.column_is_full(board, x):
                            break

                        square = self.width//80 - self.get_y_pos(board, x) * 2

                        draw_y = self.height - (self.squaremid * (square + 3))

                        if self.playerOne:
                            # Player Ones turn
                            pos = (x, self.get_y_pos(board, x))
                            if pos[1] >= 0:
                                if board[pos] == 0:
                                    board[pos] = 1
                                    pygame.draw.circle(self.background, (self.red, 0, self.blue), (draw_x, draw_y), self.radius)
                                    print("New circle: {}, {}".format(pos[0], pos[1]))
                                    print("Position: " + str(draw_x) + ", " + str(draw_y))
                                    self.screen.blit(self.background, (0, 0))
                                    self.check_if_user_won(board, pos)
                                    self.switch_player()
                        elif not self.playerOne:
                            # Player Twos turn
                            pos = (x, self.get_y_pos(board, x))
                            if board[pos] == 0:
                                board[pos] = 2
                                pygame.draw.circle(self.background, (self.red, 0, self.blue), (draw_x, draw_y), self.radius)
                                print("New circle: {}, {}".format(pos[0], pos[1]))
                                print("Position: " + str(draw_x) + ", " + str(draw_y))
                                self.screen.blit(self.background, (0, 0))
                                self.check_if_user_won(board, pos)
                                self.switch_player()



                if event.type == pygame.KEYDOWN:
                    # end the game with escape
                    if event.key == pygame.K_ESCAPE:
                        runprogram = False

                # end the Programm with the X in the upper right corner
                elif event.type == pygame.QUIT:
                    runprogram = False

            pygame.display.flip()
        pygame.quit()
        # set text at the end of the game
        print("End of Game")

    def switch_player(self):
        '''Switches between player One and Two when function is called'''
        if self.playerOne:
            self.red = 0
            self.blue = 255
            self.playerOne = False
        else:
            self.red = 250
            self.blue = 0
            self.playerOne = True

    def get_y_pos(self, board, x):
        '''Get available/free yPos at selected xPos'''
        for i in reversed(range(self.height//80)):
            if(self.check_pos(board, x, i)):
                return i
            i -= 1
            pass

    def check_pos(self, board, x, i):
        '''Help method to check, whether a selected position is occupied'''
        temp = board[(int(x), int(i))]
        if board[(int(x), int(i))] == 0:
            return True
        else:
            return False

    def check_if_board_full(self, board, pos):
        '''Checks if board is full in case of a draw'''
        for i in range(self.height // 80):
            for j in range(self.width // 80):
                if (board[(j, i)] == 0):
                    return
                elif (j == self.width // 80):
                    break
                else:
                    pass

        print("Board full! :(")
        self.game_over(0)

    def check_if_user_won(self, board, pos):
        '''Logic which first, checks if theres a draw to save resources and if not, it will check if a player has 4 in a row.'''
        self.check_if_board_full(board, pos)

        player_has_4 = False
        winner = 0

        # TODO impl. logic

        if player_has_4:
            self.game_over(winner)

    def column_is_full(self, board, x):
        '''Checks, whether a given column is already full to prevent people placing chips outside of the visible field'''
        for y in reversed(range(self.height // 80)):
            if (board[(x, y)] == 0):
                return False
            else:
                y -= y
                continue

            return True

    def game_over(self, player_no: int):
        print("Player {} wins!".format(player_no))



Connect4(8, 6)
