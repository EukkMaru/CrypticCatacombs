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
        "lives": 5,
        "numrange" : 10,
        "guess" : 5,
        "special_encounter_chance": 25,
        "teleport_chance": 5,
        "potion_chance": 95,
        "potion_luck": 25
    },
    "normal": {
        "dimensions": 6,
        "encounter_chance": 25,
        "lives": 5,
        "numrange" : 16,
        "guess" : 4,
        "special_encounter_chance": 25,
        "teleport_chance": 5,
        "potion_chance": 93,
        "potion_luck": 30
    },
    "hard": {
        "dimensions": 8,
        "encounter_chance": 30,
        "lives": 4,
        "numrange" : 16,
        "guess" : 3,
        "special_encounter_chance": 30,
        "teleport_chance": 10,
        "potion_chance": 87,
        "potion_luck": 30
    },
    "expert": {
        "dimensions": 12,
        "encounter_chance": 50,
        "lives": 3,
        "numrange" : 19,
        "guess" : 3,
        "special_encounter_chance": 30,
        "teleport_chance": 10,
        "potion_chance": 87,
        "potion_luck": 30
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
    [dimensions, 
     encounter_chance, 
     lives, 
     numrange, 
     guess, 
     special_encounter_chance, 
     teleport_chance, 
     potion_chance, 
     potion_luck] = list(list(DIFFICULTY_SETTINGS.values())[difficulty - 1].values())

    game_settings = init(dimensions)

    return [
        game_settings,
        encounter_chance,
        lives,
        numrange,
        guess,
        special_encounter_chance,
        teleport_chance, 
        potion_chance, 
        potion_luck
    ]

[game_settings, 
 encounter_chance, 
 lives, numrange, 
 guess, 
 special_encounter_chance,
 teleport_chance, 
 potion_chance, 
 potion_luck] = init_difficulty()

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

def special_encounter(tp = teleport_chance, potion = potion_chance, luck = potion_luck):
    print("You have found a mysterious chest. Do you want to open it?\n1) Open\n2) Ignore")

    chest_rng = random() * 100
    potion_rng = random() * 100

    while True:
        try:
            answer = int(input("> "))
            if answer > 2 or answer < 1:
                raise Exception()
            else:
                break
        except:
            print(f"Invalid input. Please enter an integer between 1 and 2")
    
    if answer == 2:
        return 0
    else:
        if chest_rng < tp:
            return 1
        elif chest_rng > tp and chest_rng < (tp+potion):
            if potion_rng < potion_luck:
                return 2
            else:
                return 3
        else:
            return 4

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
    
    rng = random() * 100
    if (rng < encounter_chance):
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
                prompt(current_cell, debug)

        else:
            # time.sleep(1000)
            if game_state:
                current = next_cell
                prompt(next_cell, debug)
    elif rng > encounter_chance and rng < (encounter_chance + special_encounter_chance):
        chest_result = special_encounter()
        if chest_result == 0:
            print("You decided to ignore the chest. You continue on with your journey.")
            if game_state:
                current = next_cell
                prompt(next_cell, debug)
    
        elif chest_result == 1:
            print("Suddenly, a bright flash of light obscures your vision. When you open your eyes, you find yourself transported back to the very place where your adventure began.\n\nYou have been teleported back to the starting point.")
            if game_state:
                next_cell = {
                    "x": game_settings["sx"],
                    "y": game_settings["sy"]
                }
                prompt(next_cell, debug)
        
        elif chest_result == 2:
            print("Inside the chest, you find an unknown potion. As you drink the potion, you feel a sudden jolt of pain.\n\nYou have lost one heart.")
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
                        "y": game_settings["sy"]
                    }
                    prompt(current, debug)
                game_state = False
                return
        elif chest_result == 3:
            if remaining_lives == lives:
                print("Inside the chest, you find an unknown potion. You drank the potion, but nothing seemed to happen. You decide to continue on your journey.")
                if game_state:
                    current = next_cell
                    prompt(next_cell, debug)
            else:
                print("Inside the chest, you find an unknown potion. As you drink the potion, you feel a surge of power coursing through your body.\n\nYou have gained one heart.")
                remaining_lives += 1
                if game_state:
                    current = next_cell
                    prompt(next_cell, debug)
        elif chest_result == 4:
            print("The chest was a trap! As soon as you opened it, a huge explosion engulfed you.\n\nYou have lost three hearts.")
            remaining_lives -= 3
            if remaining_lives <= 0:
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
                        "y": game_settings["sy"]
                    }
                    prompt(current, debug)
                game_state = False
                return
        else:
            print(f"\nYou have {remaining_lives} hearts remaining.\n")
            prompt(next_cell, debug)

    else:
        if game_state:
            current = next_cell
            prompt(next_cell, debug)

# if debug:
#     print(maze.cell_at(current_cell["x"], current_cell["y"]))

prompt(current_cell, debug)