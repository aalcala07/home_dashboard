import secrets, os, bcrypt

passwords_dir = 'web/.passwords'
env_file = '.env'

def generate_secret():
    secret = secrets.token_hex()

    f = open(env_file, 'r')
    lines = f.readlines()
    f.close()

    config_key_value = 'FLASK_SECRET=' + secret + "\n"
    config_value_exists = False

    for i in range(len(lines)):
        if lines[i].startswith('FLASK_SECRET'):
            config_value_exists = True
            lines[i] = config_key_value
    
    if not config_value_exists:
        f = open(env_file, 'a')
        f.write(config_key_value)
    else:
        f = open(env_file, 'w')
        f.writelines(lines)
    
    f.close()
    return secret

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

def is_registered(username):
    return os.path.exists(f"{passwords_dir}/{username}")