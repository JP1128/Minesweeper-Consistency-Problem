# -*- coding: utf-8 -*-
import random

import numpy as np
import copy

"""
Let me preface by saying the tree functions 
are not what we want yet. They just take cords.
They are what they are now because I needed some
checks to test the funciton
"""


class gpfunctions:

    def __init__(self):

        self.minefield = None
        self.x = 0
        self.y = 0
        self.cord = (0, 0)
        self.tl = False
        self.tc = False
        self.tr = False
        self.lc = False
        self.rc = False
        self.bl = False
        self.bc = False
        self.br = False

    """
    This function is meant to reset the checks between each call.
    If we use weights and record counts, reset counts here.
    """

    def setChecks(self):
        self.tl = False
        self.tc = False
        self.tr = False
        self.lc = False
        self.rc = False
        self.bl = False
        self.bc = False
        self.br = False

    """
    Utility function, helps thegp  functions return a value. 
    Made a function to reduce bloat.
    """

    def retHelper(self, cd1, cd2, x1c, x2c):

        rval = None
        if x1c == x2c:
            s = random.randrange(0,2)
            if s==0:
                rval = cd1
            else:
                rval = cd2
        elif x1c:
            rval = cd1
        elif x2c:
            rval = cd2
        return rval

    """
    Sets the minefield. 
    """

    def setMinefield(self, mf):
        self.minefield = np.array(mf, copy=True)
        self.x, self.y = mf.shape

    """
    Sets the cord we want to check against to see
    if it can hold a mine.
    """

    def setCord(self, cd):
        self.cord = copy.copy(cd)

    """
    Utility function, makes sure that any offset is within bounds of the array. 
    Returns true if in bounds, false otherwise.
    """

    def boundCheck(self, cd):
        # print(cd)
        # print(self.cord)
        if (self.cord[0] + cd[0]) < len(self.minefield) and (self.cord[1] + cd[1]) < len(self.minefield[0]):
            return True
        return False

    """
    The intention is that this function will return if a true or false value
    based on what is found with the other functions. This 
    wont be necessary to make the trees have varying functions but 
    this can be used if we do a flag system or a weighted choice system.
    Result is randomly true or false as issues occured with testing where
    everything was 0 fitness.
    """

    def getResult(self):
        return self.minefield

    # every function below this line should be a primitive
    """
    Checks for an 8 cell in either of the cords.
    In the case the either of the cords are 8 and
    are near the super cord, sets the nearEight
    check to True. Returns offsets for 8 cells,
    otherwise random.
    """

    def eightCheck(self, cd1, cd2):
        x1c = False
        x2c = False
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if self.minefield[x][y] == 8:
                x1c = True
                if abs(cd1[0]) <= 1 and abs(cd1[1]) <= 1:
                    self.minefield[self.cord[0]][self.cord[1]] = -1
        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if self.minefield[x][y] == 8:
                x1c = True
                if abs(cd2[0]) <= 1 and abs(cd2[1]) <= 1:
                    self.minefield[self.cord[0]][self.cord[1]] = -1
        return self.retHelper(cd1, cd2, x1c, x2c)

    """
    Checks if the offsets lead to empty cells.
    If the offsets being checked is empty and 
    next to the current cell, nearEmpty = True.
    Returns emptyCord if either are or random.
    """

    def emptyCheck(self, cd1, cd2):
        x1c = False
        x2c = False
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if self.minefield[x][y] == 0 or self.minefield[x][y] == -2:
                if abs(cd1[0]) <= 1 and abs(cd1[1]) <= 1:
                    self.minefield[self.cord[0]][self.cord[1]] = 0
                x1c = True
        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if (self.minefield[x][y] == 0 or self.minefield[x][y] == -2):
                if abs(cd1[0]) <= 1 and abs(cd1[1]) <= 1:
                    self.minefield[self.cord[0]][self.cord[1]] = 0
                x2c = True
        return self.retHelper(cd1, cd2, x1c, x2c)

    """
    Checks if cord is a direct neighbor, returns cord if is.
    Random if both are or both arent.
    """

    def neighborCheck(self, cd1, cd2):
        x1c = False
        x2c = False
        if self.boundCheck(cd1):
            if abs(cd1[0]) < 2 and abs(cd1[1]) < 2:
                x1c = True
        if self.boundCheck(cd2):
            if abs(cd2[0]) < 2 and abs(cd2[1]) < 2:
                x2c = True
        return self.retHelper(cd1, cd2, x1c, x2c)

    """
    Checks if cord is a outer neighbor, meaning that they are
    located on the just outer 'circle' of the cord.
    """

    def outerNeighborCheck(self, cd1, cd2):
        x1c = False
        x2c = False
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if ((abs(cd1[0]) + abs(cd1[1]) > 1) and (abs(cd1[0]) + abs(cd1[1]) < 5)) and not (
                    abs(cd1[0]) == 1 and abs(cd1[1]) == 1):
                x1c = True
        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if ((abs(cd2[0]) + abs(cd2[1]) > 1) and (abs(cd2[0]) + abs(cd2[1]) < 5)) and not (
                    abs(cd2[0]) == 1 and abs(cd2[1]) == 1):
                x1c = True
        return self.retHelper(cd1, cd2, x1c, x2c)

    def numCheck(self, cd1, cd2):
        x1c = True
        x2c = True
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if self.minefield[x][y] > 0:
                x1c = False
            elif abs(cd1[0]) + abs(cd1[1]) < 3 and self.minefield[self.cord[0]][self.cord[1]] < -3:
                self.minefield[self.cord[0]][self.cord[1]] = -3
                x1c = False
        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if self.minefield[x][y] > 0:
                x2c = False
            elif abs(cd2[0]) + abs(cd2[1]) < 3 and self.minefield[self.cord[0]][self.cord[1]] < -3:
                self.minefield[self.cord[0]][self.cord[1]] = -3
                x2c = False
        return self.retHelper(cd1, cd2, x1c, x2c)

    """
    Checks if either offsets to a cell that might possibly have a mine.
    If that 
    """

    def unknownCheck(self, cd1, cd2):
        x1c = False
        x2c = False
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if self.minefield[x][y] <= 2:
                x1c = True

        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if self.minefield[x][y] <= 2:
                x2c = True

        return self.retHelper(cd1, cd2, x1c, x2c)

    """
    Checks if either of the offset is a numbered cell.
    If it is, checks if the numbered cell is surrounded by the
    corresponding amount of unknowns to its number. If it is,
    the unknowns are set accordingly.
    """

    def fullCheck(self, cd1, cd2):
        x1c = True
        x2c = True
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if self.minefield[x][y] > -1:
                x1c = self.fullCheckHelper(x, y)

        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if self.minefield[x][y] > -1:
                x2c = self.fullCheckHelper(x, y)

        return self.retHelper(cd1, cd2, x1c, x2c)

    """
    Cannot be primitive function, helps fullcheck helper
    """

    def fullCheckHelper(self, i, j):
        cds = []

        if ((i - 1) >= 0) and ((j - 1) >= 0):
            if self.minefield[i - 1][j - 1] < 0:
                cds.append((i - 1, j - 1))
        # tc
        if (i - 1) >= 0:
            if self.minefield[i - 1][j] < 0:
                cds.append((i - 1, j))
        # tr
        if ((i - 1) >= 0) and ((j + 1) < self.y):
            if self.minefield[i - 1][j + 1] < 0:
                cds.append((i - 1, j + 1))
        # left
        if (j - 1) >= 0:
            if self.minefield[i][j - 1] < 0:
                cds.append((i, j - 1))
        # right
        if (j + 1) < self.y:
            if self.minefield[i][j + 1] < 0:
                cds.append((i, j + 1))
        # bl
        if ((i + 1) < self.x) and ((j - 1) >= 0):
            if self.minefield[i + 1][j - 1] < 0:
                cds.append((i + 1, j - 1))
        # bc
        if (i + 1) < self.x:
            if self.minefield[i + 1][j] < 0:
                cds.append((i + 1, j))
        # br
        if ((i + 1) < self.x) and ((j + 1) < self.y):
            if self.minefield[i + 1][j + 1] < 0:
                cds.append((i + 1, j + 1))
        if len(cds) == self.minefield[i][j]:
            for r in cds:
                if self.minefield[i][j] > 0:
                    self.minefield[r[0]][r[1]] = -1
                else:
                    self.minefield[r[0]][r[1]] = 0
            return False
        else:
            return True

    def filledCheck(self, cd1, cd2):
        x1c = True
        x2c = True
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if self.minefield[x][y] > -1:
                x1c = self.filledCheckHelper(x, y)

        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if self.minefield[x][y] > -1:
                x2c = self.filledCheckHelper(x, y)

        return self.retHelper(cd1, cd2, x1c, x2c)

    def filledCheckHelper(self, i, j):
        known = []
        unknown = []
        if ((i - 1) >= 0) and ((j - 1) >= 0):
            if self.minefield[i - 1][j - 1] < -2:
                unknown.append((i - 1, j - 1))
            elif self.minefield[i - 1][j - 1] == -1:
                known.append((i - 1, j - 1))
        # tc
        if (i - 1) >= 0:
            if self.minefield[i - 1][j] < -2:
                unknown.append((i - 1, j))
            elif self.minefield[i - 1][j] == -1:
                known.append((i - 1, j))
        # tr
        if ((i - 1) >= 0) and ((j + 1) < self.y):
            if self.minefield[i - 1][j + 1] < -2:
                unknown.append((i - 1, j + 1))
            elif self.minefield[i - 1][j + 1] == -1:
                known.append((i - 1, j + 1))
        # left
        if (j - 1) >= 0:
            if self.minefield[i][j - 1] < -2:
                unknown.append((i, j - 1))
            elif self.minefield[i][j - 1] == -1:
                known.append((i, j - 1))
        # right
        if (j + 1) < self.y:
            if self.minefield[i][j + 1] < -2:
                unknown.append((i, j + 1))
            elif self.minefield[i][j + 1] == -1:
                known.append((i, j + 1))
        # bl
        if ((i + 1) < self.x) and ((j - 1) >= 0):
            if self.minefield[i + 1][j - 1] < -2:
                unknown.append((i + 1, j - 1))
            elif self.minefield[i + 1][j - 1] == -1:
                known.append((i + 1, j - 1))
        # bc
        if (i + 1) < self.x:
            if self.minefield[i + 1][j] < -2:
                unknown.append((i + 1, j))
            elif self.minefield[i + 1][j] == -1:
                known.append((i + 1, j))
        # br
        if ((i + 1) < self.x) and ((j + 1) < self.y):
            if self.minefield[i + 1][j + 1] < -2:
                unknown.append((i + 1, j + 1))
            elif self.minefield[i + 1][j + 1] == -1:
                known.append((i + 1, j + 1))
        if len(known) == self.minefield[i][j]:
            for r in unknown:
                if self.minefield[i][j] > 0:
                    self.minefield[r[0]][r[1]] = 0
            return False
        else:
            return True

    """
    
    """

    def emptyTouchCheck(self, cd1, cd2):
        x1c = True
        x2c = True
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if self.minefield[x][y] == 0 or self.minefield[x][y] < -2:
                x1c = self.emptyTouchHelper(x, y)

        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if self.minefield[x][y] == 0 or self.minefield[x][y] < -2:
                x2c = self.emptyTouchHelper(x, y)

        return self.retHelper(cd1, cd2, x1c, x2c)

    def emptyTouchHelper(self, i, j):

        numb = True
        if ((i - 1) >= 0) and ((j - 1) >= 0):
            if self.minefield[i - 1][j - 1] > 0:
                numb = False
        # tc
        if (i - 1) >= 0:
            if self.minefield[i - 1][j] > 0:
                numb = False

        # tr
        if ((i - 1) >= 0) and ((j + 1) < self.y):
            if self.minefield[i - 1][j + 1] > 0:
                numb = False
        # left
        if (j - 1) >= 0:
            if self.minefield[i][j - 1] > 0:
                numb = False

        # right
        if (j + 1) < self.y:
            if self.minefield[i][j + 1] > 0:
                numb = False

        # bl
        if ((i + 1) < self.x) and ((j - 1) >= 0):
            if self.minefield[i + 1][j - 1] > 0:
                numb = False

        # bc
        if (i + 1) < self.x:
            if self.minefield[i + 1][j] > 0:
                numb = False

        # br
        if ((i + 1) < self.x) and ((j + 1) < self.y):
            if self.minefield[i + 1][j + 1] > 0:
                numb = False

        if numb:
            self.minefield[i][j] = 0
        else:
            self.minefield[i][j] = -2

        return numb

    def mineChecker(self, cd1, cd2):
        x1c = True
        x2c = True
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if self.minefield[x][y] == -1:
                x1c = self.mineCheckHelper(x, y)

        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if self.minefield[x][y] == -1:
                x2c = self.mineCheckHelper(x, y)

        return self.retHelper(cd1, cd2, x1c, x2c)

    def mineCheckHelper(self, i, j):

        numb = False
        if ((i - 1) >= 0) and ((j - 1) >= 0):
            if self.minefield[i - 1][j - 1] < 1 and self.minefield[i - 1][j - 1] != -1:
                numb = True
        # tc
        if (i - 1) >= 0:
            if self.minefield[i - 1][j] < 1 and self.minefield[i - 1][j] != -1:
                numb = True

        # tr
        if ((i - 1) >= 0) and ((j + 1) < self.y):
            if self.minefield[i - 1][j + 1] < 1 and self.minefield[i - 1][j + 1] < 0 != -1:
                numb = True
        # left
        if (j - 1) >= 0:
            if self.minefield[i][j - 1] < 1 and self.minefield[i][j - 1] < 0 != -1:
                numb = True

        # right
        if (j + 1) < self.y:
            if self.minefield[i][j + 1] < 1 and self.minefield[i][j + 1] < 0 != -1:
                numb = True

        # bl
        if ((i + 1) < self.x) and ((j - 1) >= 0):
            if self.minefield[i + 1][j - 1] < 1 and self.minefield[i + 1][j - 1] != -1:
                numb = True

        # bc
        if (i + 1) < self.x:
            if self.minefield[i + 1][j] < 1 and self.minefield[i + 1][j] != -1:
                numb = True

        # br
        if ((i + 1) < self.x) and ((j + 1) < self.y):
            if self.minefield[i + 1][j + 1] < 1 and self.minefield[i + 1][j + 1] != -1:
                numb = True

        if numb:
            self.minefield[i][j] = -2

        return numb

    def outerCompare(self, cd1, cd2):
        x1c = False
        x2c = False
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if ((abs(cd1[0]) + abs(cd1[1]) > 1) and (abs(cd1[0]) + abs(cd1[1]) < 5)) and not (
                    abs(cd1[0]) == 1 and abs(cd1[1]) == 1):
                x1c = True
                if self.minefield[x][y] == -2 and self.minefield[self.cord[0]][self.cord[1]] != 0:
                    self.minefield[self.cord[0]][self.cord[1]] = -1

        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if ((abs(cd2[0]) + abs(cd2[1]) > 1) and (abs(cd2[0]) + abs(cd2[1]) < 5)) and not (
                    abs(cd2[0]) == 1 and abs(cd2[1]) == 1):
                x2c = True
                if self.minefield[x][y] == -2 and self.minefield[self.cord[0]][self.cord[1]] != 0:
                    self.minefield[self.cord[0]][self.cord[1]] = -1

        return self.retHelper(cd1, cd2, x1c, x2c)

    def edgeCheck(self, cd1, cd2):
        x1c = False
        x2c = False
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if x == 0 or y == 0 or y ==self.y-1 or x or x == self.x-1:
                x1c = True
        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if x == 0 or y == 0 or y == self.y - 1 or x or x == self.x - 1:
                x2c = True
        return self.retHelper(cd1, cd2, x1c, x2c)