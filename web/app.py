from flask import Flask, session, render_template, redirect, request, flash, get_flashed_messages
from utilities import generate_secret, store_password, check_password, is_registered, get_device_info, get_display, get_services, get_templates, set_config_key
from decouple import config

app = Flask(__name__)

FLASK_SECRET = config('FLASK_SECRET', default='', cast=str)

if not FLASK_SECRET:
    FLASK_SECRET = generate_secret()

app.secret_key = FLASK_SECRET


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
    
    if request.method == 'POST':
        template = request.form['template']
        template = '' if template == 'default' else template
        set_config_key('TEMPLATE_CONFIG_FILE', template)
        flash('Display settings saved. Please reboot your device.', 'success')
        return redirect('/display')

    return render_template('display.html', page="display", display=get_display(), templates=get_templates())

@app.route("/services")
def services():
    if not is_logged_in():
        return redirect('/login')
    return render_template('services.html', page="services")

@app.route("/device_info")
def device_info():
    if not is_logged_in():
        return redirect('/login')
    return render_template('device_info.html', page="device_info")


def is_logged_in():
    if 'username' in session:
        return True


if __name__ == '__main__':
    app.run(host="0.0.0.0")