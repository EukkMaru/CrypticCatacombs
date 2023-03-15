from math import floor
from random import random

class Cell:

    wall_pairs = {
        'N': 'S', 
        'S': 'N', 
        'E': 'W', 
        'W': 'E', 
    }

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.walls = {
            'N': True,
            'S': True,
            'E': True,
            'W': True,
        }

    def has_all_walls(self):
        return all(self.walls.values())
    
    def knock_down_wall(self, other, wall):
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


def shuffle(array):
    for i in range(len(array)-1, -1, -1):
        j = floor(random() * (i + 1))

        temp = array[i]
        array[i] = array[j]
        array[j] = temp


class Maze:
    
    def __init__(self, nx, ny, ix=0, iy=0) -> None:
        self.nx = nx
        self.ny = ny
        self.ix = ix
        self.iy = iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    def cell_at(self, x, y):
        return self.maze_map[x][y]
    
    def print_maze(self):
        maze_rows = ["-" * (self.nx * 2)]
        
        for y in range(0, self.ny):
            maze_row = ["|"]

            for x in range(0, self.nx):
                if self.maze_map[x][y].walls["E"]:
                    maze_row.append(" |")
                else:
                    maze_row.append("  ")

            maze_rows.append("".join(maze_row))
            maze_row = ["|"]

            for x in range(0, self.nx):
                if self.maze_map[x][y].walls["S"]:
                    maze_row.append("—+")
                else:
                    maze_row.append(" +")
                
            maze_rows.append("".join(maze_row))
        
        return "\n".join(maze_rows)
    
    def find_valid_neighbours(self, cell):
        delta = [
            ["W", [-1, 0]],
            ["E", [1, 0]],
            ["S", [0, 1]],
            ["N", [0, -1]],
        ]
        neighbours = []

        for [direction, [dx, dy]] in delta:
            [x2, y2] = [cell.x + dx, cell.y + dy]

            if x2 >= 0 and x2 < self.nx and y2 >= 0 and y2 < self.ny:
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append([direction, neighbour])
        
        return neighbours
    
    def make_maze(self):
        DIRECTIONS = {
            "N": [0, -1],
            "S": [0, 1],
            "E": [1, 0],
            "W": [-1, 0], 
        }
        OPPOSITE = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E", 
        }

        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)
            if len(neighbours) == 0:
                current_cell = cell_stack.pop()
                continue

            [direction, next_cell] = neighbours[floor(random() * len(neighbours))]

            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1

        interior_cells = []
        for x in range(1, self.nx-1):
            for y in range(1, self.ny-1):
                interior_cells.append(self.cell_at(x, y))

        shuffle(interior_cells)

        num_walls_to_knock_down = round(len(interior_cells) * 4 * 0.1)

        for cell in interior_cells:
            walls_to_knock_down = []
            for direction in ["N", "S", "E", "W"]:
                if not cell.walls[direction]:
                    continue
                [dx, dy] = DIRECTIONS[direction]
                neighbor = self.cell_at(cell.x + dx, cell.y + dy)
                if not neighbor:
                    continue
                if not neighbor.has_all_walls():
                    walls_to_knock_down.append(direction)
            
            if len(walls_to_knock_down) > 0 and num_walls_to_knock_down > 0:
                direction = walls_to_knock_down[floor(random() * len(walls_to_knock_down))]
                cell.walls[direction] = False
                [dx, dy] = DIRECTIONS[direction]
                neighbor = self.cell_at(cell.x + dx, cell.y + dy)
                neighbor.walls[OPPOSITE[direction]] = False
                num_walls_to_knock_down -= 1

            if num_walls_to_knock_down == 0:
                break