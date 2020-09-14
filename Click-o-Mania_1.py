#!/bin/python

def next_move(rows, cols, colour, grid):
    '''
    Purpose: Determine next coordinate to 'pop'

    Params:
    rows: number of rows in grid
    cols: number of columns in grid
    colour: number of colours in grid
    grid: the grid
    
    Strategy:
    ***1***
    - collect all (colour_count, coord) tuples
    - find top left most solo cell
    - pop coords beneath it, right, left or above it in that order
    - repeat 
    - end if only 1 colour remaining

    ***2***
    try clear bottom left corner
    - pop bottom left if possible, else
      - 
    '''

    active_colour = None
    checked_cells = []
    adjacent_cells = []
    all_coords = []
    colour_list = ["V", "I", "B", "G", "Y", "O", "R"]

    for i in range(rows):
        for j in range(cols):

            # reset colour count
            colour_count = 0

            # check if coord not in checked cells list and is an accepted colour
            if ([i, j] not in checked_cells) and (grid[i][j] in colour_list):
                coord = [i, j]
                active_colour = grid[i][j]
                
                # add coordinate to adjacent cell list to start while loop
                adjacent_cells.append(coord)
                # while adjacent cells list is not empty
                while adjacent_cells:
                    x, y = adjacent_cells.pop()

                    # increment colour_count for each new cell checked
                    colour_count += 1

                    # add current cell to checked cells
                    checked_cells.append([x, y])

                    # append adjacent cells if same colour
                    append_adjacent(adjacent_cells, checked_cells, active_colour, x, y, rows, cols, grid)

                # append all (colour_count, coord) tuples to list
                all_coords.append((colour_count, coord))

    # one colour left over, pop it and end
    if len(all_coords) == 1:
        print(coord[0], coord[1])
        return

    # find top right most solo cell which has a neighbour which can be popped
    n = 1
    while not adjacent_cells and all_coords:

        # find top right most solo cell
        row = 100
        col = cols
        for cnt, coordinate in all_coords:
            if cnt == n:
                if (coordinate[0] < row) or ((coordinate[0] == row) and (coordinate[1] > col)):
                    row = coordinate[0]
                    col = coordinate[1]

        if row == 100:
            n += 1
            continue

        # pop coords beneath selected cell, else right, else left, else above
        # Need to count cells again to see if it can be popped
        for i in range(2):
            adjacent_cells = []
            temp_checked_cells = []
            # beneath
            if (i == 0) and (row < rows-1):
                active_colour = grid[row+1][col]
                x = row + 1
                y = col
            # right
            elif (i == 1) and (col < cols-1):
                active_colour = grid[row][col+1]
                x = row
                y = col + 1
            # left
            elif (i == 2) and (col > 0):
                active_colour = grid[row][col-1]
                x = row
                y = col - 1
            # above
            elif (i == 3) and (row > 0):
                active_colour = grid[row-1][col]
                x = row - 1
                y = col
            else:
                pass

            if (active_colour not in colour_list):
                continue

            append_adjacent(adjacent_cells, temp_checked_cells, active_colour, x, y, rows, cols, grid)
            # if checked cell has matching neighbours, exit loop
            if adjacent_cells:
                break

        # if checked cells have no matching neighbours, remove from list and try next solo cell
        if not adjacent_cells:
            all_coords.remove((n, [row, col]))

    # print coordinate corresponding to max colour count
    print(x, y)

def append_adjacent(adjacent_cells, checked_cells, colour, x, y, rows, cols, grid):
    '''
    Purpose: To append cells of the same colour to the adjacency list

    params
    adjacent_cells: [r, c] coord pair of cells with same colour
    checked_cells: [r, c] coord pair of cells already investigated
    colour: colour to search for in adjacent cells
    x: row in which to search
    y: column in which to search
    '''
    # check DOWN
    if (x+1<rows) and (grid[x+1][y] == colour) and ([x+1, y] not in adjacent_cells) and ([x+1, y] not in checked_cells):
        adjacent_cells.append([x+1, y])

    # check UP
    if (x-1>=0) and (grid[x-1][y] == colour) and ([x-1, y] not in adjacent_cells) and ([x-1, y] not in checked_cells):
        adjacent_cells.append([x-1, y])

    # check RIGHT
    if (y+1<cols) and (grid[x][y+1] == colour) and ([x, y+1] not in adjacent_cells) and ([x, y+1] not in checked_cells):
        adjacent_cells.append([x, y+1])

    # check LEFT
    if (y-1>=0) and (grid[x][y-1] == colour) and ([x, y-1] not in adjacent_cells) and ([x, y-1] not in checked_cells):
        adjacent_cells.append([x, y-1])
    

def get_key(d, val):
    '''
    Purpose: Find the corresponding key for the given value

    Params:
    d: dictionary
    val: value
    '''
    for k, v in d.items():
        if v == val:
            return k

    return None



if __name__ == "__main__": 
    rows, cols, k = [int(i) for i in input().strip().split()]
    grid = [[i for i in input().strip()] for j in range(rows)]
    next_move(rows, cols, k, grid)


'''
sample input
20 10 2
BRBBBBRRBB
RBRBBRRRRR
BRBBRRRBBB
BRRRBBBRBR
BBBBRBRRBR
BRBRRBRRRB
BBRBRBRBBB
RBRBRBRRBR
BRRRRRBBRB
RRRRBRRRRB
BRRRBBBRBR
RRBRRBBBRB
RBBBBBBBBB
BRBBRBRBBR
RBRBBBRRRB
RBRBRBRBBB
BRRRBRBRRR
RRBRBBBBBR
RBBRBBRBRB
BBBBRRBBRB

20 10 6
----------
----------
----------
----------
----------
----------
----------
----------
----------
----------
----------
--------G-
Y-------R-
V------OB-
R--B---OV-
B--B-G-GR-
V-VO-G-OV-
R-VO-Y-GY-
GVVG-V-YB-
VBOGYRGRO-


20 10 5
----------
----------
----------
----------
----------
----------
----------
----------
----------
----------
----------
----------
----------
----------
----------
R---------
G---------
R----GB-B-
YOYOOBY-R-
GYRBRYGYG-

'''
