import sys
if '../' not in sys.path:
    sys.path.append('../')

import pygame
import colors
import fonts

def draw(screen, rect):
    pass 

    # # Draw rectangle
    # shape = pygame.Rect(x, y, width, height),
    # pygame.Surface.fill(screen, colors.blue_500, shape)

    # # Draw text
    # textobj = fonts.font_sm.render("Alerts component", 1, colors.white)
    # textrect = textobj.get_rect()
    # textrect.topleft = (x + 10, y + 10)
    # screen.blit(textobj, textrect)
