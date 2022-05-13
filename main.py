import os, subprocess, signal, time
from decouple import config

if not os.path.exists('cache'):
    os.mkdir('cache')

ENABLE_CONTROL_PANEL = config('ENABLE_CONTROL_PANEL', default=False, cast=bool)

def start_web():
    # return subprocess.Popen(['python', 'web/app.py'])
    web_process = subprocess.Popen(['python', 'web/app.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    f = open('cache/.web_pid', 'w')
    f.write(str(web_process.pid))
    return web_process

def start_display():
    display_process = subprocess.Popen(['python', 'display.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    f = open('cache/.display_pid', 'w')
    f.write(str(display_process.pid))
    return display_process


if ENABLE_CONTROL_PANEL:
    print('Starting web server')
    web_process = start_web()
    
print('Starting display')
display_process = start_display()

time.sleep(2)

running = True

def kill(signum, stackframe):
    global running
    running = False

signal.signal(signal.SIGINT, kill)
signal.signal(signal.SIGTERM, kill)

while running is True:

    if display_process.poll() is not None:
        print('Restarting display')
        display_process = start_display()

    if ENABLE_CONTROL_PANEL and web_process.poll() != 1 and web_process.poll() is not None:
        print('Restarting web server')
        web_process = start_web()
    
    time.sleep(1)
