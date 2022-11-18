import string
import random
#from subprocesss import subprocess
from secrets import choice
import crypt


def generate_password_hash(password: str = "") -> str:
    if not password:
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    return password, sha512_crypt(password)


def sha512_crypt(password: str) -> str:
    salt = ''.join([choice(string.ascii_letters + string.digits) for i in range(8)])
    rounds = 5000
    prefix = f'$6$rounds={rounds}$'
    return crypt.crypt(password, prefix + salt)
