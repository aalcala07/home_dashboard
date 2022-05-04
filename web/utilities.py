import secrets, os, bcrypt, subprocess, json
from decouple import config

passwords_dir = 'web/.passwords'

# Directory for display templates (not Flask templates)
templates_dir = 'templates'

env_file = '.env'


def generate_secret():
    secret = secrets.token_hex()
    set_config_key('FLASK_SECRET', secret)
    return secret

def check_password(username, password):
    if not os.path.exists(f"{passwords_dir}/{username}"):
        return False

    f = open(f"{passwords_dir}/{username}", 'r')
    hashed = f.read()
    f.close()

    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def store_password(username, password):
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    if not os.path.exists(passwords_dir):
        os.mkdir(passwords_dir)

    f = open(f"{passwords_dir}/{username}", 'w')
    f.write(hashed.decode())
    f.close()

def is_registered(username):
    return os.path.exists(f"{passwords_dir}/{username}")

def get_device_info():
    uptime_parts = subprocess.run(['uptime'], capture_output=True, text=True).stdout.strip().split()

    return {
        "ip_address": subprocess.run(['hostname', '-I'], capture_output=True, text=True).stdout.strip().split()[0],
        "uptime": uptime_parts[2].strip(','),
        "load_average": " ".join(uptime_parts[7:10])
    }

def get_display():

    template = config('TEMPLATE_CONFIG_FILE', default='Default', cast=str)

    return {
        "resolution": config('SCREEN_WIDTH', default='', cast=str) + " x " + config('SCREEN_HEIGHT', default='', cast=str),
        "template": template if template else 'Default',
        "screen_width": config('SCREEN_WIDTH', default=0, cast=int),
        "screen_height": config('SCREEN_HEIGHT', default=0, cast=int),
        "grid_margin": config('GRID_MARGIN', default=0, cast=int),
        "icon_scale": config('ICON_SCALE', default=0, cast=float),
        "font_scale": config('FONT_SCALE', default=0, cast=float),
        "font_name": config('FONT_NAME', default="", cast=str),
        "fps": config('FPS', default=0, cast=int),
        "show_mouse": config('SHOW_MOUSE', default=False, cast=bool),
        "show_device_info": config('SHOW_DEVICE_INFO', default=False, cast=bool),
        "debug_grid": config('DEBUG_GRID', default=False, cast=bool)
    }

def get_services():
    with open(config('SERVICES_CONFIG_FILE', 'services.json')) as json_file:
        grid_data = json.load(json_file)
    return grid_data['services']

# Get display templates (not Flask templates)
def get_templates():
    files = os.listdir(templates_dir)

    templates = [
        {
            'name': 'Default',
            'value': 'default'
        }
    ]

    for template_file in files:
        templates.append({
            'name': template_file,
            'value': template_file
        })
    
    return templates

def set_config_key(key, value):
    f = open(env_file, 'r')
    lines = f.readlines()
    f.close()

    config_key_value = key + '=' + value + "\n"
    config_value_exists = False

    for i in range(len(lines)):
        if lines[i].startswith(key):
            config_value_exists = True
            lines[i] = config_key_value
    
    if not config_value_exists:
        f = open(env_file, 'a')
        f.write(config_key_value)
    else:
        f = open(env_file, 'w')
        f.writelines(lines)
    
    f.close()