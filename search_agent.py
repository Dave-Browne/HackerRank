
'''
purpose
Agent is 'b'. Agent's purpose is to clean dirty cells, represented by 'd'. 
Agent can move UP DOWN LEFT RIGHT or CLEAN, each which take 1 move.
Clean cells are represented by '-'
Cells can either all be visible or masked by an 'o' - in which case agent will explore and clean them

input
0 0
b-ooo
-dooo
ooooo
ooooo
ooooo


2 1
ooooo
---oo
-b-oo
---oo
ooooo


2 1
d--d-
-d---
dbd-d
--d-d
-dd--
'''

class agent():
    '''
    The agent is tasked to reach a target
    '''

    def __init__(self, pos_r, pos_c):
        '''
        params
        pos: [x, y] or [row, col] coord pair of agents current position
        targets: list of all coord pairs of targets
        target: coord pair of current target
        path: list of coord pairs of path taken by agent
        checked_cells: list of coord pairs checked by agent for target
        distance: distance to next target
        cost: cost function
        '''
        
        self.pos = [pos_r, pos_c]
        self.targets = []
        self.target = None
        self.path = []
        self.checked_cells = []
        self.distance = int(1e10)
        self.cost = 0


    def next_move(self, board):
        '''
        purpose: Determine next move to get agent closer to target
        '''
        
        # find targets, assign closest target
        # populate checked cells
        # NOTE: this method continuously checks for a closer target whereas we might want to keep a single target until it is cleaned, and then move to the next target
        for row in range(len(board)):
            for col in range(len(board[0])):

                # cell is dirty, check distance
                if board[row][col] == 'd':
                    target = [row, col]
                    # add dirty cell to targets list
                    if target not in self.targets:
                        self.targets.append(target)
                    # add dirty cell to checked_cells list
                    if target not in self.checked_cells:
                        self.checked_cells.append(target)
                    # get distance
                    dist = self.physical_distance(target)
                    if dist < self.distance:
                        self.distance = dist
                        self.target = target

                # cell is NOT checked AND (cell is clean OR cell is agent), add to checked_cells
                elif [row, col] not in self.checked_cells and (board[row][col] == '-' or board[row][col] == 'b'):
                    self.checked_cells.append([row, col])

        print(f'PRE MOVE  pos {self.pos}, target {self.target}, distance {self.distance}, path {self.path}, checked_cells {self.checked_cells}, targets {self.targets}')

        # if no dirty square is visible then take the last detected target
        # NOTE: this is not necessarily the closest one in targets list, but is easier to code
        if not self.target and len(self.targets) > 0:
            self.target = self.targets.pop()

        # if no dirty square is visible and none in the targets list, move towards unchecked cells
        elif not self.target and len(self.targets) == 0:
            for row in range(len(board)):
                for col in range(len(board[0])):
                    if [row, col] not in self.checked_cells:
                        dist = self.physical_distance([row, col])
                        if dist < self.distance:
                            self.distance = dist
                            self.target = [row, col]

        # move agent to target
        if self.pos != self.target:
            self.move()

        # else if agent is at target, clean
        elif self.pos == self.target:
            self.path.append('CLEAN')
            self.reset()

        print(self.path[-1])
        self.update_board(board)
        self.print_board(board)


    def physical_distance(self, target):
        '''
        purpose: Physical distance between the agent and target, limited to movements of UP, DOWN, LEFT & RIGHT
        '''
        return (abs(self.pos[0]-target[0]) + abs(self.pos[1]-target[1]))


    def move(self):
        '''
        purpose: Move agent 1 step closer to target
        '''

        # move UP
        if self.pos[0] > self.target[0]:
            self.pos[0] -= 1
            self.path.append('UP')

        # move DOWN
        elif self.pos[0] < self.target[0]:
            self.pos[0] += 1
            self.path.append('DOWN')

        # move LEFT
        elif self.pos[1] > self.target[1]:
            self.pos[1] -= 1
            self.path.append('LEFT')

        # move RIGHT
        elif self.pos[1] < self.target[1]:
            self.pos[1] += 1
            self.path.append('RIGHT')


    def reset(self):
        '''
        purpose: Reset parameters to search for a new target
        '''
        # remove target from list once it has been found
        self.targets.remove(self.target)
        self.target = []
        self.distance = int(1e10)


    def update_board(self, board):
        '''
        purpose: Update board after an action is taken
        '''
        # update previous agent position
        if self.path[-1] == 'UP':
            board[self.pos[0]+1][self.pos[1]] = '-'

        elif self.path[-1] == 'DOWN':
            board[self.pos[0]-1][self.pos[1]] = '-'

        elif self.path[-1] == 'LEFT':
            board[self.pos[0]][self.pos[1]+1] = '-'

        elif self.path[-1] == 'RIGHT':
            board[self.pos[0]][self.pos[1]-1] = '-'

        # update new agent position
        elif self.path[-1] == 'CLEAN':
            board[self.pos[0]][self.pos[1]] = 'b'

        if self.path[-1] != 'CLEAN' and board[self.pos[0]][self.pos[1]] == '-':
            board[self.pos[0]][self.pos[1]] = 'b'

            
    def print_board(self, board):
        '''
        purpose: Print the board
        '''
        print()
        for row in board:
            for char in row:
                print(char, end='')
            print()


if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(5)]
    my_agent = agent(pos[0], pos[1])

    # loop through board until all dirty cells 'd' have been cleaned OR there are unexplored cells 'o'
    while (sum([row.count('d') for row in board]) > 0) or (sum([row.count('o') for row in board]) > 0):
        my_agent.next_move(board)

    # cost - according to hackerrank scoring
    my_agent.cost = (200 - len(my_agent.path)) / 25
    print(f'cost to clean board: {my_agent.cost} out of 8')