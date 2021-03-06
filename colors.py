from decouple import config

indigo_900 = (10, 5, 20)
indigo_800 = (29, 29, 38)
indigo_200 = (155, 147, 207)

white = (255,255,255)
black = (0,0,0)

red_500 = (240, 20, 45)
green_500 = (20, 250, 40)
yellow_500 = (250, 250, 0)
blue_500 = (0, 40, 255)
purple_500 = (255, 60, 255)

gray_700 = (45, 46, 54)

debug_colors = [
    'red_500',
    'green_500',
    'yellow_500',
    'blue_500',
    'purple_500',
]


bg_color = globals()[config('BG_COLOR', default='indigo_800', cast=str)]