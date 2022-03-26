import json
import os

fp = "minesweeper/config.json"

def check_file():
    if not os.path.exists(fp):
        with open(fp, "w") as file:
            json.dump({}, file, indent=4)

def read(key):
    check_file()

    with open(fp, "r") as file:
        decoded = json.load(file)
    
    if decoded:
        try:
            return decoded[key]
        except KeyError:
            return False
    else:
        return False

def write(key, value):
    check_file()
    with open(fp, "r") as file:
        decoded = json.load(file)
    
    decoded[key] = value

    with open(fp, "w") as file:
        json.dump(decoded, file, indent=4)