import sys
from datetime import datetime
if '../' not in sys.path:
    sys.path.append('../')

import colors, fonts, services.weather as weather

padding = 10

date_font = fonts.font_6xl
time_font = fonts.font_10xl
ampm_font = fonts.font_8xl
sun_font = fonts.font_4xl

def draw(screen, rect):

    content_height = date_font.get_height() + date_font.get_height()//4 + time_font.get_height() + sun_font.get_height()
    center = (rect.x + rect.width//2, rect.y + rect.height//2)
    content_y = center[1] - content_height//2

    # Draw Date
    date_text = date_font.render(date(), 1, colors.white)
    date_text_rect = date_text.get_rect()
    date_text_rect.midtop = (center[0], content_y)
    screen.blit(date_text, date_text_rect)

    # Time Text
    time_text = time_font.render(time(), 1, colors.white)
    time_text_rect = time_text.get_rect()

    # AM/PM Text
    y_offset_time = time_font.metrics(time())[0][3]
    y_offset_ampm = ampm_font.metrics(ampm())[0][3]
    ampm_text = ampm_font.render(ampm(), 1, colors.white)
    ampm_text_rect = ampm_text.get_rect()

    time_width = time_text_rect.width + (ampm_text_rect.width//4) + ampm_text_rect.width
    time_x = center[0] - (time_width//2)

    # Draw Time
    time_text_rect.topleft = (time_x, date_text_rect.y + date_font.get_height() + date_font.get_height()//4)
    screen.blit(time_text, time_text_rect)

    # Draw AM/PM
    ampm_text_rect.topleft = (time_x + (time_width - ampm_text_rect.width), time_text_rect.y + (y_offset_time - y_offset_ampm))
    screen.blit(ampm_text, ampm_text_rect)

    weather_data = weather.current()

    if not weather_data:
        return

    # Draw Sunrise/Sunset time
    next_sun_event = get_next_sun_event(weather_data)
    sun_text = next_sun_event[0][0].upper() + next_sun_event[0][1:] + " at " + format_time(next_sun_event[1])
    sun_text = sun_font.render(sun_text, 1, colors.white)
    sun_text_rect = sun_text.get_rect()
    sun_text_rect.midtop = (center[0], content_y + content_height - sun_font.get_height())
    screen.blit(sun_text, sun_text_rect)


def date():
    return datetime.now().strftime("%A, %B") + " " + str(int(datetime.now().strftime("%d")))

def time():
    hours = str(int(datetime.now().strftime("%I")))
    minutes = datetime.now().strftime("%M")
    return f'{hours}:{minutes}'

def ampm():
    return datetime.now().strftime("%p")

def get_next_sun_event(today):

    if datetime.fromtimestamp(today['sunrise']) > datetime.now():
        return ('sunrise', today['sunrise'])

    if datetime.fromtimestamp(today['sunset']) > datetime.now():
        return ('sunset', today['sunset'])

    # Sun has set for today so get tomorrow's sunrise
    return ('sunrise', weather.daily()[1]['sunrise'])

def format_time(timestamp):
    time = datetime.fromtimestamp(timestamp)
    hours = str(int(time.strftime("%I")))
    minutes = time.strftime("%M")
    ampm = time.strftime("%p")
    return f'{hours}:{minutes} {ampm}'
