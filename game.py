import pygame
import pygame.freetype


class Connect4:
    def __init__(self, board_width, board_height):
        """Setup method that is called, when Connect4 object is created."""
        # Create board using generate_grid_dict method with given width and height.
        board = self.generate_grid_dict(board_width, board_height)
        self.draw = False
        pygame.init()

        # Set the caption for the board and the font for the win prompt.
        pygame.display.set_caption('Connect4 - Player 1')
        self.game_font = pygame.freetype.Font("SF Distant Galaxy.ttf", 40)

        # size of each square of the grid:
        self.square_size = 80
        # generate board width (amount of squares and square width):
        self.width = board_width * self.square_size
        # generate board height (amount of squares and square height):
        self.height = board_height * self.square_size
        # generate the radius of the chips depending on the square size:
        self.radius = int(self.square_size / 4)
        # find the middle of the square for chip placement:
        self.square_mid = int(self.square_size / 2)
        # set the screen size with the board width and height:
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Fill the screen with a white background.
        background = pygame.Surface(self.screen.get_size())
        background.fill((255, 255, 255))
        self.background = background.convert()

        # Build the grid.
        for i in range(0, self.width, self.square_size):
            pygame.draw.rect(self.background, (0, 0, 0), (i, 0, 0, self.height))
        for i in range(0, self.height, self.square_size):
            pygame.draw.rect(self.background, (0, 0, 0), (0, i, self.width, 0))
        self.screen.blit(self.background, (0, 0))

        # Setup, so player one starts.
        self.playerOne = True
        self.red = 250
        self.blue = 0

        # Help dict for logic, when drawing a chip. Maps 0 -> size, 1 -> size - 1...
        self.draw_dict_mapping = {}
        for i in range(self.height//80 + 1):
            self.draw_dict_mapping[i] = self.height//80 - i

        # Start the game with the run game method.
        self.run_game(board)

    @staticmethod
    def generate_grid_dict(height, width):
        """Method, which generates the dict for positioning and win logic with a given size"""
        board = {}
        for i in range(height):
            for j in range(width):
                position = (i, j)
                board[position] = 0
        return board

    def run_game(self, board):
        """Main method which starts the game when called"""
        run_program = True

        while run_program:
            # eventlistener for mouse events
            for event in pygame.event.get():
                if pygame.mouse.get_pressed() and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Get position of mouse.
                        (x, y) = pygame.mouse.get_pos()

                        # Set circle position in the middle of the grid_square.
                        draw_x = x - (x % self.square_size) + self.square_mid

                        # Calculation to get xPosition from selected Mouse xPosition.
                        x = x // 80

                        # Check if column is full before placing. Break out if that's the case.
                        if self.check_if_column_full(board, x):
                            break

                        # Calculate the yPosition, where the chip should be placed with various helper methods.
                        draw_y = self.height - (self.square_size * self.draw_dict_mapping[self.get_y_pos(board, x)]) + 40

                        # Check, which players turn it is.
                        if self.playerOne:
                            # Player Ones turn.
                            pos = (x, self.get_y_pos(board, x))
                            if board[pos] == 0:
                                board[pos] = 1
                                self.draw_circle(draw_x, draw_y, self.playerOne)
                                self.screen.blit(self.background, (0, 0))
                                if self.check_if_user_won(board, pos, 1):
                                    run_program = False
                                self.switch_player()
                        else:
                            # Player Twos turn.
                            pos = (x, self.get_y_pos(board, x))
                            if board[pos] == 0:
                                board[pos] = 2
                                self.draw_circle(draw_x, draw_y, self.playerOne)
                                self.screen.blit(self.background, (0, 0))
                                if self.check_if_user_won(board, pos, 2):
                                    run_program = False
                                self.switch_player()

                if event.type == pygame.KEYDOWN:
                    # End the game with escape.
                    if event.key == pygame.K_ESCAPE:
                        self.draw = True
                        run_program = False

                # End the Program with the X in the upper right corner.
                elif event.type == pygame.QUIT:
                    self.draw = True
                    run_program = False

            pygame.display.flip()
        self.game_over(self.playerOne, self.draw)
        # wait for given time and end the game
        pygame.time.wait(5000)
        pygame.quit()

    def switch_player(self):
        """Switches between player One and Two"""
        if self.playerOne:
            # sets the chip color to blue
            self.red = 0
            self.blue = 255
            # switch the player to player 2 and change the caption
            self.playerOne = False
            pygame.display.set_caption('Connect4 - Player 2')
        else:
            # sets the chip color to red
            self.red = 250
            self.blue = 0
            # switch the player to player 1 and change the caption
            self.playerOne = True
            pygame.display.set_caption('Connect4 - Player 1')

    def draw_circle(self, draw_x, draw_y, player_one):
        """Help method which either draws a red or blue circle with a black circle around it and a smaller circle in
        the middle, for 3d effect at the given position, depending on the player"""
        if player_one:
            pygame.draw.circle(self.background, (0, 0, 0), (draw_x, draw_y), self.radius + 1)
            pygame.draw.circle(self.background, (self.red, 0, self.blue), (draw_x, draw_y), self.radius)
            pygame.draw.circle(self.background, (self.red, 100, self.blue + 100), (draw_x, draw_y), self.radius - 8)
        else:
            pygame.draw.circle(self.background, (0, 0, 0), (draw_x, draw_y), self.radius + 1)
            pygame.draw.circle(self.background, (self.red, 0, self.blue), (draw_x, draw_y), self.radius)
            pygame.draw.circle(self.background, (self.red + 100, 100, self.blue), (draw_x, draw_y), self.radius - 8)

    def get_y_pos(self, board, x):
        """Get available/free yPos at selected xPos"""
        for i in reversed(range(self.height//80)):
            if self.check_pos(board, x, i):
                return i
            i -= 1
            pass

    @staticmethod
    def check_pos(board, x, i):
        """Help method to check, whether a selected position is occupied"""
        if board[(int(x), int(i))] == 0:
            return True
        else:
            return False

    def check_if_column_full(self, board, x):
        """Help method which checks, whether a given column is already full to prevent people placing chips outside
        of the visible field """
        for y in reversed(range(self.height // 80)):
            if board[x, 0] != 0:
                return True
            elif board[(x, y)] == 0:
                return False
            else:
                y -= y
                continue

    def check_if_board_full(self, board):
        """Checks if board is full in case of a draw"""
        for i in range(self.height // 80):
            for j in range(self.width // 80):
                if board[(j, i)] == 0:
                    return False
                elif j == self.width // 80:
                    break
                else:
                    pass
        print("Board full! :(")
        return True

    def check_if_user_won(self, board, pos, player_no):
        """Logic which first, checks if a player has 4 in a row after putting in a chip at the given position. If
        that's not the case it will check, if the board is full """

        has_player_got_4 = set()
        has_player_got_4.add(pos)

        self.check_horizontal(has_player_got_4, board, pos, player_no)

        if len(has_player_got_4) >= 4:
            return True

        has_player_got_4 = set()
        has_player_got_4.add(pos)

        self.check_vertical(has_player_got_4, board, pos, player_no)

        if len(has_player_got_4) >= 4:
            return True

        has_player_got_4 = set()
        has_player_got_4.add(pos)

        self.check_diagonal(has_player_got_4, board, pos, player_no)

        if len(has_player_got_4) >= 4:
            return True

        has_player_got_4 = set()
        has_player_got_4.add(pos)

        self.check_inverted_diagonal(has_player_got_4, board, pos, player_no)

        if len(has_player_got_4) >= 4:
            return True

        if self.check_if_board_full(board):
            self.draw = True
            return True

    def check_horizontal(self, has_player_got_4, board, pos, player_no):
        """Checks from left to right"""
        for i in range(1, 4):
            if pos[0] - i >= 0:
                if board[(pos[0] - i, pos[1])] == player_no:
                    has_player_got_4.add((pos[0] - i, pos[1]))
                    print("Added left: " + str((pos[0] - i, pos[1])))
                else:
                    break
        for i in range(1, 4):
            if pos[0] + i < self.width // 80:
                if board[(pos[0] + i, pos[1])] == player_no:
                    has_player_got_4.add((pos[0] + i, pos[1]))
                    print("Added right: " + str((pos[0] + i, pos[1])))
                else:
                    break

    def check_vertical(self, has_player_got_4, board, pos, player_no):
        """Checks under the placed chip"""
        for i in range(1,4):
            if pos[1] + i < self.height//80:
                if board[(pos[0], pos[1] + i)] == player_no:
                    has_player_got_4.add((pos[0], pos[1] + i))
                    print("Added down: " + str((pos[0], pos[1] + i)))
                else:
                    break

    def check_diagonal(self, has_player_got_4, board, pos, player_no):
        """Checks bottom-left to top-right"""
        for i in range(1, 4):
            if pos[0] + i < self.width // 80 and pos[1] - i >= 0:
                if board[(pos[0] + i, pos[1] - i)] == player_no:
                    has_player_got_4.add((pos[0] + i, pos[1] - i))
                    print("Added top-right: " + str((pos[0] + i, pos[1] - i)))
                else:
                    break
        for i in range(1, 4):
            if (self.height // 80 > pos[1] + i >= 0) and pos[0] - i >= 0:
                if board[(pos[0] - i, pos[1] + i)] == player_no:
                    has_player_got_4.add((pos[0] - i, pos[1] + i))
                    print("Added bottom-left: " + str((pos[0] - i, pos[1] + i)))
                else:
                    break

    def check_inverted_diagonal(self, has_player_got_4, board, pos, player_no):
        """Checks top-left to bottom right"""
        for i in range(1, 4):
            if (self.height // 80 > pos[1] - i >= 0) and pos[0] - i >= 0:
                if board[(pos[0] - i, pos[1] - i)] == player_no:
                    has_player_got_4.add((pos[0] - i, pos[1] - i))
                    print("Added top-left: " + str((pos[0] - i, pos[1] - i)))
                else:
                    break
        for i in range(1, 4):
            if (self.height // 80 > pos[1] + i >= 0) and pos[0] + i < self.width // 80:
                if board[(pos[0] + i, pos[1] + i)] == player_no:
                    has_player_got_4.add((pos[0] + i, pos[1] + i))
                    print("Added bottom-right: " + str((pos[0] + i, pos[1] + i)))
                else:
                    break

    def game_over(self, player_one, draw):
        """method that is called if 4 chips are in a row, column or in a diagonal sequence"""
        if draw:
            win_string = " No winner "
        elif not player_one:
            win_string = "Player 1 wins!"
        else:
            win_string = "Player 2 wins!"
        text_surface, rect = self.game_font.render(win_string, (0, 0, 0))
        self.screen.blit(text_surface, (self.width/2 - 150, self.height/2 - 20))
        pygame.display.set_caption(win_string)
        pygame.display.flip()


# Start the game and input the number of columns and rows.
Connect4(8, 6)
