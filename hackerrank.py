'''
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


output
RIGHT
...
'''
import copy

def next_move(pos_r, pos_c, board):
    '''
    purpose: Determine next move to get agent closer to target
    '''

    # agent position
    agent = [pos_r, pos_c]
    
    # target position
    final_target = []
    min_dist = int(1e10)
    for row in range(len(board)):
        for col in range(len(board[0])):
            # cell is dirty
            if board[row][col] == 'd':
                target = [row, col]
                dist = physical_distance(agent, target)
                if dist < min_dist:
                    min_dist = dist
                    final_target = target

    # assign a direction to each cell, due to sensing edge cells will be checked
    # d d l l l
    # d d l l l
    # d d l u u
    # r r r u u
    # r r r u u
    if not final_target:

        final_target = copy.deepcopy(agent)

        # move DOWN (first 3 rows AND first 2 columns)
        if (agent[0] in range(3)) and (agent[1] in range(2)):
            final_target[0] += 1        # DOWN

        # move RIGHT (last 2 rows AND first 3 columns)
        if (agent[0] in range(3,5)) and (agent[1] in range(3)):
            final_target[1] += 1        # RIGHT

        # move UP (last 3 rows AND last 2 columns)
        if (agent[0] in range(2,5)) and (agent[1] in range(3,5)):
            final_target[0] -= 1        # UP

        # move LEFT (first 2 rows AND last 3 columns)
        if (agent[0] in range(3)) and (agent[1] in range(2,5)):
            final_target[1] -= 1        # LEFT

        # move LEFT if middle block
        if (agent[0] == 2) and (agent[1] == 2):
            final_target[1] -= 1        # LEFT

    # move agent to target
    if agent != final_target:
        direction = move(agent, final_target)

    # else if agent is at target, clean
    elif agent == final_target:
        direction = 'CLEAN'
        
    print(direction)


def physical_distance(agent, target):
    '''
    purpose: Physical distance between the agent and target, limited to movements of UP, DOWN, LEFT & RIGHT

    params
    agent: [x, y] coord pair of agents current position
    target: [x, y] coord pair of target position
    '''
    return int((abs(agent[0]-target[0]) + abs(agent[1]-target[1])))


def move(agent, target):
    '''
    purpose: Move agent 1 step closer to target
    '''

    # move UP
    if agent[0] > target[0]:
        agent[0] -= 1
        direction = 'UP'

    # move DOWN
    elif agent[0] < target[0]:
        agent[0] += 1
        direction = 'DOWN'

    # move LEFT
    elif agent[1] > target[1]:
        agent[1] -= 1
        direction = 'LEFT'

    # move RIGHT
    elif agent[1] < target[1]:
        agent[1] += 1
        direction = 'RIGHT'

    return direction


if __name__ == "__main__": 
    pos = [int(i) for i in input().strip().split()] 
    board = [[j for j in input().strip()] for i in range(5)]  
    next_move(pos[0], pos[1], board)