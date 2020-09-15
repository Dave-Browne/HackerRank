#!/bin/python

from math import ceil


def next_move(rows, cols, k, grid):
    '''
    Purpose: Determine next coordinate to 'pop'

    Params:
    rows: number of rows in grid
    cols: number of columns in grid
    k: number of colours in grid
    grid: the grid
    
    Strategy:
    PRIORITIES
    1) Keep the columns at level heights
    2) Reduce the number of solo cells, start with the tallest column to shortest column, from bottom row to top

    ALGORITHM
    - while single cells:
        NB NOTE: fewer diff colours inbetween = higher priority
      - if same colour above single cell with poppable cell inbetween - pop it
        elif same colour up-left with poppable below - pop it
        elif same colour up-right with poppable below - pop it
        elif check if below poppable - pop it
      - pop from top right to bottom left

    problem: look out for solo cells ontop of each other at the top of a pile - resolve them
    '''

    target = []
    targets = []
    all_coords = []
    checked_cells = []
    empty_checked_cells = []
    adjacent_same_colour = []
    colour_list = ["V", "I", "B", "G", "Y", "O", "R"]
    colour = None

    # list of columns and their heights [column, height]
    heights = []
    for col in range(cols):
        for row in range(rows):
            if grid[row][col] in colour_list:
                heights.append([col, rows-row])
                break

    # sort according to heights (increasing)
    heights_sorted = sorted(heights, key=lambda x: x[1])

    # create list of columns in increasing height order
    columns_sorted = []
    for i in heights_sorted:
        columns_sorted.append(i[0])

    # create list of columns in decreasing height
    columns_sorted.reverse()

    # produce a list of the number of same colour adjacent cells and it's coordinate
    # process from tallest column to shortest column, bottom row to top row
    for j in columns_sorted:
        for i in range(rows-1, -1, -1):

            # reset colour count
            colour_count = 0

            # check if coord not in checked cells list and is an accepted colour
            if ([i, j] not in checked_cells) and (grid[i][j] in colour_list):

                target = [i, j]

                # add target to adjacent cell list to start while loop
                adjacent_same_colour.append(target)
                # while adjacent cells list is not empty
                while adjacent_same_colour:
                    x, y = adjacent_same_colour.pop()

                    # increment colour_count for each new cell checked
                    colour_count += 1

                    # add current cell to checked cells
                    checked_cells.append([x, y])

                    # append adjacent cells if same colour
                    append_adjacent(x, y, grid, adjacent_same_colour, checked_cells)

                # append all (colour_count, coord) tuples to list
                all_coords.append((colour_count, target))

    # find solo cells
    for cnt, coordinate in all_coords:
        if cnt == 1:
            x = coordinate[0]
            y = coordinate[1]

            # insert single cell instances into targets list
            targets.insert(0, [x, y])

    # ALGORITHM
    while targets:
        x, y = targets.pop()

        print(f'start {x} {y}')
        # check if popping 1 cell above removes solo cell
        if clear_solo_cell(x, y, x-2, y, grid):
            print(f'target 1 above poppable {x}, {y}')
            return

        # check if popping 1 cell left removes solo cell
        elif clear_solo_cell(x, y, x-1, y-1, grid):
            print(f'target 1 left is poppable {x}, {y}')
            return

        # check if popping 1 cell right removes solo cell
        elif clear_solo_cell(x, y, x-1, y+1, grid):
            print(f'target 1 right is poppable {x}, {y}')
            return

        # check if same colour ABOVE target - pop poppable cell inbetween
        elif find_x_above(x, y, grid):
            print(f'target ABOVE is poppable {x}, {y}')
            return

        # check if same colour one column to LEFT and ABOVE target - pop poppable cell inbetween
#        elif find_x_above_left(x, y, grid):
#            print(f'target LEFT is poppable {x}, {y}')
#            return

        # check if same colour one column to RIGHT and ABOVE target - pop poppable cell inbetween
#        elif find_x_above_right(x, y, grid):
#            print(f'target RIGHT is poppable {x}, {y}')
#            return

        # check if same colour BELOW target - pop poppable cell inbetween
        elif pop_below(x, y, grid):
            print(f'target BELOW is poppable {x}, {y}')
            return

        # append left and right cells to list
#        if is_valid(x, y-1, rows, cols) and grid[x][y-1] in colour_list and [x, y-1] not in targets:
#            targets.insert(0, [x, y-1])
#        if is_valid(x, y+1, rows, cols) and grid[x][y+1] in colour_list and [x, y+1] not in targets:
#            targets.insert(0, [x, y+1])

    # pop from top right to bottom left
    for i in range(rows):
        for j in range(cols-1, -1, -1):

            if grid[i][j] in colour_list and is_poppable(i, j, grid):
                return


