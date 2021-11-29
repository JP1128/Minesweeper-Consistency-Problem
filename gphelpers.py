# -*- coding: utf-8 -*-
import copy

import numpy as np

"""
Made to reduce the amount of math calls.
Takes the denumerated cords and renumerates them.
This is necessary for tuples
"""


def cordadjust(mines, y):
    mn = []

    for x in mines:
        mn.append(((x // y), (x % y)))

    return mn



"""
Using the minefield generator that JP made, this function 
adjusts it to differentiate between the empty cells
near numbered-cell adjacent cells (-2), and empty not near
numbered-cells (0). This also gets the cords for 0 and -2
"""

def dummymf(mf):
    md = np.array(mf, copy=True)
    cords = []
    i = 0
    x = len(md)
    y = len(md[0])
    while i < x:
        j = 0
        while j < y:

            if md[i][j] == 0:
                # tl
                if ((i - 1) >= 0) and ((j - 1) >= 0):
                    if md[i - 1][j - 1] > 0:
                        md[i][j] = -2
                # tc
                if (i - 1) >= 0:
                    if md[i - 1][j] > 0:
                        md[i][j] = -2
                # tr
                if ((i - 1) >= 0) and ((j + 1) < y):
                    if md[i - 1][j + 1] > 0:
                        md[i][j] = -2
                # left
                if (j - 1) >= 0:
                    if md[i][j - 1] > 0:
                        md[i][j] = -2
                # right
                if (j + 1) < y:
                    if md[i][j + 1] > 0:
                        md[i][j] = -2
                # bl
                if ((i + 1) < x) and ((j - 1) >= 0):
                    if md[i + 1][j - 1] > 0:
                        md[i][j] = -2
                # bc
                if ((i + 1) < x):
                    if md[i + 1][j] > 0:
                        md[i][j] = -2
                # br
                if ((i + 1) < x) and ((j + 1) < y):
                    if md[i + 1][j + 1] > 0:
                        md[i][j] = -2
                cords.append((i, j))
            j = j + 1
        i = i + 1


    return md, cords
