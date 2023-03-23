from maze import Maze
from math import floor, isnan
from random import random, choice, randint
import os
import time
import sys
import msvcrt
import keyboard

debug = False

def clear_console():
    if os.name == 'posix':  # For Linux and macOS
        os.system('clear')
    elif os.name == 'nt':  # For Windows
        os.system('cls')

def init(dimension=8):
    hxy = floor(dimension / 2)
    STARTING_QUADRANT = randint(0, 3)
    ENDING_QUADRANT = (STARTING_QUADRANT + 2) % 4
    starting_x = randint(0, hxy - 1)
    starting_y = randint(0, hxy - 1)
    ending_x = randint(0, hxy - 1)
    ending_y = randint(0, hxy - 1)
    
    if STARTING_QUADRANT == 0:
        starting_x += hxy
    elif STARTING_QUADRANT == 2:
        starting_y += hxy
    elif STARTING_QUADRANT == 3:
        starting_x += hxy
        starting_y += hxy

    if ENDING_QUADRANT == 0:
        ending_x += hxy
    elif ENDING_QUADRANT == 2:
        ending_y += hxy
    elif ENDING_QUADRANT == 3:
        ending_x += hxy
        ending_y += hxy

    return {"nx": dimension, "ny": dimension, "sx": starting_x, "sy": starting_y, "ex": ending_x, "ey": ending_y}

DIFFICULTY_SETTINGS = {
    "easy": {
        "dimensions": 4,
        "encounter_chance": 15,
        "lives": 5,
        "specialEncounterChance": 25,
        "tpChance": 5,
        "potionChance": 95,
        "potionLuck": 25,
        "numgame": {
            "numRange": 10,
            "guess": 5
        },
        "freezegame": {
            "length": 10,
            "interval": 100
        },
        "memorygame": {
            "length": 4,
            "interval": 1000
        },
        "typinggame": {
            "length": 4,
            "time": 4000
        }
    },
    "normal": {
        "dimensions": 6,
        "encounter_chance": 25,
        "lives": 5,
        "specialEncounterChance": 25,
        "tpChance": 5,
        "potionChance": 93,
        "potionLuck": 30,
        "numgame": {
            "numRange": 16,
            "guess": 4
        },
        "freezegame": {
            "length": 10,
            "interval": 50
        },
        "memorygame": {
            "length": 6,
            "interval": 1000
        },
        "typinggame": {
            "length": 6,
            "time": 5000
        }
    },
    "hard": {
        "dimensions": 8,
        "encounter_chance": 30,
        "lives": 4,
        "specialEncounterChance": 30,
        "tpChance": 10,
        "potionChance": 87,
        "potionLuck": 30,
        "numgame": {
            "numRange": 16,
            "guess": 3
        },
        "freezegame": {
            "length": 20,
            "interval": 40
        },
        "memorygame": {
            "length": 6,
            "interval": 500
        },
        "typinggame": {
            "length": 8,
            "time": 5000
        }
    },
    "expert": {
        "dimensions": 12,
        "encounter_chance": 50,
        "lives": 3,
        "specialEncounterChance": 30,
        "tpChance": 10,
        "potionChance": 87,
        "potionLuck": 50,
        "numgame": {
            "numRange": 19,
            "guess": 3
        },
        "freezegame": {
            "length": 20,
            "interval": 15
        },
        "memorygame": {
            "length": 8,
            "interval": 500
        },
        "typinggame": {
            "length": 8,
            "time": 3500
        }
    }
}


def select_difficulty():
    print('Select the difficulty:\n\n1) Easy\n2) Normal\n3) Hard\n4) Expert\n')

    while True:
        try:
            difficulty = int(input("> "))
            if difficulty > 4 or difficulty < 1:
                raise Exception()
            else:
                break
        except:
            print("Invalid input. Please enter a valid number between 1 and 4.\n")
    
    return difficulty

def init_difficulty():
    difficulty = select_difficulty()
    if difficulty == 1:
        game_settings = init(DIFFICULTY_SETTINGS["easy"]["dimensions"])
    elif difficulty == 2:
        game_settings = init(DIFFICULTY_SETTINGS["normal"]["dimensions"])
    elif difficulty == 3:
        game_settings = init(DIFFICULTY_SETTINGS["hard"]["dimensions"])
    elif difficulty == 4:
        game_settings = init(DIFFICULTY_SETTINGS["expert"]["dimensions"])
    
    return DIFFICULTY_SETTINGS[list(DIFFICULTY_SETTINGS.keys())[difficulty - 1]], game_settings

settings, game_settings = init_difficulty()
maze = Maze(game_settings["nx"], game_settings["ny"], game_settings["sx"], game_settings["sy"])
maze.make_maze()

if debug:
    print(maze.print_maze())
    print(f"Starting pos: ({game_settings['sx']}, {game_settings['sy']}), \nEnding pos: ({game_settings['ex']}, {game_settings['ey']})")

game_state = True

