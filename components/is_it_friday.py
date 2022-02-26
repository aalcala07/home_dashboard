import sys
import pygame
import colors
import fonts

if '../' not in sys.path:
    sys.path.append('../')

import services.is_it_friday as friday

padding = 10

font = fonts.font_6xl

def draw(screen, rect):
    content_height = font.get_height()
    center = (rect.x + rect.width//2, rect.y + rect.height//2)
    content_y = center[1] - content_height//2

    text = font.render(friday.get_text(), 1, colors.white)
    text_rect = text.get_rect()
    text_rect.midtop = (center[0], content_y)
    screen.blit(text, text_rect)