def is_poppable(x, y, grid):
    '''
    Purpose: Check if a target is poppable - if yes pop it

    Params:
    x, y: coordinate pair of target cell

    Return:
    True if poppable, otherwise False
    '''

    has_adjacent_same_colour = []

    # append adjacent cells if same colour
    append_adjacent(x, y, grid, has_adjacent_same_colour)

    # target is poppable
    if has_adjacent_same_colour:
        print(x, y)
        return True

    return False


def append_adjacent(x, y, grid, adjacent_cells=[], checked_cells=[]):
    '''
    Purpose: To append cells of the same colour to the adjacency list

    Params:
    x: row in which to search
    y: column in which to search
    grid: the grid
    adjacent_cells: [r, c] coord pair of cells with same colour
    checked_cells: [r, c] coord pair of cells already investigated
    '''

    rows = len(grid)
    cols = len(grid[0])
    colour = grid[x][y]

    # check DOWN
    if (x+1<rows) and (grid[x+1][y] == colour) and ([x+1, y] not in adjacent_cells) and ([x+1, y] not in checked_cells):
        adjacent_cells.append([x+1, y])

    # check UP
    if (x-1>=0) and (grid[x-1][y] == colour) and ([x-1, y] not in adjacent_cells)  and ([x-1, y] not in checked_cells):
        adjacent_cells.append([x-1, y])

    # check RIGHT
    if (y+1<cols) and (grid[x][y+1] == colour) and ([x, y+1] not in adjacent_cells)  and ([x, y+1] not in checked_cells):
        adjacent_cells.append([x, y+1])

    # check LEFT
    if (y-1>=0) and (grid[x][y-1] == colour) and ([x, y-1] not in adjacent_cells)  and ([x, y-1] not in checked_cells):
        adjacent_cells.append([x, y-1])


def is_valid(x, y, rows, cols):
    '''
    Purpose: Determine if cell is a valid coordinate in the grid

    Params:
    x, y: coordinate pair of target cell

    Return:
    True if valid, otherwise False
    '''
    return (x < rows) and (x >= 0) and (y < cols) and (y >= 0)


def is_same_colour(x1, y1, x2, y2, grid):
    '''
    Purpose: Determine if two cells are the same colour

    Params:
    [x1, y1]: coordinate pair of cell 1
    [x2, y2]: coordinate pair of cell 2

    Return:
    True if colours are the same, otherwise False
    '''
    return grid[x1][y1] == grid[x2][y2]


def clear_solo_cell(x, y, x2, y2, grid):
    '''
    Purpose: Check if original cell & target cell have same colour and pop cell inbetween if possible
             Designed for the following target cells (up two / up one left one / up one right one / down two)

    Params:
    x, y: coordinate pair of the original cell
    x2, y2: coordinate pair of either -> cell up two / up one left one / up one right one / down two

    Return: True if there is a poppable cell (it will be printed by is_poppable), otherwise False
    '''

    rows = len(grid)
    cols = len(grid[0])

    if is_valid(x2, y2, rows, cols) and is_same_colour(x, y, x2, y2, grid):
        
        # x3 must be calculated because x2 can be above or below x
        x3 = ceil((x + x2) / 2)
        
        return is_poppable(x3, y2, grid)

    return False


def find_x_above(x, y, grid):
    '''
    Purpose: Determine which cell ABOVE the target cell is the same colour
             and if there are poppable cells inbetween.
             if there is a poppable cell, pop it

    Params:
    x, y: coordinate pair of target cell

    Return:
    True if there is a poppable cell (it will be printed by is_poppable), otherwise False
    '''

    rows = len(grid)
    cols = len(grid[0])

    x_above = x - 2
    while is_valid(x_above, y, rows, cols):

        # check for colour match
        if is_same_colour(x, y, x_above, y, grid):

            # check for poppable cells inbetween
            if is_poppable(x_above+1, y, grid):
                return True
            else:
                return False

        x_above -= 1

    return False


def find_x_below(x, y, grid):
    '''
    Purpose: Determine which cell BELOW the target cell is the same colour
             and if there are poppable cells inbetween.
             if there is a poppable cell, pop it

    Params:
    x, y: coordinate pair of target cell

    Return:
    True if there is a poppable cell (it will be printed by is_poppable), otherwise False
    '''

    rows = len(grid)
    cols = len(grid[0])

    x_below = x + 2
    while is_valid(x_below, y, rows, cols):

        # check for colour match
        if is_same_colour(x, y, x_below, y, grid):

            # check for poppable cells inbetween
            if is_poppable(x_below-1, y, grid):
                return True
            else:
                return False

        x_below += 1

    return False


