from maze import Maze
from math import floor
from math import isnan
from random import random
# import time

debug = True

def init(dimension = 8):
    hxy = int(dimension / 2)
    STARTING_QUADRANT = floor(random() * 4)
    ENDING_QUADRANT = (STARTING_QUADRANT + 2) % 4

    starting_x = floor(random() * hxy)
    starting_y = floor(random() * hxy)

    if STARTING_QUADRANT == 0:
        starting_x += hxy
    elif STARTING_QUADRANT == 2:
        starting_y += hxy
    elif STARTING_QUADRANT == 3:
        starting_x += hxy
        starting_y += hxy

    ending_x = floor(random() * hxy)
    ending_y = floor(random() * hxy)

    if ENDING_QUADRANT == 0:
        ending_x += hxy
    elif ENDING_QUADRANT == 2:
        ending_y += hxy
    elif ENDING_QUADRANT == 3:
        ending_x += hxy
        ending_y += hxy

    return {
        'nx': dimension,
        'ny': dimension,
        'sx': starting_x,
        'sy': starting_y,
        'ex': ending_x,
        'ey': ending_y,
    }

DIFFICULTY_SETTINGS = {
    "easy": {
        "dimensions": 4,
        "encounter_chance": 15,
        "lives": 8,
        "numrange" : 10,
        "guess" : 6,
    },
    "normal": {
        "dimensions": 6,
        "encounter_chance": 25,
        "lives": 5,
        "numrange" : 13,
        "guess" : 5,
    },
    "hard": {
        "dimensions": 8,
        "encounter_chance": 40,
        "lives": 4,
        "numrange" : 16,
        "guess" : 4,
    },
    "expert": {
        "dimensions": 12,
        "encounter_chance": 60,
        "lives": 3,
        "numrange" : 19,
        "guess" : 4,
    },
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
    [dimensions, encounter_chance, lives, numrange, guess] = list(list(DIFFICULTY_SETTINGS.values())[difficulty - 1].values())

    game_settings = init(dimensions)

    return [
        game_settings,
        encounter_chance,
        lives,
        numrange,
        guess,
    ]

[game_settings, encounter_chance, lives, numrange, guess] = init_difficulty()

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

def encounter(num_range = numrange, num_guesses = guess):
    answer = floor(random() * num_range)

    print(f"You have encountered a monster!\nGuess a number between 0 and {num_range - 1}. You have {num_guesses} guesses.\n")

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

remaining_lives = lives

def prompt(current, debug = False):
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
    
    if (random() * 100 < encounter_chance):
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
                    remaining_lives = lives
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