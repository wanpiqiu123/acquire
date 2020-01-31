import sys
from pygame.locals import *
# from my_color import *
from gui import *
import variables
from game import *

# from utility import *
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
DISPLAYSURF.fill(BGCOLOR)
pygame.display.set_caption('A')
flag = True
while flag:
    DISPLAYSURF.fill(BGCOLOR)
    for event in pygame.event.get(): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            flag = False
            break
    pygame.display.update()
pygame.quit()
pygame.init()
screen = pygame.display.set_mode((WINDOWWIDTH//2, WINDOWHEIGHT//2))
screen.fill(BGCOLOR)
pygame.display.set_caption('B')
flag = True
while flag:
    screen.fill(BGCOLOR)
    for event in pygame.event.get(): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            # pygame.quit()
            flag = False
            break
    pygame.display.update()