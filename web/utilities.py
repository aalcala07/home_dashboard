import secrets, os, bcrypt, subprocess, json, math, shutil
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

    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    uptime = human_time_from_seconds(uptime_seconds)

    one_minute, five_minutes, fifteen_minutes = os.getloadavg()

    total, used, free = shutil.disk_usage("/")

    return {
        "ip_address": subprocess.run(['hostname', '-I'], capture_output=True, text=True).stdout.strip().split()[0],
        "uptime": uptime,
        "load_average_one_min": str(one_minute),
        "load_average_five_min": str(five_minutes),
        "load_average_fifteen_min": str(fifteen_minutes),
        "disk_usage": "%d / %d GB" % (used // (2**30), total // (2**30)),
        "space_available": "%d GB" % (free // (2**30))
    }

def human_time_from_seconds(seconds):
    seconds_in_day = 24*60*60
    seconds_in_hour = 60*60
    seconds_in_minute = 60

    if (seconds >= seconds_in_day):
        days = math.floor(seconds / seconds_in_day)
        return str(days) + " " + ("day" if days == 1 else "days")

    if (seconds >= seconds_in_hour):
        hours = math.floor(seconds / seconds_in_hour)
        return str(hours) + " " + ("hour" if hours == 1 else "hours")

    if (seconds >= seconds_in_minute):
        minutes = math.floor(seconds / seconds_in_minute)
        return str(minutes) + " " + ("minute" if minutes == 1 else "minutes")

    return 'less than 1 minute'

def get_display():

    template = config('TEMPLATE_CONFIG_FILE', default='Default', cast=str)
    display_configs = [
        {
            'name': 'screen_width',
            'label': 'Screen Width',
            'value': config('SCREEN_WIDTH', default=0, cast=int),
            'type': 'int'
        },
        {
            'name': 'screen_height',
            'label': 'Screen Height',
            'value': config('SCREEN_HEIGHT', default=0, cast=int),
            'type': 'int'
        },
        {
            'name': 'grid_margin',
            'label': 'Grid Margin',
            'value': config('GRID_MARGIN', default=0, cast=int),
            'type': 'int'
        },
        {
            'name': 'icon_scale',
            'label': 'Icon Scale',
            'value': config('ICON_SCALE', default=0, cast=int),
            'type': 'float'
        },
        {
            'name': 'font_scale',
            'label': 'Font Scale',
            'value': config('FONT_SCALE', default=0, cast=float),
            'type': 'float'
        },
        {
            'name': 'font_name',
            'label': 'Font Name',
            'value': config('FONT_NAME', default="", cast=str),
            'type': 'str'
        },
        {
            'name': 'fps',
            'label': 'FPS',
            'value': config('FPS', default=0, cast=int),
            'type': 'int'
        },
        {
            'name': 'show_mouse',
            'label': 'Show Mouse',
            'value': config('SHOW_MOUSE', default=False, cast=bool),
            'type': 'bool'
        },
        {
            'name': 'show_device_info',
            'label': 'Show Device Info',
            'value': config('SHOW_DEVICE_INFO', default=False, cast=bool),
            'type': 'bool'
        },
        {
            'name': 'debug_grid',
            'label': 'Debug Grid',
            'value': config('DEBUG_GRID', default=False, cast=bool),
            'type': 'bool'
        },
    ]
    

    return {
        "resolution": config('SCREEN_WIDTH', default='', cast=str) + " x " + config('SCREEN_HEIGHT', default='', cast=str),
        "template": template if template else 'Default',
        "configs": display_configs
    }

def get_services():
    with open(config('SERVICES_CONFIG_FILE', 'services.json')) as json_file:
        grid_data = json.load(json_file)
    return grid_data['services']

# Get display templates (not Flask templates)
def get_templates():
    templates = [
        {
            'name': 'Default',
            'value': 'default'
        }
    ]

    if os.path.exists(templates_dir):
        files = os.listdir(templates_dir)
    
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