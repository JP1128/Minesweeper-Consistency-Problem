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
        self.surrUnknown = False
        self.surrNumbd = True
        self.nearEmpty = False
        self.nearEight = False  # true if certain checks pass that would determine abosulute truth to cell being a mine
        self.mineFalse = False  # true if certain checks pass that would determine abosulute truth to cell not being a mine
        self.minefield = None
        self.cord = (0, 0)


    """
    This function is meant to reset the checks between each call.
    If we use weights and record counts, reset counts here.
    """
    def setChecks(self):
        self.surrUnknown = False
        self.surrNumbd = True
        self.nearEmpty = False
        self.nearEight = False  # true if certain checks pass that would determine abosulute truth to cell being a mine
        self.mineFalse = False  # true if certain checks pass that would determine abosulute truth to cell not being a mine

    """
    Utility function, helps thegp  functions return a value. 
    Made a function to reduce bloat.
    """

    def retHelper(self, cd1, cd2, x1c, x2c):
        rval = None
        if x1c == x2c:
            r = random.randrange(0, 2)
            if r == 0:
                rval = cd1
            else:
                rval = cd1
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
        #print(cd)
        #print(self.cord)
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

        if self.nearEight:
            return True

        #if self.nearEmpty:
            #return False

        mk = random.choice([True,False])

        return mk

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
                    self.nearEight = True
        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if self.minefield[x][y] == 8:
                x1c = True
                if abs(cd2[0]) <= 1 and abs(cd2[1]) <= 1:
                    self.nearEight = True
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
            if self.minefield[x][y] == 0 and abs(cd1[0]) <= 1 and abs(cd1[1]) <= 1:
                self.nearEmpty = True
                x1c = True
        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if self.minefield[x][y] == 0 and abs(cd2[0]) <= 1 and abs(cd2[1]) <= 1:
                self.nearEmpty = True
                x2c = True
        return self.retHelper(cd1, cd2, x1c, x2c)

    """
    Checks if cord is a neighbor, returns cord if is.
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
    def outerNeighborCheck(self,cd1,cd2):
        x1c = False
        x2c = False
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if ((abs(cd1[0]) + abs(cd1[1]) >1) and (abs(cd1[0]) + abs(cd1[1]) < 5)) and not(abs(cd1[0]) == 1 and abs(cd1[1]) == 1):
                x1c = True
        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if ((abs(cd2[0]) + abs(cd2[1]) >1) and (abs(cd2[0]) + abs(cd2[1]) < 5)) and not(abs(cd2[0]) == 1 and abs(cd2[1]) == 1):
                x1c = True
        return self.retHelper(cd1, cd2, x1c, x2c)

    def numCheck(self, cd1, cd2):
        x1c = False
        x2c = False
        if self.boundCheck(cd1):
            x = self.cord[0] + cd1[0]
            y = self.cord[1] + cd1[1]
            if self.minefield[x][y] > 0:
                x1c = True
        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if self.minefield[x][y] > 0:
                x2c = True
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
            if self.minefield[x][y] <= 0:
                x1c = True
                if abs(cd1[0]) < 2 and abs(cd1[1]) < 2:
                    self.surrUnknown = True
        if self.boundCheck(cd2):
            x = self.cord[0] + cd2[0]
            y = self.cord[1] + cd2[1]
            if self.minefield[x][y] <= 0:
                x2c = True
                if abs(cd2[0]) < 2 and abs(cd2[1]) < 2:
                    self.surrUnknown = True
        return self.retHelper(cd1, cd2, x1c, x2c)

