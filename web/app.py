from flask import Flask, session, render_template, redirect, request, flash, get_flashed_messages, abort
from utilities import generate_secret, store_password, check_password, is_registered, get_device_info, get_display, get_services, get_templates, set_config_key, toggle_service, get_locations, save_service_config
from decouple import config
import os, signal, time

# Flask Documentation 
# See https://flask.palletsprojects.com/en/2.1.x/

app = Flask(__name__)

FLASK_SECRET = config('FLASK_SECRET', default='', cast=str)

if not FLASK_SECRET:
    FLASK_SECRET = generate_secret()

app.secret_key = FLASK_SECRET
app.templates_auto_reload = True

should_shutdown = False

@app.route('/')
def index():
    return redirect('/login')

@app.route('/start', methods=['GET', 'POST'])
def start():
    
    if is_registered('root'):
        return redirect('/login')

    if request.method == 'POST':
        store_password('root', request.form['password'])
        session['username'] = 'root'
        return redirect('/overview')
    
    return render_template('start.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if not is_registered('root'):
        return redirect('/start')

    if request.method == 'POST':

        username = request.form['username']

        if check_password(username, request.form['password']):
            session['username'] = username
            return redirect('/overview')
        
        flash('Wrong password', 'error')
        return redirect('/login')
    
    if is_logged_in():
        return redirect('/overview')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route("/overview")
def overview():
    if not is_logged_in():
        return redirect('/login')

    return render_template('overview.html', page="overview", device_info=get_device_info(), display=get_display(), services=get_services())

@app.route("/display", methods=['GET', 'POST'])
def display():
    if not is_logged_in():
        return redirect('/login')

    display = get_display()
    
    if request.method == 'POST':
        for config in display['configs']:
            value = request.form['configs[' + config['name'] + ']']
            set_config_key(config['name'].upper(), value)

        template = request.form['template']
        template = '' if template == 'default' else template
        set_config_key('TEMPLATE_CONFIG_FILE', template)
        return redirect('/restart')

    return render_template('display.html', page="display", display=display, templates=get_templates())

@app.route("/services")
def services():
    if not is_logged_in():
        return redirect('/login')
    return render_template('services.html', page="services", services=get_services())

@app.route("/services/<service_name>", methods=['GET', 'POST'])
def services_show(service_name):
    if not is_logged_in():
        return redirect('/login')

    service = get_services(service_name)
    locations = get_locations()

    if not service:
        abort(404)

    if request.method == 'POST':

        for i in range(len(service['configs'])):

            if service_name == 'weather' and service['configs'][i]['name'] == 'locations':
                value = [location['name'] for location in locations if f'configs[locations][{location["name"]}]' in request.form and request.form[f'configs[locations][{location["name"]}]'] == 'on']
            else:
                value = request.form[f'configs[{service["configs"][i]["name"]}]']

            value_type = service['configs'][i]['type']

            if value_type == 'int':
                value = int(value)
            elif value_type == 'float':
                value = float(value)

            service['configs'][i]['value'] = value
        
        save_service_config(service_name, service)

        if 'restart' in request.form:
            return redirect('/restart')
        return redirect('/services/' + service_name)

    # Special templates for certain services
    if service_name == 'weather':
        return render_template('services/weather.html', page="", service=service, locations=locations)

    return render_template('services_show.html', page="", service=service)

@app.route("/services/<service_name>/toggle", methods=['POST'])
def services_toggle(service_name):
    if not is_logged_in():
        return redirect('/login')

    enable = 'enable' in request.form and request.form['enable'] == 'on'
    toggle_service(service_name, enable)
    return redirect("/restart")


@app.route("/device_info")
def device_info():
    if not is_logged_in():
        return redirect('/login')
    return render_template('device_info.html', page="device_info")

@app.route("/restart", methods=['GET', 'POST'])
def restart():

    if request.method == 'POST':
        f = open('cache/.display_pid', 'r')
        pid = int(f.read())
        os.kill(pid, signal.SIGTERM)
        global should_shutdown
        should_shutdown = True
        return {
            "status": "success"
        }
    
    return render_template('restart.html')

@app.route("/after-restart")
def afterRestart():
    flash('System restarted successfully', 'success')
    return redirect('/')

def is_logged_in():
    if 'username' in session:
        return True

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0")


while True:
    if should_shutdown is True:
        f = open('cache/.web_pid', 'r')
        pid = int(f.read())
        os.kill(pid, signal.SIGTERM)
    time.sleep(1)