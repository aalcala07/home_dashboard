import os, subprocess, signal, time
from decouple import config

if not os.path.exists('cache'):
    os.mkdir('cache')

ENABLE_CONTROL_PANEL = config('ENABLE_CONTROL_PANEL', default=False, cast=bool)

def start_web():
    # return subprocess.Popen(['python', 'web/app.py'])
    return subprocess.Popen(['python', 'web/app.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_display():
    display_process = subprocess.Popen(['python', 'display.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    f = open('cache/.display_pid', 'w')
    f.write(str(display_process.pid))
    return display_process



if ENABLE_CONTROL_PANEL:
    print('starting web')
    web_process = start_web()
    
print('starting display')
display_process = start_display()

time.sleep(3)

running = True

def kill(signum, stackframe):
    global running
    running = False

signal.signal(signal.SIGINT, kill)
signal.signal(signal.SIGTERM, kill)

while running is True:
    time.sleep(1)

    if display_process.poll() is not None:
        print('restarting display')
        display_process = start_display()

    if ENABLE_CONTROL_PANEL and web_process.poll() != 1:
        print('restarting web server')
        web_process = start_web()
