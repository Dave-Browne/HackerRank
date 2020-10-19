#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'nonDivisibleSubset' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER k
#  2. INTEGER_ARRAY s
#

def nonDivisibleSubset(k, s):
    '''
    Purpose:
    Want the longest subset of list s where any 2 elements of s are not divisible be k
    Therefore (a + b) % k != 0

    Strategy:
    a+b is divisible by k if the sum of the remainders of a/k + b/k = k
    This means we can only keep one of the divisble pairs
    eg if k = 5, divisible pairs are 1-4 and 2-3. Keep 2 or 3 whichever has the highest count
    for all a/k == 0, we can only keep 1 value
    for all a = b = k/2, we can only keep 1 value
    '''
    s = [i % k for i in s]
    a = 1
    b = k-1    
    while b > a:
        if s.count(a) > s.count(b):
            s = [i for i in s if i != b]
        else:
            s = [i for i in s if i != a]

        a += 1
        b -= 1
        
    # case where a/k == 0, can only keep one instance of 0
    if s.count(0):
        s = [i for i in s if i != 0]
        s.append(0)

    # case where a = b, can only keep one instance
    if k % 2 == 0 and s.count(int(k/2)) > 1:
        s = [i for i in s if i != int(k/2)]
        s.append(int(k/2))

    return len(s)


if __name__ == '__main__':

    first_multiple_input = input().rstrip().split()
    n = int(first_multiple_input[0])
    k = int(first_multiple_input[1])
    s = list(map(int, input().rstrip().split()))

    result = nonDivisibleSubset(k, s)


'''
sample input
15 6
278 576 496 727 410 124 338 149 209 702 282 718 771 575 436

sample output
11


hidden case
input
87 9
61197933 56459859 319018589 271720536 358582070 849720202 481165658 675266245 541667092 615618805 129027583 755570852 437001718 86763458 791564527 163795318 981341013 516958303 592324531 611671866 157795445 718701842 773810960 72800260 281252802 404319361 757224413 682600363 606641861 986674925 176725535 256166138 827035972 124896145 37969090 136814243 274957936 980688849 293456190 141209943 346065260 550594766 132159011 491368651 3772767 131852400 633124868 148168785 339205816 705527969 551343090 824338597 241776176 286091680 919941899 728704934 37548669 513249437 888944501 239457900 977532594 140391002 260004333 911069927 586821751 113740158 370372870 97014913 28011421 489017248 492953261 73530695 27277034 570013262 81306939 519086053 993680429 599609256 639477062 677313848 950497430 672417749 266140123 601572332 273157042 777834449 123586826

output
50
'''
