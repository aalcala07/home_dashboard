import sys
from datetime import date, datetime, timedelta

if '../' not in sys.path:
    sys.path.append('../')

import colors
import fonts

padding = 10
counter_font = fonts.font_8xl
label_font = fonts.font_3xl
def draw(screen, rect):

    y_padding = (rect.height - (counter_font.get_height() + label_font.get_height()))//2

    # Draw Counter
    
    counter_text = fonts.font_8xl.render(str(days_until_next_year()), 1, colors.white)
    counter_text_rect = counter_text.get_rect()
    counter_text_rect.topright = (rect.x + rect.width - padding, rect.y + y_padding)
    screen.blit(counter_text, counter_text_rect)

    # Draw Label
    label_text = label_font.render(f'Days Until {next_year()}', 1, colors.white)
    label_text_rect = label_text.get_rect()
    label_text_rect.topright = (rect.x + rect.width - padding, counter_text_rect.y + counter_text_rect.height)
    screen.blit(label_text, label_text_rect)

def next_year():
    current_year = int(datetime.now().strftime("%Y"))
    return current_year + 1

def days_until_next_year():
    return (datetime.strptime(f'{next_year()}-01-01', "%Y-%m-%d") - datetime.now()).days
