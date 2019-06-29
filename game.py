import pygame


class Connect4:
    def __init__(self, height, width):
        print("Setting up the board.")
        d = self.generateGridDict(height, width)

        pygame.init()

        # set the screen size, gridsize and chipsize (radius)
        sqramountwidth = height
        sqramountheight = width
        squaresize = 80
        width = sqramountwidth * squaresize
        height = sqramountheight * squaresize
        radius = int(squaresize / 4)
        squaremid = int(squaresize / 2)
        screen = pygame.display.set_mode((width, height))

        # fill the screen with a white background
        background = pygame.Surface(screen.get_size())
        background.fill((255, 255, 255))
        background = background.convert()

        # build the grid
        for i in range(0, width, squaresize):
            pygame.draw.rect(background, (0, 0, 0), (i, 0, 0, width))
            pygame.draw.rect(background, (0, 0, 0), (0, i, width, 0))
        screen.blit(background, (0, 0))

        # colors
        red = 0
        green = 0
        blue = 0

        # Player
        playerone = True

        # start programm
        runprogramm = True

        while runprogramm:
            # eventlistener
            for event in pygame.event.get():
                if pygame.mouse.get_pressed():
                    # get mousecklick
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # get position of mouse
                        (x, y) = pygame.mouse.get_pos()
                        # set circle position in the middle of the gridsquare
                        x = x - (x % squaresize) + squaremid
                        y = height - squaremid

                        # swtitch players
                        if playerone == True:
                            blue = 255
                            red = 0
                            playerone = False

                        else:
                            blue = 0
                            red = 250
                            playerone = True

                        if x == squaremid and playerone == True:
                            j = 1
                            k = 1
                            i = j * 10 + k
                            d[i] = 1
                            print(d[i])
                        if d[(1,1)] == 1 and x == squaremid:
                            y = height - squaremid * 3
                        if x == squaremid and playerone == False:
                            j = 1
                            k = 1
                            i = j * 10 + k
                            d[i] = 2
                            print(d[i])

                        pygame.draw.circle(background, (red, green, blue), (x, y), radius)

                        screen.blit(background, (0, 0))

                if event.type == pygame.KEYDOWN:
                    # end the game with escape
                    if event.key == pygame.K_ESCAPE:
                        runprogramm = False

                # end the Programm with the X in the upper right corner
                elif event.type == pygame.QUIT:
                    runprogramm = False

            pygame.display.flip()
        pygame.quit()
        # set text at the end of the game
        print("End of Game")

    def generateGridDict(self, height, width):
        board = {}
        for i in range(height):
            for j in range(width):
                position = (i, j)
                board[position] = 0
        return board


Connect4(8, 6)