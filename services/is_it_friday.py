import requests
import logging

def update():
    logging.info('Fetching Is It Friday data')
    url = 'https://www.is-it-friday.org/'
    friday = False
    try:
        r = requests.get(url)
        friday = "YES!!! IT'S FRIDAY" in r.text

        with open('cache/.is_it_friday_data', 'w') as f:
            print(friday, file=f)
    except requests.exceptions.RequestException as e:
        logging.error('Connection error while trying to retrieve Is It Friday data')


def get_text():
    try:
        with open('cache/.is_it_friday_data') as f:
            cached_data = f.readline().strip()
            friday = cached_data == 'True'

        return f'Today is {"not "*(not friday)}Friday.'

    except FileNotFoundError:
        return 'Unknown if today is Friday.'

if __name__ == "__main__":
    print('Updating cached data from remote service')
    update()
    print('Reading from cache')
    print(get_text())
