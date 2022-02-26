import requests, json
from os.path import exists
from decouple import config
import logging

OPEN_WEATHER_MAP_API_KEY = config('OPEN_WEATHER_MAP_API_KEY', default='', cast=str)
OPEN_WEATHER_MAP_API_URL = "https://api.openweathermap.org"
LOCATION_LAT = config('LOCATION_LAT', cast=float)
LOCATION_LONG = config('LOCATION_LONG', cast=float)
FREQUENCY = config('WEATHER_RELOAD_FREQUENCY_MINUTES', default=5, cast=int)

# Request data from API
def update():

    if not OPEN_WEATHER_MAP_API_KEY or OPEN_WEATHER_MAP_API_KEY == '':
        logging.error('Cannot fetch weather. Missing OPEN_WEATHER_MAP_API_KEY')
        return

    logging.info('Fetching weather data')

    try:
        r = requests.get(f'{OPEN_WEATHER_MAP_API_URL}/data/2.5/onecall?lat={LOCATION_LAT}&lon={LOCATION_LONG}&appid={OPEN_WEATHER_MAP_API_KEY}&exclude=minutely,hourly,alerts&units=imperial')
        weather_data = r.json()

        if 'current' in weather_data:
            weather_data_file = open("cache/.weather_data", "w") 
            weather_data_file.write(json.dumps(weather_data, indent = 4))
            weather_data_file.close()
            print('Weather data saved')
        else:
            # Rate limit reached or other error
            logging.error('Weather was not provided. Check API rate limit.')
    except requests.exceptions.JSONDecodeError:
        logging.error('Weather data not properly formed JSON.')
    except requests.exceptions.RequestException as e:
        logging.error('Connection error while trying to retrieve weather data.')

# Get data from cache file
def get():

    if(exists('cache/.weather_data') == False):
        return None
        
    with open('cache/.weather_data') as json_file:
        weather_data = json.load(json_file)

    return weather_data

# Get the current weather
def current():

    data = get()

    if not data:
        return None

    return data['current']

# Get the daily forecast
def daily():

    data = get()

    if not data:
        return None

    return data['daily']
