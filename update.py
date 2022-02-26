import sys, json
from importlib import import_module

def list_active_services():
    with open('services.json') as json_file:
        grid_data = json.load(json_file)
    services = [(row.get('service'), row.get('update_interval_seconds', 0)) for row in grid_data['services'] if row.get('service')]
    return services

#TODO: refactor this and the similar code in ui.py to a generic get_callback()
def get_update_callback(service_name):
    module = import_module('services.' + service_name)
    return getattr(module, 'update', None)

if __name__ == "__main__":
    services = list_active_services()
    for service, update_interval in services:
        callback = get_update_callback(service)
        if callback:
            if update_interval:
                print(f'{service} will update every {update_interval} seconds.')
            else:
                print(f'{service} has an update callback, but is not set to update at any interval.')

        else:
            print(f'{service} has no update callback available.')
