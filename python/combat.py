from random import random
from math import floor
from time import sleep

def wrap(string, head, tail):
    return f"{head} {string} {tail}"

def randomize_map(size, difficulty):
    key = "-" * size
    MAX_INDEX = size - difficulty + 1
    START_INDEX = floor(random() * MAX_INDEX)
    return key[0:START_INDEX] + "+" * difficulty + key[START_INDEX + difficulty:]

def animate(source):
    result = []

    for i in range(len(source)):
        chars = source.split('')
        chars[i] = "|"
        result.append(chars.join(''))

    return result

def generate_hitbox(length, layer, hit_chance = 3):
    recuresion = dict()
    for i in range(layer):
        temp_map = randomize_map(length, hit_chance)
        marker = animate(temp_map)
        for j in range(len(marker)):
            marker[j] = wrap(marker[j], "[", "]")
        recuresion[i] = {
            "Map": wrap(temp_map, "[", "]"),
            "Marker": marker, 
        }
    return recuresion

def animate_hitbox(recursion, delay = 50):
    freeze = []
    freeze_index = []
    