#!/bin/python

def next_move(rows, cols, k, grid):
    '''
    Purpose: Determine next coordinate to 'pop'

    Params:
    rows: number of rows in grid
    cols: number of columns in grid
    k: number of colours in grid
    grid: the grid
    
    Strategy:
    Priorities:
    1) reduce the number of solo cells to 0, start from bottom left corner

    ALGORITHM
    - while singles:
        if same colour above with poppable inbetween - pop it
        elif same colour up-left with poppable below - pop it
        elif same colour up-right with poppable below - pop it
        elif check if below poppable - pop it
        NB NOTE: fewer diff colours inbetween = higher priority
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

    # produce a list of the number of same colour adjacent cells and it's coordinate
    for i in range(rows):
        for j in range(cols):

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


    # insert bottom left cell to targets list
    target = [rows-1, 0]
    targets.insert(0, target)

    while targets:
        x, y = targets.pop()

        # check if a target is poppable - if yes pop it
        print(f'start {x, y}')
        if is_poppable(x, y, grid):
            print(f'target is poppable {x}, {y}')
            return

        # check if same colour one column to RIGHT and ABOVE target - pop poppable cell inbetween
        elif find_x_above_right(x, y, grid):
            print(f'target RIGHT is poppable {x}, {y}')
            return

        # check if same colour one column to LEFT and ABOVE target - pop poppable cell inbetween
        elif find_x_above_left(x, y, grid):
            print(f'target LEFT is poppable {x}, {y}')
            return

        # check if same colour ABOVE target - pop poppable cell inbetween
        elif find_x_above(x, y, grid):
            print(f'target ABOVE is poppable {x}, {y}')
            return

        # check if same colour BELOW target - pop poppable cell inbetween
        elif find_x_below(x, y, grid):
            print(f'target BELOW is poppable {x}, {y}')
            return

        # add above and right cells to targets list
        # above
        if (x > 0) and (grid[x-1][y] in colour_list):
            targets.insert(0, [x-1, y])

        # right
        if (y < cols-1) and (grid[x][y+1] in colour_list):
            targets.insert(0, [x, y+1])


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
    return (x < rows) and (x > 0) and (y < cols) and (y > 0)


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

        x_above -= 1

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
