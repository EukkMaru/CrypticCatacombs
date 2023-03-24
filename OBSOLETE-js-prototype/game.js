import { Maze } from './maze.js';
import readline from 'readline';

const debug = false;

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

//initialize (the parameter should always be even)
function init(dimension = 8) {
    let hxy = dimension / 2;
    const starting_quadrant = Math.floor(Math.random() * 4);
    const ending_quadrant = (starting_quadrant + 2) % 4;
    /*
    1 | 0
    --+--
    2 | 3
    */

    let starting_x = Math.floor(Math.random() * hxy);
    let starting_y = Math.floor(Math.random() * hxy);

    switch (starting_quadrant) {
        case 0:
            starting_x += hxy;
            break;
        case 2:
            starting_y += hxy;
            break;
        case 3:
            starting_x += hxy;
            starting_y += hxy;
            break;
    }

    let ending_x = Math.floor(Math.random() * hxy);
    let ending_y = Math.floor(Math.random() * hxy);

    switch (ending_quadrant) {
        case 0:
            ending_x += hxy;
            break;
        case 2:
            ending_y += hxy;
            break;
        case 3:
            ending_x += hxy;
            ending_y += hxy;
            break;
    }
    return {
        'nx': dimension,
        'ny': dimension,
        'sx': starting_x,
        'sy': starting_y,
        'ex': ending_x,
        'ey': ending_y
    }
}

const difficultySettings = {
    "easy": {
      "dimensions": 4,
      "encounterChance": 15,
      "lives": 5,
      "numrange": 10,
      "guess": 5,
      "specialEncounterChance": 25,
      "teleportChance": 5,
      "potionChance": 95,
      "potionLuck": 25
    },
    "normal": {
      "dimensions": 6,
      "encounterChance": 25,
      "lives": 5,
      "numrange": 16,
      "guess": 4,
      "specialEncounterChance": 25,
      "teleportChance": 5,
      "potionChance": 93,
      "potionLuck": 30
    },
    "hard": {
      "dimensions": 8,
      "encounterChance": 30,
      "lives": 4,
      "numrange": 16,
      "guess": 3,
      "specialEncounterChance": 30,
      "teleportChance": 10,
      "potionChance": 87,
      "potionLuck": 30
    },
    "expert": {
      "dimensions": 12,
      "encounterChance": 50,
      "lives": 3,
      "numrange": 19,
      "guess": 3,
      "specialEncounterChance": 30,
      "teleportChance": 10,
      "potionChance": 87,
      "potionLuck": 30
    }
  };
  

async function selectDifficulty() {
    console.log('Select the difficulty:\n\n1) Easy\n2) Normal\n3) Hard\n4) Expert\n');

    let difficulty = await new Promise(resolve => {
        rl.question('> ', (ans) => {
            let parsedAns = parseInt(ans);
            if (isNaN(parsedAns) || parsedAns < 1 || parsedAns > 4) {
                console.log('Invalid input. Please enter a valid number between 1 and 4.\n');
                resolve(selectDifficulty());
            } else {
                resolve(parsedAns);
            }
        });
    });

    return difficulty;
}

async function initDifficulty() {
    let difficulty = await selectDifficulty();
    let {
        dimensions,
        encounterChance,
        lives,
        numrange,
        guess,
        specialEncounterChance,
        teleportChance,
        potionChance,
        potionLuck
    } = difficultySettings[Object.keys(difficultySettings)[difficulty - 1]];

    let gameSettings = init(dimensions);
    return {
        gameSettings,
        encounterChance,
        lives,
        numrange,
        guess,
        specialEncounterChance,
        teleportChance,
        potionChance,
        potionLuck
    };
}

const {
    gameSettings,
    encounterChance,
    lives,
    numrange,
    guess,
    specialEncounterChance,
    teleportChance,
    potionChance,
    potionLuck
} = await initDifficulty();

const maze = new Maze(gameSettings.nx, gameSettings.ny, gameSettings.sx, gameSettings.sy);
maze.make_maze();

if (debug) {
    console.log(maze.toString());
    console.log(`Starting pos: (${gameSettings.sx}, ${gameSettings.sy}),\nEnding pos: (${gameSettings.ex}, ${gameSettings.ey})`);
}


//true: in game, false: game over/end
let gamestate = true;

function generateOptions(north = false, south = false, west = false, east = false) {
    let options = '';
    let count = 1;
    let possibleDir = [];

    if (!north) {
        options += `${count++}) Up`;
        possibleDir.push('N');
    }
    if (!west) {
        options += `${options ? '\n' : ''}${count++}) Left`;
        possibleDir.push('W');
    }
    if (!south) {
        options += `${options ? '\n' : ''}${count++}) Down`;
        possibleDir.push('S');
    }
    if (!east) {
        options += `${options ? '\n' : ''}${count++}) Right`;
        possibleDir.push('E');
    }

    options += "\n";

    return {
        'text': options,
        'directions': possibleDir
    };
}

