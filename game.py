import pygame


class Connect4:
    def __init__(self, board_width, board_height):
        '''Setup method that is called, when Connect4 object is created.'''
        # Create board using generate_grid_dict method with given width and height.
        board = self.generate_grid_dict(board_width, board_height)

        pygame.init()

        # set the screen size, gridsize and chipsize (radius)
        self.square_size = 80
        self.width = board_width * self.square_size
        self.height = board_height * self.square_size
        self.radius = int(self.square_size / 4)
        self.square_mid = int(self.square_size / 2)
        self.screen = pygame.display.set_mode((self.width, self.height))

        # fill the screen with a white background
        background = pygame.Surface(self.screen.get_size())
        background.fill((255, 255, 255))
        self.background = background.convert()

        # build the grid
        for i in range(0, self.width, self.square_size):
            pygame.draw.rect(self.background, (0, 0, 0), (i, 0, 0, self.width))
            pygame.draw.rect(self.background, (0, 0, 0), (0, i, self.width, 0))
        self.screen.blit(self.background, (0, 0))

        # Setup, so player one starts
        self.playerOne = True
        self.red = 250
        self.blue = 0

        # Help dict for logic, when drawing a chip. Maps 0 -> size, 1 -> size - 1...
        self.draw_dict_mapping = {}
        for i in range(self.height//80 + 1):
            self.draw_dict_mapping[i] = self.height//80 - i

        self.run_game(board)

    @staticmethod
    def generate_grid_dict(height, width):
        '''Method, which generates the board with a given size'''
        board = {}
        for i in range(height):
            for j in range(width):
                position = (i, j)
                board[position] = 0
        return board

    def run_game(self, board):
        '''Main method which starts the game when called'''
        # start program
        run_program = True

        while run_program:
            for event in pygame.event.get():
                if pygame.mouse.get_pressed() and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # get position of mouse
                        (x, y) = pygame.mouse.get_pos()

                        # set circle position in the middle of the gridsquare
                        draw_x = x - (x % self.square_size) + self.square_mid

                        # Calculation to get xPosition from selected Mouse xPosition (480 -> 6)
                        x = x // 80

                        # Check if column is full before placing. Break out if that's the case.
                        if self.check_if_column_full(board, x):
                            break

                        # Calculate the yPosition, where the chip should be placed with various helper methods
                        draw_y = self.height - (self.square_size * self.draw_dict_mapping[self.get_y_pos(board, x)]) + 40

                        # Check, which players turn it is
                        if self.playerOne:
                            # Player Ones turn
                            pos = (x, self.get_y_pos(board, x))
                            if board[pos] == 0:
                                board[pos] = 1
                                self.draw_circle(draw_x, draw_y, self.playerOne)
                                self.screen.blit(self.background, (0, 0))
                                self.check_if_user_won(board, pos, 1)
                                self.switch_player()
                        else:
                            # Player Twos turn
                            pos = (x, self.get_y_pos(board, x))
                            if board[pos] == 0:
                                board[pos] = 2
                                self.draw_circle(draw_x, draw_y, self.playerOne)
                                self.screen.blit(self.background, (0, 0))
                                self.check_if_user_won(board, pos, 2)
                                self.switch_player()



                if event.type == pygame.KEYDOWN:
                    # end the game with escape
                    if event.key == pygame.K_ESCAPE:
                        run_program = False

                # end the Programm with the X in the upper right corner
                elif event.type == pygame.QUIT:
                    run_program = False

            pygame.display.flip()
        pygame.quit()

    def switch_player(self):
        '''Switches between player One and Two'''
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
            if self.check_pos(board, x, i):
                return i
            i -= 1
            pass

    def check_pos(self, board, x, i):
        '''Help method to check, whether a selected position is occupied'''
        if board[(int(x), int(i))] == 0:
            return True
        else:
            return False

    def check_if_column_full(self, board, x):
        '''Help method which checks, whether a given column is already full to prevent people placing chips outside of the visible field'''
        for y in reversed(range(self.height // 80)):
            if board[x, 0] != 0:
                return True
            elif board[(x, y)] == 0:
                return False
            else:
                y -= y
                continue

    def check_if_user_won(self, board, pos, player_no):
        '''Logic which first, checks if a player has 4 in a row after putting in a chip at the given position. If that's not the case it will check, if the board is full'''

        has_player_got_4 = set()
        has_player_got_4.add(pos)

        self.check_horizontal(has_player_got_4, board, pos, player_no)

        if len(has_player_got_4) >= 4:
            self.game_over(player_no)

        has_player_got_4 = set()
        has_player_got_4.add(pos)

        self.check_vertical(has_player_got_4, board, pos, player_no)

        if len(has_player_got_4) >= 4:
            self.game_over(player_no)

        has_player_got_4 = set()
        has_player_got_4.add(pos)

        self.check_diagonal(has_player_got_4, board, pos, player_no)

        if len(has_player_got_4) >= 4:
            self.game_over(player_no)

        has_player_got_4 = set()
        has_player_got_4.add(pos)

        self.check_inverted_diagonal(has_player_got_4, board, pos, player_no)

        if len(has_player_got_4) >= 4:
            self.game_over(player_no)

        self.check_if_board_full(board)

    def check_horizontal(self, has4_set, board, pos, player_no):
        '''Checks from left to right'''
        for i in range(1, 4):
            if pos[0] - i >= 0:
                if board[(pos[0] - i, pos[1])] == player_no:
                    has4_set.add((pos[0] - i, pos[1]))
                    print("Added left: " + str((pos[0] - i, pos[1])))
                else:
                    break
        for i in range(1, 4):
            if pos[0] + i < self.width // 80:
                if board[(pos[0] + i, pos[1])] == player_no:
                    has4_set.add((pos[0] + i, pos[1]))
                    print("Added right: " + str((pos[0] + i, pos[1])))
                else:
                    break

    def check_vertical(self, has4_set, board, pos, player_no):
        '''Checks under the placed chip'''
        for i in range(1,4):
            if pos[1] + i < self.height//80:
                if board[(pos[0], pos[1] + i)] == player_no:
                    has4_set.add((pos[0], pos[1] + i))
                    print("Added down: " + str((pos[0], pos[1] + i)))
                else:
                    break

    def check_diagonal(self, has4_set, board, pos, player_no):
        '''Checks bottom-left to top-right'''
        for i in range(1, 4):
            if pos[0] + i < self.height // 80 and pos[1] - i >= 0:
                if board[(pos[0] + i, pos[1] - i)] == player_no:
                    has4_set.add((pos[0] + i, pos[1] - i))
                    print("Added top-right: " + str((pos[0] + i, pos[1] - i)))
                else:
                    break
        for i in range(1, 4):
            if (self.height // 80 > pos[1] + i >= 0) and pos[0] - i >= 0:
                if board[(pos[0] - i, pos[1] + i)] == player_no:
                    has4_set.add((pos[0] - i, pos[1] + i))
                    print("Added bottom-left: " + str((pos[0] - i, pos[1] + i)))
                else:
                    break

    def check_inverted_diagonal(self, has4_set, board, pos, player_no):
        '''Checks top-left to bottom right'''
        for i in range(1, 4):
            if (self.height // 80 > pos[1] - i >= 0) and pos[0] - i >= 0:
                if board[(pos[0] - i, pos[1] - i)] == player_no:
                    has4_set.add((pos[0] - i, pos[1] - i))
                    print("Added top-left: " + str((pos[0] - i, pos[1] - i)))
                else:
                    break
        for i in range(1, 4):
            if (self.height // 80 > pos[1] + i >= 0) and pos[0] + i < self.width // 80:
                if board[(pos[0] + i, pos[1] + i)] == player_no:
                    has4_set.add((pos[0] + i, pos[1] + i))
                    print("Added bottom-right: " + str((pos[0] + i, pos[1] + i)))
                else:
                    break

    def check_if_board_full(self, board):
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

    def draw_circle(self, draw_x, draw_y, player_one):
        '''Help method which either draws a red or blue circle at the given position, depending on the player'''
        if player_one:
            pygame.draw.circle(self.background, (0, 0, 0), (draw_x, draw_y), self.radius + 1)
            pygame.draw.circle(self.background, (self.red, 0, self.blue), (draw_x, draw_y), self.radius)
            pygame.draw.circle(self.background, (self.red, 100, self.blue + 100), (draw_x, draw_y), self.radius - 8)
        else:
            pygame.draw.circle(self.background, (0, 0, 0), (draw_x, draw_y), self.radius + 1)
            pygame.draw.circle(self.background, (self.red, 0, self.blue), (draw_x, draw_y), self.radius)
            pygame.draw.circle(self.background, (self.red + 100, 100, self.blue), (draw_x, draw_y), self.radius - 8)

    def game_over(self, player_no: int):
        '''Method that is called, when a player has 4 in a row or the board is full.'''
        print("Player {} wins!".format(player_no))


Connect4(8, 6)
