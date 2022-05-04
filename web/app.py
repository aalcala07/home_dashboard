from flask import Flask, session, render_template, redirect, request, flash, get_flashed_messages
import bcrypt, os

app = Flask(__name__)
app.secret_key = 'secret'

passwords_dir = 'web/.passwords'



@app.route('/')
def index():
    return redirect('/login')

@app.route('/start', methods=['GET', 'POST'])
def start():
    
    if os.path.exists(f"{passwords_dir}/root"):
        return redirect('/login')

    if request.method == 'POST':
        store_password('root', request.form['password'])
        session['username'] = 'root'
        return redirect('/overview')
    
    return render_template('start.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if not os.path.exists(f"{passwords_dir}/root"):
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
    return render_template('overview.html', page="overview")

@app.route("/display")
def display():
    if not is_logged_in():
        return redirect('/login')
    return render_template('display.html', page="display")

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

if __name__ == '__main__':
    app.run(host="0.0.0.0")