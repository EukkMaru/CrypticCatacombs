class Cell {
    static wall_pairs = {
        'N': 'S',
        'S': 'N',
        'E': 'W',
        'W': 'E'
    };

    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.walls = {
            'N': true,
            'S': true,
            'E': true,
            'W': true
        };
    }

    has_all_walls() {
        return Object.values(this.walls).every(wall => wall === true);
    }

    knock_down_wall(other, wall) {
        this.walls[wall] = false;
        other.walls[Cell.wall_pairs[wall]] = false;
    }
}

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

export class Maze {
    constructor(nx, ny, ix = 0, iy = 0) {
        this.nx = nx;
        this.ny = ny;
        this.ix = ix;
        this.iy = iy;
        this.maze_map = Array.from(Array(nx), (col, x) =>
            Array.from(Array(ny), (cell, y) => new Cell(x, y))
        );
    }

    cell_at(x, y) {
        return this.maze_map[x][y];
    }

    toString() {
        let maze_rows = ["—".repeat(this.nx * 2)];
        for (let y = 0; y < this.ny; y++) {
            let maze_row = ["|"];
            for (let x = 0; x < this.nx; x++) {
                if (this.maze_map[x][y].walls["E"]) {
                    maze_row.push(" |");
                } else {
                    maze_row.push("  ");
                }
            }
            maze_rows.push(maze_row.join(""));
            maze_row = ["|"];
            for (let x = 0; x < this.nx; x++) {
                if (this.maze_map[x][y].walls["S"]) {
                    maze_row.push("—+");
                } else {
                    maze_row.push(" +");
                }
            }
            maze_rows.push(maze_row.join(""));
        }
        return maze_rows.join("\n");
    }

    find_valid_neighbours(cell) {
        const delta = [
            ["W", [-1, 0]],
            ["E", [1, 0]],
            ["S", [0, 1]],
            ["N", [0, -1]],
        ];
        let neighbours = [];
        for (let [direction, [dx, dy]] of delta) {
            let [x2, y2] = [cell.x + dx, cell.y + dy];
            if (x2 >= 0 && x2 < this.nx && y2 >= 0 && y2 < this.ny) {
                let neighbour = this.cell_at(x2, y2);
                if (neighbour.has_all_walls()) {
                    neighbours.push([direction, neighbour]);
                }
            }
        }
        return neighbours;
    }

    make_maze() {
        const DIRECTIONS = {
            "N": [0, -1],
            "S": [0, 1],
            "E": [1, 0],
            "W": [-1, 0]
        };
        
        const OPPOSITE = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E"
        };
        
        // Total number of cells.
        let n = this.nx * this.ny;
        let cell_stack = [];
        let current_cell = this.cell_at(this.ix, this.iy);
        // Total number of visited cells during maze construction.
        let nv = 1;

        while (nv < n) {
            let neighbours = this.find_valid_neighbours(current_cell);

            if (neighbours.length === 0) {
                // We've reached a dead end: backtrack.
                current_cell = cell_stack.pop();
                continue;
            }

            // Choose a random neighbouring cell and move to it.
            let [direction, next_cell] = neighbours[
                Math.floor(Math.random() * neighbours.length)
            ];
            current_cell.knock_down_wall(next_cell, direction);
            cell_stack.push(current_cell);
            current_cell = next_cell;
            nv += 1;
        }
        // Get a list of all the cells in the maze except for those on the edges.
        let interior_cells = [];
        for (let x = 1; x < this.nx - 1; x++) {
            for (let y = 1; y < this.ny - 1; y++) {
                interior_cells.push(this.cell_at(x, y));
            }
        }

        // Randomly shuffle the list of interior cells.
        shuffle(interior_cells);

        // Compute the number of walls to knock down (n% of the total number of interior walls).
        let num_walls_to_knock_down = Math.round(interior_cells.length * 4 * 0.1);

        // Loop over the interior cells and knock down walls until the desired number of walls has been knocked down.
        for (let cell of interior_cells) {
            let walls_to_knock_down = [];
            for (let direction of ["N", "S", "E", "W"]) {
                if (!cell.walls[direction]) {
                    continue;
                }
                let [dx, dy] = DIRECTIONS[direction];
                let neighbor = this.cell_at(cell.x + dx, cell.y + dy);
                if (!neighbor) {
                    continue;
                }
                if (!neighbor.has_all_walls()) {
                    walls_to_knock_down.push(direction);
                }
            }
            if (walls_to_knock_down.length > 0 && num_walls_to_knock_down > 0) {
                let direction = walls_to_knock_down[Math.floor(Math.random() * walls_to_knock_down.length)];
                cell.walls[direction] = false;
                let [dx, dy] = DIRECTIONS[direction];
                let neighbor = this.cell_at(cell.x + dx, cell.y + dy);
                neighbor.walls[OPPOSITE[direction]] = false;
                num_walls_to_knock_down--;
            }
            if (num_walls_to_knock_down == 0) {
                break;
            }
        }

    }
}