def generate_options(north = False, south = False, west = False, east = False):
    options = ''
    count = 1
    possible_dir = []

    if not north:
        options += f"{count}) Up"
        count += 1
        possible_dir.append("N")
    if not west:
        if options:
            options += "\n"
        options += f"{count}) Left"
        count += 1
        possible_dir.append("W")
    if not south:
        if options:
            options += "\n"
        options += f"{count}) Down"
        count += 1
        possible_dir.append("S")
    if not east:
        if options:
            options += "\n"
        options += f"{count}) Right"
        count += 1
        possible_dir.append("E")
    
    options += "\n"

    return {
        "text": options,
        "directions": possible_dir,
    }

def encounter(numgame = settings["numgame"], freezegame = settings["freezegame"], memorygame = settings["memorygame"], typinggame = settings["typinggame"]):
    def guessing(numgame):
        print(f"You have encountered a monster!\nGuess a number between 0 and {num_range - 1}. You have {num_guesses} guesses.\n")
        num_range = numgame["num_range"]
        answer = random.randint(0, num_range)
        while True:
            guess = int(input("> "))

            if isnan(guess):
                print(f"Invalid input. Please enter a number between 0 and {num_range - 1}.\n")
                continue
            elif guess < 0 or guess > (num_range - 1):
                print(f"Invalid guess. Please enter a number between 0 and {num_range - 1}.\n")
                continue
            elif guess == answer:
                print("Congratulations! You have defeated a monster!\n")
                return True
            else:
                num_guesses -= 1
                if num_guesses == 0:
                    print(f"Sorry, you are out of guesses. The answer was {answer}.\nYou lost one heart.\n")
                    return False
                elif guess > answer:
                    print(f"Wrong answer. Your guess is too high. You have {num_guesses} guesses left.")
                    continue
                elif guess < answer:
                    print(f"Wrong answer. Your guess is too low. You have {num_guesses} guesses left.")
                    continue

    def freezing(freezegame):
        
        def wrap(string, head, tail):
            return f"{head}{string}{tail}"

        def randomize_map(size, difficulty):
            key = "-" * size
            max_index = size - difficulty + 1
            start_index = random.randint(0, max_index - 1)
            key = key[:start_index] + "+" * difficulty + key[start_index + difficulty:]
            return key

        def animate(source):
            result = []
            for i in range(len(source)):
                chars = list(source)
                chars[i] = "|"
                result.append("".join(chars))
            return result

        def generate_hitbox(length, layer = 2, hit_chance=3):
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
        def sleep(ms):
            time.sleep(ms / 1000)
            return;
        recursion = generate_hitbox(freezegame["length"])
        freeze = [False] * len(recursion)
        freeze_index = [0] * len(recursion)
        freeze_count = 0

        def on_key_press(key):
            nonlocal freeze_count
            if freeze_count < len(freeze):
                freeze[freeze_count] = True
                freeze_index[freeze_count] = (index - 1 + len(recursion[freeze_count]["Marker"])) % len(recursion[freeze_count]["Marker"])
                freeze_count += 1
            else:
                freeze_count += 1

        keyboard.on_press_key("space", on_key_press)

        index = 0

        def print_frames():
            sys.stdout.write("\033[2J\033[H")  # Clear the console
            print("\n" * 6)
            for layer in recursion:
                if not freeze[layer]:
                    print(recursion[layer]["Marker"][index])
                else:
                    print(recursion[layer]["Marker"][freeze_index[layer]])

        while freeze_count < len(freeze):
            print_frames()
            index = (index + 1) % len(recursion[0]["Marker"])
            sleep(freezegame["interval"])

        print_frames()

        keyboard.unhook_key("space")

        final_frames = [recursion[layer]["Marker"][freeze_index[layer]] for layer in recursion]
        final_state = "\n".join(final_frames)

        original_maps = "\n".join([recursion[layer]["Map"] for layer in recursion])

        original_plus_count = original_maps.count("+")
        final_plus_count = final_state.count("+")
        difference = original_plus_count - final_plus_count

        return difference == 0

    def memorizing(memorygame):
        return;

    def typing(typinggame):
        return;

    selected_game = random.choice(["guessing", "freezing", "memorizing", "typing"])
    
    if selected_game == "guessing":
        return guessing()
    elif selected_game == "freezing":
        return freezing()
    elif selected_game == "memorizing":
        return memorizing()
    elif selected_game == "typing":
        return typing()



# def encounter(num_range = numrange, num_guesses = guess):
#     answer = floor(random() * num_range)

#     print(f"You have encountered a monster!\nGuess a number between 0 and {num_range - 1}. You have {num_guesses} guesses.\n")
    
#     while True:
#         guess = int(input("> "))

