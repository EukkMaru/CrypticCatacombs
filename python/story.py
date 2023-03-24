import os
import time 
from time import sleep
import sys
import math

def clear_console():
    if os.name == 'posix':  # For Linux and macOS
        os.system('clear')
    elif os.name == 'nt':  # For Windows
        os.system('cls')

def typing_Ani(text, speed):
        string = text;
        for letter in string:
            sleep(speed) 
            sys.stdout.write(letter)
            sys.stdout.flush()
        print("")
        

def Item_Typing_Ani(list, speed):
    for item in list:
        typing_Ani(item, speed)
    print("")


def print_story():
    Item_Typing_Ani(["You went to Jeju Island for a 'Kentech preview' on January 31st"], 0.03)
    sleep(1)
    Item_Typing_Ani(['While taking a walk near Seob-ji-ko-ji, You found a cave on the beach and went in.'], 0.03)
    sleep(1)
    Item_Typing_Ani(['There was a large mural, and you went deeper, as if you were being attracted by something..'], 0.03)

    

def show_title():
    cryptic = """"              
  / 
 / 
/ 


0
   _
  / 
 / 
/ 
\\

0
   ___               
  / __
 / / 
/ /
\_

0
   ___                
  / __\ 
 / / | 
/ /__
\___

0         
   ___                
  / __\ 
 / / | '
/ /__| 
\____/

0        
   ___              
  / __\ __
 / / | '__
/ /__| | 
\____/_|   

0         
   ___               
  / __\ __ _
 / / | '__| 
/ /__| |  | 
\____/_|   

0           
   ___                
  / __\ __ _  
 / / | '__| | 
/ /__| |  | |
\____/_|   \\

0          
   ___                
  / __\ __ _   _ 
 / / | '__| | |
/ /__| |  | |_|
\____/_|   \__
           |_
0
   ___                 
  / __\ __ _   _ _
 / / | '__| | | | 
/ /__| |  | |_| 
\____/_|   \__, 
           |___
0  
   ___                
  / __\ __ _   _ _ _
 / / | '__| | | | '
/ /__| |  | |_| | |
\____/_|   \__, | 
           |___/|
0
   ___                 
  / __\ __ _   _ _ __ 
 / / | '__| | | | '_ 
/ /__| |  | |_| | |_
\____/_|   \__, | .
           |___/|_|
0           
   ___                 
  / __\ __ _   _ _ __ 
 / / | '__| | | | '_ \\
/ /__| |  | |_| | |_)
\____/_|   \__, | ._
           |___/|_|
0          
   ___                 _  
  / __\ __ _   _ _ __ | 
 / / | '__| | | | '_ \| 
/ /__| |  | |_| | |_) | 
\____/_|   \__, | .__/ 
           |___/|_|
0          
   ___                 _   
  / __\ __ _   _ _ __ | |_
 / / | '__| | | | '_ \| __
/ /__| |  | |_| | |_) | |
\____/_|   \__, | .__/ \\
           |___/|_|
0          
   ___                 _   _
  / __\ __ _   _ _ __ | |_(
 / / | '__| | | | '_ \| __|
/ /__| |  | |_| | |_) | |_
\____/_|   \__, | .__/ \_
           |___/|_|
0
   ___                 _   _
  / __\ __ _   _ _ __ | |_(_)
 / / | '__| | | | '_ \| __| 
/ /__| |  | |_| | |_) | |_| 
\____/_|   \__, | .__/ \__|_
           |___/|_|
0           
   ___                 _   _
  / __\ __ _   _ _ __ | |_(_) 
 / / | '__| | | | '_ \| __| |
/ /__| |  | |_| | |_) | |_| | 
\____/_|   \__, | .__/ \__|_
           |___/|_|
0           
   ___                 _   _
  / __\ __ _   _ _ __ | |_(_) _
 / / | '__| | | | '_ \| __| |/ 
/ /__| |  | |_| | |_) | |_| | 
\____/_|   \__, | .__/ \__|_|\\
           |___/|_|
0           
   ___                 _   _
  / __\ __ _   _ _ __ | |_(_) __
 / / | '__| | | | '_ \| __| |/ 
/ /__| |  | |_| | |_) | |_| | (_
\____/_|   \__, | .__/ \__|_|\_
           |___/|_|
0           
   ___                 _   _
  / __\ __ _   _ _ __ | |_(_) ___
 / / | '__| | | | '_ \| __| |/ _
/ /__| |  | |_| | |_) | |_| | (__
\____/_|   \__, | .__/ \__|_|\___
           |___/|_|
0           
   ___                 _   _
  / __\ __ _   _ _ __ | |_(_) ___
 / / | '__| | | | '_ \| __| |/ __|
/ /__| |  | |_| | |_) | |_| | (__
\____/_|   \__, | .__/ \__|_|\___|
           |___/|_|
"""
    cryptics = []
    cryptics = cryptic.split(sep='0')
    catacomb = """
    
        ___
    / 
    / 
    / 
    \_
    0
    ___   
    / __\\
    / /  
    / /_
    \____

    0
    ___      
    / __\__
    / /  / 
    / /__| (_
    \____/\_

    0
    ___     
    / __\__ _| 
    / /  / _` 
    / /__| (_| 
    \____/\__,_

    0
    ___      _
    / __\__ _| |
    / /  / _` | 
    / /__| (_| |
    \____/\__,_

    0
    ___      _   
    / __\__ _| |_
    / /  / _` | _
    / /__| (_| | 
    \____/\__,_|\_

    0
    ___      _                           
    / __\__ _| |_ _
    / /  / _` | __/ 
    / /__| (_| | || (
    \____/\__,_|\__\_

    0
    ___      _       
    / __\__ _| |_ __ 
    / /  / _` | __/ _` 
    / /__| (_| | || (_
    \____/\__,_|\__\__

    0
    ___      _                
    / __\__ _| |_ __ _ 
    / /  / _` | __/ _` 
    / /__| (_| | || (_| 
    \____/\__,_|\__\__,_

    0
    ___      _                          
    / __\__ _| |_ __ _  
    / /  / _` | __/ _` |
    / /__| (_| | || (_| |
    \____/\__,_|\__\__,_|

    0
    ___      _              
    / __\__ _| |_ __ _  
    / /  / _` | __/ _` |/
    / /__| (_| | || (_| | 
    \____/\__,_|\__\__,_|\\

    0
    ___      _                          
    / __\__ _| |_ __ _  _
    / /  / _` | __/ _` |/ 
    / /__| (_| | || (_| | (
    \____/\__,_|\__\__,_|\\
    0
    ___      _                       
    / __\__ _| |_ __ _  __  
    / /  / _` | __/ _` |/ __/
    / /__| (_| | || (_| | (_
    \____/\__,_|\__\__,_|\__
    0
    ___      _                          
    / __\__ _| |_ __ _  ___ 
    / /  / _` | __/ _` |/ __/
    / /__| (_| | || (_| | (_| 
    \____/\__,_|\__\__,_|\___
    0
    ___      _                           
    / __\__ _| |_ __ _  ___ ___
    / /  / _` | __/ _` |/ __/ _
    / /__| (_| | || (_| | (_| (
    \____/\__,_|\__\__,_|\___\_
    0
    ___      _                           
    / __\__ _| |_ __ _  ___ ___  _
    / /  / _` | __/ _` |/ __/ _ \| 
    / /__| (_| | || (_| | (_| (_) 
    \____/\__,_|\__\__,_|\___\___
    0
    ___      _                         
    / __\__ _| |_ __ _  ___ ___  _ 
    / /  / _` | __/ _` |/ __/ _ \| '
    / /__| (_| | || (_| | (_| (_) | 
    \____/\__,_|\__\__,_|\___\___/|
    0
    ___      _                           
    / __\__ _| |_ __ _  ___ ___  _ _ 
    / /  / _` | __/ _` |/ __/ _ \| '_ 
    / /__| (_| | || (_| | (_| (_) | | 
    \____/\__,_|\__\__,_|\___\___/|_
    0
    ___      _                           
    / __\__ _| |_ __ _  ___ ___  _ __ 
    / /  / _` | __/ _` |/ __/ _ \| '_ ` 
    / /__| (_| | || (_| | (_| (_) | | |
    \____/\__,_|\__\__,_|\___\___/|_| 
    0
    ___      _                            
    / __\__ _| |_ __ _  ___ ___  _ __ __
    / /  / _` | __/ _` |/ __/ _ \| '_ ` 
    / /__| (_| | || (_| | (_| (_) | | | | 
    \____/\__,_|\__\__,_|\___\___/|_| |_|
    0
    ___      _                          
    / __\__ _| |_ __ _  ___ ___  _ __ ___
    / /  / _` | __/ _` |/ __/ _ \| '_ ` _ 
    / /__| (_| | || (_| | (_| (_) | | | | 
    \____/\__,_|\__\__,_|\___\___/|_| |_|
    0
    ___      _                            
    / __\__ _| |_ __ _  ___ ___  _ __ ___
    / /  / _` | __/ _` |/ __/ _ \| '_ ` _ 
    / /__| (_| | || (_| | (_| (_) | | | | | 
    \____/\__,_|\__\__,_|\___\___/|_| |_| 
    0
    ___      _                            
    / __\__ _| |_ __ _  ___ ___  _ __ ___ 
    / /  / _` | __/ _` |/ __/ _ \| '_ ` _ \\
    / /__| (_| | || (_| | (_| (_) | | | | | 
    \____/\__,_|\__\__,_|\___\___/|_| |_| |
    0
    ___      _                            
    / __\__ _| |_ __ _  ___ ___  _ __ ___ |
    / /  / _` | __/ _` |/ __/ _ \| '_ ` _ \|
    / /__| (_| | || (_| | (_| (_) | | | | | |
    \____/\__,_|\__\__,_|\___\___/|_| |_| |_
    0
    ___      _                            _
    / __\__ _| |_ __ _  ___ ___  _ __ ___ | |
    / /  / _` | __/ _` |/ __/ _ \| '_ ` _ \| 
    / /__| (_| | || (_| | (_| (_) | | | | | | 
    \____/\__,_|\__\__,_|\___\___/|_| |_| |_|_
    0
    ___      _                            _
    / __\__ _| |_ __ _  ___ ___  _ __ ___ | |__  
    / /  / _` | __/ _` |/ __/ _ \| '_ ` _ \| '_ 
    / /__| (_| | || (_| | (_| (_) | | | | | | |_
    \____/\__,_|\__\__,_|\___\___/|_| |_| |_|_._
    0
    ___      _                            _
    / __\__ _| |_ __ _  ___ ___  _ __ ___ | |__  
    / /  / _` | __/ _` |/ __/ _ \| '_ ` _ \| '_
    / /__| (_| | || (_| | (_| (_) | | | | | | |_) 
    \____/\__,_|\__\__,_|\___\___/|_| |_| |_|_.__
    0
    ___      _                            _
    / __\__ _| |_ __ _  ___ ___  _ __ ___ | |__  
    / /  / _` | __/ _` |/ __/ _ \| '_ ` _ \| '_ \\
    / /__| (_| | || (_| | (_| (_) | | | | | | |_)
    \____/\__,_|\__\__,_|\___\___/|_| |_| |_|_.__
    0
    ___      _                            _
    / __\__ _| |_ __ _  ___ ___  _ __ ___ | |__  _
    / /  / _` | __/ _` |/ __/ _ \| '_ ` _ \| '_ \/
    / /__| (_| | || (_| | (_| (_) | | | | | | |_) \_
    \____/\__,_|\__\__,_|\___\___/|_| |_| |_|_.__/|
    0
    ___      _                            _
    / __\__ _| |_ __ _  ___ ___  _ __ ___ | |__  __
    / /  / _` | __/ _` |/ __/ _ \| '_ ` _ \| '_ \/ _
    / /__| (_| | || (_| | (_| (_) | | | | | | |_) \__
    \____/\__,_|\__\__,_|\___\___/|_| |_| |_|_.__/|__
    0
    ___      _                            _
    / __\__ _| |_ __ _  ___ ___  _ __ ___ | |__  ___
    / /  / _` | __/ _` |/ __/ _ \| '_ ` _ \| '_ \/ __|
    / /__| (_| | || (_| | (_| (_) | | | | | | |_) \__ \\
    \____/\__,_|\__\__,_|\___\___/|_| |_| |_|_.__/|___/
    0

    
    
    
    """    
    catacombs = []
    catacombs = catacomb.split(sep='0')
    for i in range(22):
        clear_console()
        print(cryptics[i])
        print(catacombs[math.floor(i*32/22)])
        sleep(0.13)


def rule_description():
    sleep(1)
    clear_console()
    Item_Typing_Ani(["Rule description: You are trapped in a maze The maze is square and varies in size with difficulty\nYou can advance in up to four directions in each room.\nWhen you move to each room, you may face a new event.\n Complete the mission in each event and save your life to escape the maze"],0.03)
