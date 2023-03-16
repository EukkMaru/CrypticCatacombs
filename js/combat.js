import readline from 'readline';

function generateHitbox(length, layer, hitChance = 3) {
    length *= 1;
    layer *= 1;
    hitChance *= 1;

    function wrap(string, head, tail) {
        return `${head} ${string} ${tail}`;
    }

    function randomizeMap(size = length, difficulty = hitChance) {
        let key = "-".repeat(size);
        const maxIndex = size - difficulty + 1;
        const startIndex = Math.floor(Math.random() * maxIndex);
        key = key.substring(0, startIndex) + "+".repeat(difficulty) + key.substring(startIndex + difficulty);
        return key;
    }

    function animate(source) {
        let result = [];
        for (let i = 0; i < source.length; i++) {
            let chars = source.split('');
            chars[i] = '|';
            result.push(chars.join(''));
        }
        return result;
    }

    let recursion = {};
    for (let i = 0; i < layer; i++) {
        let map = randomizeMap(length, hitChance);
        recursion[i] = {
            'Map': wrap(map, '[', ']'),
            'Marker': animate(map).map(marker => wrap(marker, '[', ']'))
        };
    }

    return recursion;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function animateHitbox(recursion, delay = 50) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
        terminal: false
    });

    let freeze = [];
    let freezeIndex = [];
    for (let i = 0; i < Object.keys(recursion).length; i++) {
        freeze.push(false);
        freezeIndex.push(0);
    }

    let freezeCount = 0;

    rl.on('line', () => {
        if (freezeCount < freeze.length) {
            freeze[freezeCount] = true;
            freezeIndex[freezeCount] = (index - 1 + recursion[freezeCount].Marker.length) % recursion[freezeCount].Marker.length;
            freezeCount++;
        } else {
            freezeCount++;
        }
    });

    let index = 0;

    async function printFrames() {
        console.clear();
        console.log('\n'.repeat(6));
        for (const layer in recursion) {
            if (!freeze[layer]) {
                console.log(recursion[layer].Marker[index]);
            } else {
                console.log(recursion[layer].Marker[freezeIndex[layer]]);
            }
        }
    }

    while (freezeCount < freeze.length) {
        await printFrames();
        index = (index + 1) % recursion[0].Marker.length;
        await sleep(delay);
    }

    await printFrames();

    rl.close();

    // Collect the last frame of each layer
    const finalFrames = Object.keys(recursion).map(layer => {
        return recursion[layer].Marker[freezeIndex[layer]];
    });

    // Concatenate the frames into a single string
    const finalState = finalFrames.join('\n');

    return finalState;
}



// Example usage:
(async () => {
    const recursion = generateHitbox(10, 3, 3);
    const finalState = await animateHitbox(recursion);

    const originalMaps = Object.keys(recursion).map(layer => {
        return recursion[layer].Map;
    }).join('\n');

    const countPlus = (str) => {
        return (str.match(/\+/g) || []).length;
    };

    const originalPlusCount = countPlus(originalMaps);
    const finalPlusCount = countPlus(finalState);
    const difference = originalPlusCount - finalPlusCount;

    // console.log('Original Maps:\n', originalMaps);
    // console.log('Final Frozen State:\n', finalState);
    console.log(`You have dealt ${difference} damage!`);
})();