#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the queensAttack function below.
def queensAttack(n, k, r_q, c_q, obstacles):
    '''
    n: length & breadth of chess board (rows/cols are from 1:n)
    k: num obstacles
    r_q: row of queen
    c_q: col of queen
    obstacles: array of obstacles
    '''
    num_attacks = 0

    # up/down
    # no obstacles
    if not c_q in map(lambda x: x[1], obstacles):
        # up
        num_attacks += n - r_q
        # down
        num_attacks += r_q - 1
    # obstacles
    else:
        obstacle_up = (n+1, c_q)
        obstacle_down = (0, c_q)
        obs = [i for i in obstacles if i[1] == c_q]
        for obstacle in obs:
            if obstacle[0] > r_q and obstacle[0] < obstacle_up[0]:
                obstacle_up = obstacle
            elif obstacle[0] < r_q and obstacle[0] > obstacle_down[0]:
                obstacle_down = obstacle
        # up
        num_attacks += obstacle_up[0] - r_q - 1
        # down
        num_attacks += r_q - obstacle_down[0] - 1
    print(f'num_attacks UD {num_attacks}')
        
    # left/right
    # no obstacles
    if not r_q in map(lambda x: x[0], obstacles):
        # left
        num_attacks += c_q - 1
        # right
        num_attacks += n - c_q
    # obstacles
    else:
        obstacle_left = (r_q, 0)
        obstacle_right = (r_q, n+1)
        obs = [i for i in obstacles if i[0] == r_q]
        for obstacle in obs:
            if obstacle[1] > c_q and obstacle[1] < obstacle_right[1]:
                obstacle_right = obstacle
            elif obstacle[1] < c_q and obstacle[1] > obstacle_left[1]:
                obstacle_left = obstacle
        # right
        num_attacks += obstacle_right[1] - c_q - 1
        # left
        num_attacks += c_q - obstacle_left[1] - 1
    print(f'num_attacks UD+LR {num_attacks}')

    # diagonals: determine the obstacles in the queens diagonals
    # if the difference between Queen pos and obstacle pos row and col are equal, obstacle is in a diagonal of queen
    # eg queen (6, 3), obstacle (4, 5). Difference = (2, -2). Abs value of difference is equal so obstacle is in queens path
    diag_obstacles = [i for i in obstacles if abs(r_q - i[0]) == abs(c_q - i[1])]

    # boundary coordinates
    dist_UL = min(n+1-r_q, c_q-0)
    obstacle_UL = (r_q+dist_UL, c_q-dist_UL)

    dist_UR = min(n+1-r_q, n+1-c_q)
    obstacle_UR = (r_q+dist_UR, c_q+dist_UR)

    dist_DL = min(r_q-0, c_q-0)
    obstacle_DL = (r_q-dist_DL, c_q-dist_DL)

    dist_DR = min(r_q-0, n+1-c_q)
    obstacle_DR = (r_q-dist_DR, c_q+dist_DR)

    for obs in diag_obstacles:
        # UL
        if obs[0] > r_q and obs[1] < c_q and obs[0] < obstacle_UL[0] and obs[1] > obstacle_UL[1]:
            obstacle_UL = obs
        # UR
        elif obs[0] > r_q and obs[1] > c_q and obs[0] < obstacle_UR[0] and obs[1] < obstacle_UR[1]:
            obstacle_UR = obs
        # DL
        elif obs[0] < r_q and obs[1] < c_q and obs[0] > obstacle_DL[0] and obs[1] > obstacle_DL[1]:
            obstacle_DL = obs
        # DR
        elif obs[0] < r_q and obs[1] > c_q and obs[0] > obstacle_DR[0] and obs[1] < obstacle_DR[1]:
            obstacle_DR = obs

    # add queen moves for diagonals
    num_attacks += obstacle_UL[0] - r_q - 1
    print(f'num_attacks UD+LR+UL {num_attacks}')
    num_attacks += obstacle_UR[0] - r_q - 1
    print(f'num_attacks UD+LR+UL+UR {num_attacks}')
    num_attacks += r_q - obstacle_DL[0] - 1
    print(f'num_attacks UD+LR+UL+UR+DL {num_attacks}')
    num_attacks += r_q - obstacle_DR[0] - 1
    print(f'num_attacks UD+LR+UL+UR+DL+DR {num_attacks}')

    return num_attacks


if __name__ == '__main__':
    nk = input().split()
    n = int(nk[0])
    k = int(nk[1])
    r_qC_q = input().split()
    r_q = int(r_qC_q[0])
    c_q = int(r_qC_q[1])
    obstacles = []
    for _ in range(k):
        obstacles.append(list(map(int, input().rstrip().split())))

    result = queensAttack(n, k, r_q, c_q, obstacles)

'''
sample input
5 3
4 3
5 5
4 2
2 3

output
10


input
7 5
6 3
6 2
4 3
7 5
4 5
3 6

output
11
'''
