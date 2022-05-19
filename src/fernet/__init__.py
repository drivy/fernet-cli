#!/usr/bin/env python

import os
import re
import sys
import base64
from cryptography.fernet import Fernet


def read_key():
    return os.environ["FERNET_KEY"]


def generate_key():
    key = Fernet.generate_key()
    return key.decode()


def encrypt(string):
    key = read_key()
    raw_data = Fernet(key).encrypt(string.encode())
    data = base64.b64encode(raw_data)
    return data.decode()


def decrypt(string):
    key = read_key()
    raw_data = base64.b64decode(string)
    data = Fernet(key).decrypt(raw_data)
    return data.decode()


def init():
    for raw_key, value in os.environ.items():
        if not re.match(r"^FERNET__", raw_key):
            continue
        key = re.sub(r"^FERNET__", "", raw_key)
        print(f"export {key}='{decrypt(value)}'")


def usage():
    print("usage is\n\tfernet generate|init|encrypt|decrypt [content]")


def run():
    if len(sys.argv) >= 2 and (sys.argv[1] == "i" or sys.argv[1] == "init"):
        init()
    elif len(sys.argv) >= 2 and (sys.argv[1] == "g" or sys.argv[1] == "generate"):
        print(generate_key())
    elif len(sys.argv) >= 3 and (sys.argv[1] == "e" or sys.argv[1] == "encrypt"):
        print(encrypt(sys.argv[2]))
    elif len(sys.argv) >= 3 and (sys.argv[1] == "d" or sys.argv[1] == "decrypt"):
        print(decrypt(sys.argv[2]))
    else:
        usage()
        sys.exit(1)
