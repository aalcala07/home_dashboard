import requests, json
from os.path import exists
from decouple import config
import logging

OPEN_WEATHER_MAP_API_URL = "https://api.openweathermap.org"

with open('cache/services.json') as json_file:
    service_config = json.load(json_file)
configs = [service['configs'] for service in service_config['services'] if service['service'] == 'weather'][0]

# Request data from API
def update():

    api_key = config('open_weather_map_api_key')
    
    if not api_key or api_key == '':
        logging.error('Cannot fetch weather. Missing OPEN_WEATHER_MAP_API_KEY')
        return
    
    for location in locations():

        logging.info('Fetching weather data for ' + location['name'])

        try:
            r = requests.get(f'{OPEN_WEATHER_MAP_API_URL}/data/2.5/onecall?lat={location["lat"]}&lon={location["long"]}&appid={api_key}&exclude=minutely,hourly,alerts&units=imperial')
            weather_data = r.json()

            if 'current' in weather_data:
                weather_data_file = open("cache/.weather_data_" + location['name'], "w") 
                weather_data_file.write(json.dumps(weather_data, indent = 4))
                weather_data_file.close()
                logging.info('Weather data saved for ' + location['name'])
            else:
                # Rate limit reached or other error
                logging.error('Weather was not provided. Check API rate limit.')
        except requests.exceptions.JSONDecodeError:
            logging.error('Weather data not properly formed JSON.')
        except requests.exceptions.RequestException as e:
            logging.error('Connection error while trying to retrieve weather data.')

# Get data from cache file
def get(location_name):

    location_name = 'local' if location_name == '' else location_name
    filepath = 'cache/.weather_data_' + location_name

    if(exists(filepath) == False):
        return None
        
    with open(filepath) as json_file:
        weather_data = json.load(json_file)

    return weather_data

# Get the current weather
def current(location_name):

    data = get(location_name)

    if not data:
        return None

    return data['current']

# Get the daily forecast
def daily(location_name):

    data = get(location_name)

    if not data:
        return None

    return data['daily']

def get_params():
    with open(config('SERVICES_CONFIG_FILE', 'services.json')) as json_file:
        service_config = json.load(json_file)

    for service in service_config['services']:
        if service['service'] == 'weather':
            params = service
    
    if not params:
        logging.error('Unable to find weather service config.')
        return
    
    if 'locations' in params:
        for location in params['locations']:
            location.setdefault('lat', config(location['name'].upper() + '_LAT', cast=float, default=30.317170636707612))
            location.setdefault('long', config(location['name'].upper() + '_LONG', cast=float, default=-97.75409570782983))

    return params

def config(name):
    return [config['value'] for config in configs if config['name'] == name][0]


def locations():
    with open('cache/locations.json') as json_file:
        locations_config = json.load(json_file)
    return [location for location in locations_config['locations'] if location['name'] in config('locations')]