async function encounter(range = numrange, numGuesses = guess) {
    const answer = Math.floor(Math.random() * range); // generate random answer

    console.log(`You have encountered a monster!\nGuess a number between 0 and ${range - 1}. You have ${numGuesses} guesses.\n`);

    return new Promise(resolve => {
        function askQuestion() {
            rl.question('> ', (guess) => {
                const parsedGuess = parseInt(guess, 10);

                if (isNaN(parsedGuess)) {
                    console.log(`Invalid input. Please enter a number between 0 and ${range - 1}.\n`);
                    askQuestion(); // call the function again to ask for a valid input
                } else if (parsedGuess < 0 || parsedGuess > (range - 1)) {
                    console.log(`Invalid guess. Please enter a number between 0 and ${range - 1}.\n`);
                    askQuestion(); // call the function again to ask for a valid input
                } else if (parsedGuess === answer) {
                    console.log('Congratulations! You have defeated a monster!\n');
                    resolve(true);
                } else {
                    numGuesses--;

                    if (numGuesses === 0) {
                        console.log(`Sorry, you are out of guesses. The answer was ${answer}.\nYou lost one heart.\n`);
                        resolve(false);
                    } else {
                        const hint = parsedGuess > answer ? 'too high' : 'too low';
                        console.log(`Wrong answer. Your guess is ${hint}. You have ${numGuesses} guesses left.`);
                        askQuestion();
                    }
                }
            });
        }

        askQuestion();
    });
}

async function specialEncounter(tp = teleportChance, potion = potionChance, luck = potionLuck) {
    console.log('You have found a mysterious chest. Do you want to open it?\n1) Open\n2) Ignore');

    let chestRNG = Math.random() * 100;
    let potionRNG = Math.random() * 100;
    
    return new Promise(resolve => { //1: tp, 2: poison potion(-1), 3: health potion, 4: trap(-3)
        function askQuestion() {
            rl.question('> ', (ans) => {
                const parsedAns = parseInt(ans, 10);

                if(isNaN(parsedAns)) {
                    console.log(`Invalid input, Please enter a number between 1 and 2.`);
                    askQuestion();
                } else if (parsedAns < 1 || parsedAns > 2) {
                    console.log(`Invalid input, Please enter a number between 1 and 2.`);
                    askQuestion();
                } else if (parsedAns == 2) {
                    resolve(0);
                } else {
                    if(chestRNG < tp) {
                        resolve(1);
                    } else if (chestRNG > tp && chestRNG < (tp+potion)) {
                        if(potionRNG < potionLuck) {
                            resolve(2);
                        } else {
                            resolve(3);
                        }
                    } else {
                        resolve(4);
                    }
                }
            });
        }

        askQuestion();
    });
}


