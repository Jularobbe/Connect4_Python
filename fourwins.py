import pygame

pygame.init()

#set the screen size, gridsize and chipsize (radius)
sqramountwidth = 5
sqramountheight = 4
squaresize = 80
width = sqramountwidth * squaresize
height = sqramountheight * squaresize
radius = int(squaresize/4)
squaremid = int(squaresize/2)
screen = pygame.display.set_mode((width, height))

#fill the screen with a white background
background = pygame.Surface(screen.get_size())
background.fill((255, 255, 255))
background = background.convert()

#build the grid
for i in range (0,width,squaresize):
    pygame.draw.rect(background, (0,0,0),(i,0,0,width))
    pygame.draw.rect(background, (0,0,0),(0,i,width,0))
screen.blit(background, (0, 0))

d = {
    11:0,
    12:0,
    13:0,
    14:0,
    15:0,
    21:0,
    22:0,
    23:0,
    24:0,
    25:0,
    31:0,
    32:0,
    33:0,
    34:0,
    35:0,
    41:0,
    42:0,
    43:0,
    44:0,
    45:0
}

#colors
red = 0
green = 0
blue = 0

#Player
playerone = True

#set the game time
clock = pygame.time.Clock()
FPS = 30
playtime = 0.0

#start programm
runprogramm = True

while runprogramm:
    #let the playtime run
    milliseconds = clock.tick(FPS)
    playtime += milliseconds/1000.0

    #eventlistener
    for event in pygame.event.get():
        if pygame.mouse.get_pressed():
            #get mousecklick
            if event.type == pygame.MOUSEBUTTONDOWN:
                #get position of mouse
                (x, y) = pygame.mouse.get_pos()
                #set circle position in the middle of the gridsquare
                x = x - (x%squaresize) + squaremid
                y = height - squaremid

                #swtitch players
                if playerone == True:
                    blue = 255
                    red = 0
                    playerone = False

                else:
                    blue = 0
                    red = 250
                    playerone = True

                if x == squaremid and playerone == True:
                    j=1
                    k=1
                    i=j*10+k
                    d[i]=1
                    print(d[i])
                if d[11]== 1 and x == squaremid:
                    y = height - squaremid*3
                if x == squaremid and playerone == False:
                    j=1
                    k=1
                    i=j*10+k
                    d[i]=2
                    print(d[i])

                pygame.draw.circle(background, (red, green, blue), (x,y),radius)

                screen.blit(background, (0, 0))

        if event.type == pygame.KEYDOWN:
                #end the game with escape
            if event.key == pygame.K_ESCAPE:
                runprogramm = False

        #end the Programm with the X in the upper right corner
        elif event.type == pygame.QUIT:
                runprogramm = False

    #set text at the end of the game
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)
    pygame.display.flip()
pygame.quit()
#end of game
print("This game was played for {0:2f} seconds".format(playtime))