#         if isnan(guess):
#             print(f"Invalid input. Please enter a number between 0 and {num_range - 1}.\n")
#             continue
#         elif guess < 0 or guess > (num_range - 1):
#             print(f"Invalid guess. Please enter a number between 0 and {num_range - 1}.\n")
#             continue
#         elif guess == answer:
#             print("Congratulations! You have defeated a monster!\n")
#             return True
#         else:
#             num_guesses -= 1
#             if num_guesses == 0:
#                 print(f"Sorry, you are out of guesses. The answer was {answer}.\nYou lost one heart.\n")
#                 return False
#             elif guess > answer:
#                 print(f"Wrong answer. Your guess is too high. You have {num_guesses} guesses left.")
#                 continue
#             elif guess < answer:
#                 print(f"Wrong answer. Your guess is too low. You have {num_guesses} guesses left.")
#                 continue



def generate_cell_visualization(north = True, south = True, west = True, east = True):
    result = ""

    if north:
        result += "+—————————+\n|         |\n|         |\n"
    else:
        result += "+——— ⇑ ———+\n|         |\n|         |\n"

    if west:
        result += "|"
    else:
        result += "⇐"

    if east:
        result += "    •    |\n|         |\n|         |\n"
    else:
        result += "    •    ⇒\n|         |\n|         |\n"
    
    if south:
        result += "+—————————+"
    else:
        result += "+——— ⇓ ———+"
    
    return result

current_cell = {
    "x": game_settings["sx"], 
    "y": game_settings["sy"], 
}

remaining_lives = settings["lives"]

def prompt(current, debug = False):
    lives = settings["lives"]
    global remaining_lives
    global game_state
    walls = maze.cell_at(current["x"], current["y"]).walls
    options = generate_options(walls["N"], walls["S"], walls["W"], walls["E"])
    print(generate_cell_visualization(walls["N"], walls["S"], walls["W"], walls["E"]))
    print(f"Heart : [ {'+' * remaining_lives}{'-' * (lives - remaining_lives)} ]")

    while True:
        try:
            answer = int(input(options["text"]))
            if answer < 1 or answer > len(options["directions"]):
                raise Exception()
            else:
                break
        except:
            print(f"Invalid input. Please enter an integer between 1 and {len(options['directions'])}")
        
    if options["directions"][answer - 1] == "N":
        next_cell = {
            "x": current["x"],
            "y": current["y"] - 1,
        }
    elif options["directions"][answer - 1] == "S":
        next_cell = {
            "x": current["x"],
            "y": current["y"] + 1,
        }
    elif options["directions"][answer - 1] == "E":
        next_cell = {
            "x": current["x"] + 1,
            "y": current["y"],
        }
    elif options["directions"][answer - 1] == "W":
        next_cell = {
            "x": current["x"] - 1,
            "y": current["y"],
        }

    if debug:
        print(maze.cell_at(next_cell["x"], next_cell["y"]))
        print(options["directions"])
    
    if next_cell["x"] == game_settings["ex"] and next_cell["y"] == game_settings["ey"]:
        game_state = False
        winning_str = """                                              (`\ .-') /`                  .-') _ ,---.,---. 
                                               `.( OO ),'                 ( OO ) )|   ||   | 
  ,--.   ,--..-'),-----.  ,--. ,--.         ,--./  .--.   .-'),-----. ,--./ ,--,' |   ||   | 
   \  `.'  /( OO'  .-.  ' |  | |  |         |      |  |  ( OO'  .-.  '|   \ |  |\ |   ||   | 
 .-')     / /   |  | |  | |  | | .-')       |  |   |  |, /   |  | |  ||    \|  | )|   ||   | 
(OO  \   /  \_) |  |\|  | |  |_|( OO )      |  |.'.|  |_)\_) |  |\|  ||  .     |/ |  .'|  .' 
 |   /  /\_   \ |  | |  | |  | | `-' /      |         |    \ |  | |  ||  |\    |  `--' `--'  
 `-./  /.__)   `'  '-'  '('  '-'(_.-'       |   ,'.   |     `'  '-'  '|  | \   |  .--. .--.  
   `--'          `-----'   `-----'          '--'   '--'       `-----' `--'  `--'  '--' '--'  """
        return print(winning_str)
    
    if (random() * 100 < settings["encounter_chance"]):
        combat = encounter()
        if not combat:
            remaining_lives -= 1
            if remaining_lives == 0:
                print("Game Over!")
                
                while True:
                    try:
                        restart = input("Do you want to play again? (y/n)\n")
                        if restart in ["y", "n"]:
                            break
                        else:
                            raise Exception()
                    except:
                        print("Invalid input. Please enter only y or n.")

                if restart.lower() == "y":
                    remaining_lives = settings["lives"]
                    current = {
                        "x": game_settings["sx"],
                        "y": game_settings["sy"],
                    }
                    prompt(current, debug)
                
                game_state = False
                return
            else:
                print(f"\nYou have {remaining_lives} hearts remaining.\n")
                prompt(current, debug)

        else:
            # time.sleep(1000)
            if game_state:
                current = next_cell
                prompt(next_cell, debug)
    else:
        if game_state:
            current = next_cell
            prompt(next_cell, debug)

# if debug:
#     print(maze.cell_at(current_cell["x"], current_cell["y"]))

prompt(current_cell, debug)
