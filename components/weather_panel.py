import sys
from datetime import datetime
from decouple import config
from os.path import exists

if '../' not in sys.path:
    sys.path.append('../')

import pygame, colors, fonts, services.weather as weather

ICON_SCALE = config('ICON_SCALE', default=1, cast=int)

forecast_day_font = fonts.font_4xl
forecast_temp_font = fonts.font_4xl

def draw(screen, rect):
    weather_data = weather.get()

    if not weather_data:
        # TODO: Add loading text/animation
        return

    current_weather_content_width = rect.width*4//16
    thermometer_content_width = rect.width*3//16
    forecast_content_width = rect.width*9//16

    current_weather_content_x = rect.x
    thermometer_content_x = current_weather_content_x + current_weather_content_width
    forecast_content_x = thermometer_content_x + thermometer_content_width

    draw_current_weather(screen, pygame.Rect(current_weather_content_x, rect.y, current_weather_content_width, rect.height), weather_data)
    draw_thermometer(screen, pygame.Rect(thermometer_content_x, rect.y, thermometer_content_width, rect.height), weather_data)
    draw_forecast(screen, pygame.Rect(forecast_content_x, rect.y, forecast_content_width, rect.height), weather_data)


def draw_current_weather(screen, rect, weather_data):
    # pygame.Surface.fill(screen, colors.red_500, rect)

    current_temp_font = fonts.font_8xl
    current_condition_font = fonts.font_3xl

    content_height = current_temp_font.get_height() + current_condition_font.get_height()
    center = (rect.x + rect.width//2, rect.y + rect.height//2)
    content_y = center[1] - content_height//2

    # Draw Temp
    current_temp = str(round(weather_data['current']['temp']))
    temp_text = current_temp_font.render(f'{current_temp}°', 1, colors.white)
    temp_text_rect = temp_text.get_rect()
    temp_text_rect.midtop = (center[0], content_y)
    screen.blit(temp_text, temp_text_rect)

    # Draw Condition
    condition_text = current_condition_font.render(weather_data['current']['weather'][0]['main'], 1, colors.white)
    condition_text_rect = condition_text.get_rect()
    condition_text_rect.midtop = (center[0], content_y + current_temp_font.get_height())
    screen.blit(condition_text, condition_text_rect)


def draw_thermometer(screen, rect, weather_data):

    max_temp = 100
    min_temp = 0
    fill_percentage = 0

    temp = weather_data['current']['temp']

    if temp <= min_temp:
        fill_percentage = 0
    elif temp >= max_temp:
        fill_percentage = 1
    else: 
        fill_percentage = temp/max_temp

    content_height = rect.height*7//10
    content_width = rect.width//3
    center = (rect.x + rect.width//2, rect.y + rect.height//2)
    content_y = center[1] - content_height//2
    
    outline_width = content_width//6
    border_radius = content_width//2

    # Thermometer Fill
    thermometer_height = content_height - (outline_width * 2)
    thermometer_fill_height = thermometer_height * fill_percentage
    thermometer_rect = pygame.Rect(0, 0, rect.width//3, thermometer_fill_height)
    thermometer_rect.midbottom = (center[0], content_y + outline_width + thermometer_height)
    if fill_percentage > 0.99:
        # Prevents fill from overflowing border
        pygame.draw.rect(screen, colors.red_500, thermometer_rect, 0, border_radius)
    else:
        pygame.draw.rect(screen, colors.red_500, thermometer_rect, 0, 0, 0, 0, border_radius, border_radius)

    # Thermometer Outline
    thermometer_rect_outline = pygame.Rect(0, 0, rect.width//3 + outline_width, content_height)
    thermometer_rect_outline.center = center
    pygame.draw.rect(screen, colors.white, thermometer_rect_outline, outline_width, border_radius)


def draw_forecast(screen, rect, weather_data):

    padding = 10
    font = fonts.font_4xl
    row_height = font.get_height()

    column_plus_padding = (rect.width - (padding*2))/5
    column_padding = column_plus_padding/10
    column_width = column_padding*8
    column_height = (column_padding*2) + (row_height + row_height//2) * 5
    table_width = column_plus_padding*5

    padding_x = (rect.width - table_width)//2
    padding_y = (rect.height - column_height)//2

    x_pos = rect.x + padding_x + column_padding + column_width//2

    for i in range(5):
        weather_data_day = weather_data['daily'][i]
        draw_forecast_column(screen, (x_pos, rect.y + padding_y), row_height, {
            "letter": datetime.fromtimestamp(weather_data_day['dt']).strftime("%a")[0],
            "high": str(round(weather_data_day['temp']['max'])),
            "low": str(round(weather_data_day['temp']['min'])),
            "icon": 'weather/' + weather_data_day['weather'][0]['icon'] + ("@2x" if ICON_SCALE > 1 else "") + ".png",
        })
        
        x_pos += column_padding*2 + column_width


def draw_forecast_column(screen, position, row_height, data):
    y = position[1]
    y += row_height + row_height//2
    draw_forecast_day(screen, (position[0], y), data['letter'])
    y += row_height + row_height//2
    draw_forecast_temp(screen, (position[0], y), data['high'])
    y += row_height + row_height//2
    draw_forecast_temp(screen, (position[0], y), data['low'])
    y += row_height + row_height//2
    draw_forecast_icon(screen, (position[0], y), data['icon'])


def draw_forecast_day(screen, position, letter):
    text = forecast_day_font.render(letter, 1, colors.indigo_200)
    text_rect = text.get_rect()
    text_rect.center = position
    screen.blit(text, text_rect)


def draw_forecast_temp(screen, position, temp):
    text = forecast_temp_font.render(temp, 1, colors.white)
    text_rect = text.get_rect()
    text_rect.center = position
    screen.blit(text, text_rect)


def draw_forecast_icon(screen, position, icon):
    path = f'icons/{icon}'
    
    if (exists(path) == False):
        return

    icon = pygame.image.load(path)
    width = icon.get_width()
    height = icon.get_height()
    screen.blit(icon, (position[0] - (width//2), position[1] - (height//2)))
