from maze import Maze
from math import floor, isnan
from random import random, choice, randint
from story import print_story, show_title, rule_description
import os
import time
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
        "potionLuck": 40,
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

show_title()
time.sleep(3)
print_story()
time.sleep(5)
input("Press the Enter key to continue...")
rule_description()
input("Press the Enter key to continue...")

settings, game_settings = init_difficulty()
maze = Maze(game_settings["nx"], game_settings["ny"], game_settings["sx"], game_settings["sy"])
maze.make_maze()

def special_encounter(tp = settings["tpChance"], potion = settings["potionChance"], luck = settings["potionLuck"]):
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
            if potion_rng < settings["potionLuck"]:
                return 2
            else:
                return 3
        else:
            return 4


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
    def guessing(numgame = numgame):
        range = numgame["numRange"]
        guesses = numgame["guess"]
        clear_console()
        print(f"You have encountered a goblin!\nGuess a number between 0 and {range - 1}. You have {guesses} guesses.\n")
        answer = randint(0, range)
        while True:
            while True:
                try:
                    guess = int(input("> "))
                    break
                except ValueError:
                    print("Invalid input. Please enter an integer.")
                    continue

            if isnan(guess) or not guess:
                print(f"Invalid input. Please enter a number between 0 and {range - 1}.\n")
                continue
            elif guess < 0 or guess > (range - 1):
                print(f"Invalid guess. Please enter a number between 0 and {range - 1}.\n")
                continue
            elif guess == answer:
                return True
            else:
                guesses -= 1
                if guesses == 0:
                    print(f"Sorry, you are out of guesses. The answer was {answer}.\n")
                    return False
                elif guess > answer:
                    print(f"Wrong answer. Your guess is too high. You have {guesses} guesses left.")
                    continue
                elif guess < answer:
                    print(f"Wrong answer. Your guess is too low. You have {guesses} guesses left.")
                    continue

    def freezing(freezegame = freezegame):
        
        def wrap(string, head, tail):
            return f"{head}{string}{tail}"

        def randomize_map(size, difficulty):
            key = "-" * size
            max_index = size - difficulty + 1
            start_index = randint(0, max_index - 1)
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
    
        clear_console()
        print("You have encountered a golem!\nStop the bar at \"+\" using your spacebar!")
        time.sleep(4)

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
            #sys.stdout.write("\033[2J\033[H")  # Clear the console
            clear_console()
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

    def memorizing(memorygame = memorygame):
        length = memorygame["length"]
        interval = memorygame["interval"]
        numbers = [str(randint(0, 9)) for _ in range(length)]
        clear_console()
        print("You have encountered a slime!\nMemorize the numbers to fight it!")
        time.sleep(4)
        for number in numbers:
            clear_console()
            print(number)
            time.sleep(interval / 1000)
            clear_console()
            time.sleep(interval / 1000)
        user_input = input("Enter the string in reverse order: ")
        return user_input == "".join(reversed(numbers))

    def typing(typinggame = typinggame):
        keys = "qweasd"
        clear_console()
        print("You have encountered a skeleton!\nType the string of text in time to fight it!")
        time.sleep(4)
        indexes = [randint(0, len(keys) - 1) for _ in range(typinggame["length"])]
        target = "".join([keys[i] for i in indexes])
        remaining_time = typinggame["time"]
        score = 0
        def generate_frame(target, score):
            uppercase_target = target[:score].upper() + target[score:]
            if score != 0:
                return uppercase_target
            else:
                return target
        is_pressed_dict = {}
        key_timer = {key: time.monotonic() for key in keys}
        while remaining_time > 0 and score < len(target):
            clear_console()
            frame = generate_frame(target, score)
            print(frame)
            print(f"Time remaining: {remaining_time / 1000:.2f} seconds")
            if score < len(target):
                current_target = target[score]
                if keyboard.is_pressed(current_target) and not is_pressed_dict.get(current_target, False):
                    is_pressed_dict[current_target] = True
                    score += 1
                    key_timer[current_target] = time.monotonic()
                if not keyboard.is_pressed(current_target):
                    is_pressed_dict[current_target] = False
                if not keyboard.is_pressed(current_target) and any([keyboard.is_pressed(c) for c in keys]):
                    failed_key = [c for c in keys if keyboard.is_pressed(c)][0]
                    if time.monotonic() - key_timer[failed_key] > 0.5: #holding threshold
                        print("You pressed the wrong key!")
                        return False
            remaining_time -= 25
            time.sleep(0.025)
        clear_console()
        print(target.upper()) #visualization issue
        return score == len(target)

    selected_game = choice(["guessing", "freezing", "memorizing", "typing"])
    
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
        except KeyboardInterrupt:
            exit()
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
    if (rng < settings["encounter_chance"]):
        combat = encounter()
        if not combat:
            remaining_lives -= 1
            print("You lost the combat, you lost one heart.")
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
                prompt(next_cell, debug)
        else:
            print('Congratulations! You have won the combat! You continue on with your journey.')
            # time.sleep(1000)
            if game_state:
                current = next_cell
                prompt(next_cell, debug)
    elif rng > settings["encounter_chance"] and rng < (settings["encounter_chance"] + settings["specialEncounterChance"]):
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
            else:
                prompt(next_cell, debug)
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
