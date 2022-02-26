import sys

if '../' not in sys.path:
    sys.path.append('../')

import pygame, colors, fonts

camera_label_font = fonts.font_2xl
primary_camera_status_font = fonts.font_7xl
secondary_camera_status_font = fonts.font_5xl

camera_bg_color = colors.gray_700
camera_outline_color = colors.bg_color
padding = 10

def draw(screen, rect):

    primary_camera_height = rect.height*3/5
    secondary_camera_height = rect.height*2/5
    secondary_camera_width = rect.width//2
    secondary_camera_y = rect.y + primary_camera_height

    draw_primary_camera(screen, pygame.Rect(rect.x, rect.y, rect.width, primary_camera_height), {
        "name": "CAM1"
    })
    draw_secondary_camera(screen, pygame.Rect(rect.x, secondary_camera_y, secondary_camera_width, secondary_camera_height), {
        "name": "CAM2"
    })
    draw_secondary_camera(screen, pygame.Rect(rect.x + secondary_camera_width, secondary_camera_y, secondary_camera_width, secondary_camera_height), {
        "name": "CAM3"
    })

def draw_primary_camera(screen, rect, camera):
    pygame.Surface.fill(screen, camera_bg_color, rect)
    pygame.draw.rect(screen, camera_outline_color, rect, 1)

    center = (rect.x + rect.width//2, rect.y + rect.height//2)

    # Label Text
    label_text = camera_label_font.render(camera['name'], 1, colors.white)
    label_text_rect = label_text.get_rect()
    label_text_rect.topleft = (rect.x + padding, rect.y + padding)
    screen.blit(label_text, label_text_rect)

    # Status Text
    status_text = primary_camera_status_font.render('OFFLINE', 1, colors.white)
    status_text_rect = status_text.get_rect()
    status_text_rect.center = center
    screen.blit(status_text, status_text_rect)

def draw_secondary_camera(screen, rect, camera):
    pygame.Surface.fill(screen, camera_bg_color, rect)
    pygame.draw.rect(screen, camera_outline_color, rect, 1)

    center = (rect.x + rect.width//2, rect.y + rect.height//2)

    # Label Text
    label_text = camera_label_font.render(camera['name'], 1, colors.white)
    label_text_rect = label_text.get_rect()
    label_text_rect.topleft = (rect.x + padding, rect.y + padding)
    screen.blit(label_text, label_text_rect)

    # Status Text
    status_text = secondary_camera_status_font.render('OFFLINE', 1, colors.white)
    status_text_rect = status_text.get_rect()
    status_text_rect.center = center
    screen.blit(status_text, status_text_rect)