async function prompt(current, debug = false) {
    //current is an object where {'x' : int, 'y' : int}
    let walls = maze.cell_at(current.x, current.y).walls;
    let options = generateOptions(walls.N, walls.S, walls.W, walls.E);
    console.log(generateCellVisualization(walls.N, walls.S, walls.W, walls.E));
    console.log(`Heart : [ ${'+'.repeat(remainingLives)}${'-'.repeat(lives - remainingLives)} ]`);

    rl.question(options.text, async (ans) => {
        ans *= 1;
        let next_cell;
        if (!Number.isInteger(ans) || ans < 1 || ans > options.directions.length) {
            console.log("Invalid input. Please enter an integer between 1 and " + options.directions.length + ".\n");
            next_cell = current;
            return prompt(next_cell, debug);
        }
        switch (options.directions[ans - 1]) {
            case 'N':
                next_cell = {
                    'x': current.x,
                    'y': current.y - 1
                }
                break;
            case 'S':
                next_cell = {
                    'x': current.x,
                    'y': current.y + 1
                }
                break;
            case 'E':
                next_cell = {
                    'x': current.x + 1,
                    'y': current.y
                }
                break;
            case 'W':
                next_cell = {
                    'x': current.x - 1,
                    'y': current.y
                }
                break;
        }
        if (debug) {
            console.log(maze.cell_at(next_cell.x, next_cell.y));
            console.log(options.directions);
        }
        if (next_cell.x == gameSettings.ex && next_cell.y == gameSettings.ey) {
            gamestate = false;
            return console.log("You Won!");
        }
        var rng = Math.random() * 100;
        if (rng < encounterChance) {
            let combat = await encounter();
            if (!combat) {
                remainingLives--;
                if (remainingLives == 0) {
                    console.log("Game Over!");
                    rl.question('Do you want to play again? (y/n)', (answer) => {
                        if (answer.toLowerCase() === 'y') {
                            remainingLives = lives;
                            current = {
                                'x': gameSettings.sx,
                                'y': gameSettings.sy
                            };
                            return prompt(current, debug);
                        } else {
                            rl.close();
                        }
                    });
                    gamestate = false;
                    return;
                } else {
                    console.log(`\nYou have ${remainingLives} hearts remaining.\n`);
                    prompt(next_cell, debug); // prompt again with the same cell
                }
            } else {
                // delay execution of next cell
                setTimeout(() => {
                    if (gamestate) {
                        current = next_cell;
                        prompt(next_cell, debug);
                    }
                }, 1000); // wait for 1 second before triggering visualization of next cell
            }
        } else if (rng > encounterChance && rng < (encounterChance + specialEncounterChance)) {
            let chestResult = await specialEncounter();
            if (chestResult == 0) {
                console.log(`You decided to ignore the chest. You continue on with your journey.`);
                setTimeout(() => {
                    if (gamestate) {
                        current = next_cell;
                        prompt(next_cell, debug);
                    }
                }, 1000);
            } else if (chestResult == 1) {
                console.log(`Suddenly, a bright flash of light obscures your vision. When you open your eyes, you find yourself transported back to the very place where your adventure began.\n\nYou have been teleported back to the starting point.`);
                setTimeout(() => {
                    if (gamestate) {
                        next_cell = {
                            'x': gameSettings.sx,
                            'y': gameSettings.sy
                        }
                        prompt(next_cell, debug);
                    }
                }, 1000);
            } else if (chestResult == 2) {
                console.log(`Inside the chest, you find an unknown potion. As you drink the potion, you feel a sudden jolt of pain.\n\nYou have lost one heart.`)
                remainingLives--;
                if (remainingLives == 0) {
                    console.log("Game Over!");
                    rl.question('Do you want to play again? (y/n)', (answer) => {
                        if (answer.toLowerCase() === 'y') {
                            remainingLives = lives;
                            current = {
                                'x': gameSettings.sx,
                                'y': gameSettings.sy
                            };
                            return prompt(current, debug);
                        } else {
                            rl.close();
                        }
                    });
                    gamestate = false;
                    return;
                } else {
                    console.log(`\nYou have ${remainingLives} hearts remaining.\n`);
                    prompt(next_cell, debug); // prompt again with the same cell
                }   
            } else if (chestResult == 3) {
                if(remainingLives == lives) {
                    console.log(`Inside the chest, you find an unknown potion. You drank the potion, but nothing seemed to happen. You decide to continue on your journey.`);
                    setTimeout(() => {
                        if (gamestate) {
                            current = next_cell;
                            prompt(next_cell, debug);
                        }
                    }, 1000);
                } else {
                    console.log(`Inside the chest, you find an unknown potion. As you drink the potion, you feel a surge of power coursing through your body.\n\nYou have gained one heart.`)
                    remainingLives++;
                    setTimeout(() => {
                        if (gamestate) {
                            current = next_cell;
                            prompt(next_cell, debug);
                        }
                    }, 1000);
                }
            } else if (chestResult == 4) {
                console.log(`The chest was a trap! As soon as you opened it, a huge explosion engulfed you.\n\nYou have lost three hearts.`);
                remainingLives -= 3;
                if (remainingLives <= 0) {
                    console.log("Game Over!");
                    rl.question('Do you want to play again? (y/n)', (answer) => {
                        if (answer.toLowerCase() === 'y') {
                            remainingLives = lives;
                            current = {
                                'x': gameSettings.sx,
                                'y': gameSettings.sy
                            };
                            prompt(current, debug);
                        } else {
                            rl.close();
                        }
                    });
                    gamestate = false;
                    return;
                } else {
                    console.log(`\nYou have ${remainingLives} hearts remaining.\n`);
                    prompt(next_cell, debug); // prompt again with the same cell
                }
            }
        }
        else {
            if (gamestate) {
                current = next_cell;
                prompt(next_cell, debug);
            }
        }
    });
}

function generateCellVisualization(north = true, south = true, west = true, east = true) {
    let result = new String();
    if (north) {
        result += '+—————————+\n|         |\n|         |\n';
    } else {
        result += '+——— ⇑ ———+\n|         |\n|         |\n';
    }

    if (west) {
        result += '|';
    } else {
        result += '⇐';
    }

    if (east) {
        result += '    •    |\n|         |\n|         |\n';
    } else {
        result += '    •    ⇒\n|         |\n|         |\n';
    }

    if (south) {
        result += '+—————————+';
    } else {
        result += '+——— ⇓ ———+';
    }

    return result;
}

let current_cell = {
    'x': gameSettings.sx,
    'y': gameSettings.sy
};

let remainingLives = lives;

if (debug) {
    console.log(maze.cell_at(current_cell.x, current_cell.y));
}
prompt(current_cell, debug);
