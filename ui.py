import pygame, sys, json
from importlib import import_module
from decouple import config
from fractions import Fraction
#from itertools import repeat
import colors

SCREEN_WIDTH = config('SCREEN_WIDTH', default=1080, cast=int)
SCREEN_HEIGHT = config('SCREEN_HEIGHT', default=1920, cast=int)
DEBUG_GRID = config('DEBUG_GRID', default=False, cast=bool)
GRID_MARGIN = config('GRID_MARGIN', default=30, cast=int)


def draw_row(screen, row_number):
    y = row_y(row_number)
    row_height = rows[row_number]["height"]
    use_margin = rows[row_number]["use_margin"]
    x = GRID_MARGIN if use_margin else 0

    for column in rows[row_number]['columns']:
        
        if (DEBUG_GRID):
            shape = pygame.Rect(x, y, column["width"], row_height)
            pygame.Surface.fill(screen, getattr(colors, column["debug_color"]), shape)

        if "component" in column:
            rect = pygame.Rect(x, y, column['width'], row_height)
            column["component"](screen, rect)

        x += column["width"]

def row_y(row_number):
    y = sum(rows[i]["height"] for i in range(row_number))
    return y

def get_component_callback(component_name):
    module = import_module('components.' + component_name)
    return getattr(module, 'draw')

debug_color_index = 0

def next_debug_color():
    global debug_color_index
    if debug_color_index >= len(colors.debug_colors):
        debug_color_index = 0
    color = colors.debug_colors[debug_color_index]
    debug_color_index += 1
    return color

def get_rows():
    with open('template.json') as json_file:
        grid_data = json.load(json_file)

    rows = []

    for row in grid_data['rows']:
        columns = []
        
        for column in row['columns']:
            margins = (GRID_MARGIN * 2) if row['use_margin'] else 0
            columns.append({
                "width": int((SCREEN_WIDTH - margins) * Fraction(column['width'])),
                "component": get_component_callback(column['component']),
                "debug_color": next_debug_color()
            })

        rows.append({
            "height": int(SCREEN_HEIGHT * Fraction(row['height'])),
            "columns": columns,
            "use_margin": row["use_margin"]
        })
    
    return rows

rows = get_rows()
