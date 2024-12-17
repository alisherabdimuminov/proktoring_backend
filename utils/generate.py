import string
import random


def generate():
    token = ""
    letters = string.ascii_lowercase
    for i in range(6):
        token += random.choice(letters)
    return token
