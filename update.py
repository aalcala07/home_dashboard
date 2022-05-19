import sys, json
from importlib import import_module
from decouple import config

def list_active_services():
    with open(config('SERVICES_CONFIG_FILE', 'cache/services.json')) as json_file:
        grid_data = json.load(json_file)
    services = [(row.get('service'), row.get('configs', [])) for row in grid_data['services'] if row.get('service') and row.get('enabled') is True]
    return services

#TODO: refactor this and the similar code in ui.py to a generic get_callback()
def get_update_callback(service_name):
    module = import_module('services.' + service_name)
    return getattr(module, 'update', None)

if __name__ == "__main__":
    services = list_active_services()
    for service, configs in services:
        update_interval = next((config['value'] for config in configs if config.name == 'update_interval_seconds'), None)
        callback = get_update_callback(service)
        if callback:
            if update_interval:
                print(f'{service} will update every {update_interval} seconds.')
            else:
                print(f'{service} has an update callback, but is not set to update at any interval.')

        else:
            print(f'{service} has no update callback available.')