def find_x_above_right(x, y, grid):
    '''
    Purpose: Determine which cell ABOVE the target cell and one column to the RIGHT
             is the same colour and if there are poppable cells below it.
             if there is a poppable cell, pop it

    Params:
    x, y: coordinate pair of target cell

    Return:
    True if there is a poppable cell (it will be printed by is_poppable), otherwise False
    '''

    rows = len(grid)
    cols = len(grid[0])

    x_above = x - 1
    y_right = y + 1

    while is_valid(x_above, y_right, rows, cols):

        # check for colour match
        if is_same_colour(x, y, x_above, y_right, grid):

            # check for poppable cells inbetween
            if is_poppable(x_above+1, y_right, grid):
                return True
            else:
                return False

        x_above -= 1

    return False


def find_x_above_left(x, y, grid):
    '''
    Purpose: Determine which cell ABOVE the target cell and one column to the LEFT
             is the same colour and if there are poppable cells below it.
             if there is a poppable cell, pop it

    Params:
    x, y: coordinate pair of target cell

    Return:
    True if there is a poppable cell (it will be printed by is_poppable), otherwise False
    '''

    rows = len(grid)
    cols = len(grid[0])

    x_above = x - 1
    y_left = y - 1

    while is_valid(x_above, y_left, rows, cols):

        # check for colour match
        if is_same_colour(x, y, x_above, y_left, grid):

            # check for poppable cells inbetween
            if is_poppable(x_above+1, y_left, grid):
                return True
            else:
                return False

        x_above -= 1

    return False


def pop_below(x, y, grid):
    '''
    Purpose: Determine if a cell BELOW the target cell is poppable - pop it

    Params:
    x, y: coordinate pair of target cell

    Return:
    True if there is a poppable cell (it will be printed by is_poppable), otherwise False
    '''

    rows = len(grid)
    cols = len(grid[0])

    x_below = x + 1
    while is_valid(x_below, y, rows, cols):

        # check for poppable cells
        if is_poppable(x_below, y, grid):

                return True

        x_below += 1

    return False


if __name__ == "__main__": 
    rows, cols, k = [int(i) for i in input().strip().split()]
    grid = [[i for i in input().strip()] for j in range(rows)]
    next_move(rows, cols, k, grid)


'''
sample input
~~~~~~~~~~~~
Game 1
~~~~~~~~~~~~
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

~~~~~~~~~~~~
Game 2
~~~~~~~~~~~~
20 10 3
BBRBYBBRRB
YBYBYBRRBB
YYRRYYYBBB
YRRRYRBBBB
RRRYYBYYYR
YBBYYRYYBB
RRYRYYBRBY
RRRRYRYYRY
BRRYYRRYYB
RRYRBBBRRY
RBYBYRYYRR
BYBYYBRYBY
BRRBRYRYRB
RBYRRYBYYY
BRYYRYRRBY
BRRYYBYRBY
YBYYBYBBYB
RBYYRRYBRB
BYYBYYRBYB
YBRBYYRRRR

~~~~~~~~~~~~
Game 3
~~~~~~~~~~~~
20 10 5
OBYRORBYGB
YYRGOBRBYB
BOYGYRYOYR
GYYOGYOBBY
GOBGGYOGRR
OBBRBOYRBB
RRGYBRBGOY
GRYRGYGGOR
YOBOOGOBGG
YRBOGYBBGG
RRGOYBYYYY
YBBRBBRGGG
RGBYYBBRGY
YBYOBRBOGG
OBYGOGROOR
RGBOORBBBR
GOGOBRORGG
GGYBOBYRGB
YBYORYGBOR
GYROOOOBOG

~~~~~~~~~~~~
Game 3 - state 2
~~~~~~~~~~~~
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

~~~~~~~~~~~~
Game 4
~~~~~~~~~~~~
20 10 6
BGOBVBGROB
YBYBVGRRGG
VYOOYYYBBB
VRRRVOBGBG
OOOVYBYYVR
VGBYYOYYGB
OOYOYVGOBV
ROROYOYYOY
BRRYYROVYB
RRYRBGGRRV
OGYGVOVYOR
GYBYYBOVGV
GOOBOVOVOB
OGVORVGVVY
GOYVOVRRGV
GORVYBYOBV
VGYYBYBGYG
RGVYOOVBOG
GVVGVVRBYB
VBOBYYOORO

~~~~~~~~~~~~
Game 4 - state 2
~~~~~~~~~~~~
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
'''
