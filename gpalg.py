# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import generator
import gphelpers
import random
from deap import gp
from gpfunctions import gpfunctions
import copy
import sys

np.set_printoptions(linewidth=800)
from timeit import default_timer as timer


class gpalg:

    def __init__(self, x: int = 16, y: int = 36, popnuml: int = 40, gen: int = 1500):
        self.minefields = None  # a minefield
        self.minefieldcords = []  # collection of cords for minefields
        self.mfdummyfield = None  # a dummy minefield to test against
        self.population = []  # collection of individuals in population, might be best to tuple of (gp,fitness)
        self.popfit = []  # collection of fitnesses, remove if the tuple system is better
        self.funcObj = gpfunctions()  # this will hold the funcObj, we do this so we can change the field and mine cord
        self.orgPset = gp.PrimitiveSet('main', 0)  # this will hold the original set of callable functions, this is mainly for mutations after setPop
        self.maxGen = gen
        self.replacements = 0  # replacement stat, mainly for steady state GA
        self.x = x  # number of rows
        self.y = y  # number of columns
        self.bestFit = 0
        self.bestCand = None
        self.bestField = []
        self.minDepth = 5
        self.maxDepth = 10
        self.bestPosFit = 0
        self.popnum = popnuml
        self.setMinefields()
        start = timer()
        self.setPop()

        self.steadyStateAlg()  # change to generationalAlg() for generational var
        print(self.bestFit)
        print(self.bestField)
        print("Time Taken:", timer() - start)  # 215.2650292 when running 100 MFs and computing inital fitness

    """
    Creates 100 testing minefields, most likely changed if we have a set of
    desired minefields. calls a helper function to deal with denumerated cords.
    """

    def setMinefields(self):

        _minefield, _mines = generator.create_consistent_field(self.x, self.y,.2)
        md, cords, dummyfield = gphelpers.dummymf(_minefield)
        _mines = gphelpers.cordadjust(_mines, self.y)
        _mines = _mines + cords
        self.minefield = md
        self.mfdummyfield = dummyfield
        self.minefieldcords = _mines
        print("Normal field: \n",md)
        print("Dummy field: \n ", dummyfield)
        self.bestPosFit = self.ft(md,md)
        print("Best fit:", self.bestPosFit)

    """
    Apparently deap needs function objects for expressions. Assume pset is 
    original indivudal pset. (this is funked)
    """

    def getExpr(self, pset, type_):

        expr = gp.genGrow(pset, 2, self.maxDepth//2)
        return expr

    """
    Used for pop creation, min and max refer to treedepth.
    Min of 5 seems to run optimally, max depth doesnt seem to be
    reached. genGrow does uneven branches.
    """

    def genIndv(self, min: int = 15, max: int = 40):
        tempPset = copy.copy(self.orgPset)
        expr = gp.genGrow(tempPset, self.minDepth, self.maxDepth)
        # print(expr)

        return expr

    """
    Gets every possible tupled offset and adds
    them as a terminal. Might be better to limit
    them to (k,n) k <= x//2 and n <= y//2, this may 
    be too much.
    """

    def combl(self):

        i = (self.x*-1)+1
        while i < self.x:
            j = (self.y*-1)+1
            while j < self.y:
                tul = (i, j)
                # (type(tul))
                if not (i == 0 and j == 0):
                    self.orgPset.addTerminal(tul)
                j += 1
            i += 1

    """
    Sets the initial population and sets up the primitve
    functions. As of now, individuals are loosely typed (packed?)
    trees, meaning there is no check for what each function is returning 
    to the next. As of now they all just take in tuples
    and return int tuples. 
    """

    def setPop(self):
        #self.orgPset.addPrimitive(self.funcObj.eightCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.emptyCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.neighborCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.outerNeighborCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.numCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.unknownCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.fullCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.filledCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.emptyTouchCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.mineChecker, 2)
        self.orgPset.addPrimitive(self.funcObj.outerCompare, 2)
        self.orgPset.addPrimitive(self.funcObj.edgeCheck, 2)
        self.combl()  # add terminals

        i = 0
        while i < self.popnum:
            #print(i)
            expr = self.genIndv(self.minDepth, self.maxDepth)
            indv = gp.PrimitiveTree(expr)
            fit = self.fitness(indv)
            if fit not in self.popfit:
                i = i + 1
                self.population.append(indv)
                self.popfit.append(fit)


        self.popfit = np.array(self.popfit)

    """
    This is the main thing that needs work. The intention know is that
    trees are compiled to get a result, but the result returned from
    gp.compile doesn't matter as of now. As of now, the result is retrieved
    from the self.funcObj.getResult function, where the intenion is that
    True means a mine can be there as determined by the tree, but a check
    occurs if thats actually the case. +1 for each mine. 
    If an entire minefield is determined correctly, +10 fitness to that indivudal.
    """

    def fitness(self, indv):
        fit = 0
        tree = copy.copy(indv)

        # print(i)
        self.funcObj.setMinefield(copy.copy(self.mfdummyfield))

        mf = copy.copy(self.minefield)
        xks = 0
        while xks < 1:
            for cd in self.minefieldcords:
                self.funcObj.setCord(cd)
                # print(tree)
                gp.compile(tree, self.orgPset)
            xks += 1


        mp = self.funcObj.getResult()

        fit = self.ft(mf,mp)
        if fit > self.bestFit:
            self.bestFit = fit
            self.bestCand = copy.copy(indv)
            self.bestField = mp
            print(str(indv))
            print("New Bestfit: ",self.bestFit)
            print(mp)

        return fit

    def ft(self, mf, mp):
        fit = 0
        for arc in self.minefieldcords:
            if mf[arc[0]][arc[1]] < 1:
                if mf[arc[0]][arc[1]] == -2 and mp[arc[0]][arc[1]] == -2:
                    fit +=2
                if mf[arc[0]][arc[1]] == -2 and mp[arc[0]][arc[1]] == 0:
                    fit += 1
                if mf[arc[0]][arc[1]] == 0 and mp[arc[0]][arc[1]] == 0:
                    fit += 2
                if mf[arc[0]][arc[1]] == -0 and mp[arc[0]][arc[1]] == -2:
                    fit += 1
                if mf[arc[0]][arc[1]] == -1 and mp[arc[0]][arc[1]] == -1:
                    fit += 5
        return fit
    # crossovers and mutations seem to return tuples with 1 index

    def mutate(self, indv):
        pset = copy.copy(self.orgPset)
        tree = indv
        r = random.randrange(0, 6)
        # mutshrink depends on arguments, we dont have arguments as of now
        if r  <4:
            tree = gp.mutUniform(tree, self.getExpr, pset)
            # print("1")
       # if r == 1 or r == 3:
          #  tree = gp.mutNodeReplacement(tree, pset)
            # print("2")
       # if r == 2:
        #    tree = gp.mutInsert(tree, pset)
            # print("3")

        if r < 4:
            tree = tree[0]

        indv = tree
        return indv

    """
    Tournament Selection between two individuals, selects highest fitness.
    Returns indexes of parents in population. Special checks if pop is 2.
    Check pop length before calling.
    """

    def selectParents(self):
        p1 = 0
        p2 = 1
        mrs = len(self.population)
        if mrs > 2:
            x1 = random.randrange(0, mrs)
            x2 = random.randrange(0, mrs)
            while x2 == x1:
                x2 = random.randrange(0, mrs)
            if (self.popfit[x1] == self.popfit[x2]):
                p1 = random.choice([x1, x2])
            elif (self.popfit[x1] > self.popfit[x2]):
                p1 = x1
            else:
                p1 = x2

            x1 = random.randrange(0, mrs)
            x2 = random.randrange(0, mrs)

            while x1 == p1:
                x1 = random.randrange(0, mrs)
            while x2 == x1 or x2 == p1:
                x2 = random.randrange(0, mrs)

            if self.popfit[x1] == self.popfit[x2]:
                p2 = random.choice([x1, x2])
            elif self.popfit[x1] > self.popfit[x2]:
                p2 = x1
            else:
                p2 = x2

        return p1, p2

    """
    Takes trees as parameters, returns new trees.
    Origninally used cxonepoint and the leaf variant,
    took out due to issues. Can probably readd without
    issue. Probably best to wait until we have proper fitness
    functions.
    """

    def crossover(self, p1, p2):
        trees = None
        # print(p1)
        # print(p2)
        trees = gp.cxOnePoint(p1, p2)
        return trees

    """
    Replaces worst in population if new is better then the worst.
    If we want to reduce elitism, we can replace worst regardless.
    
    """

    def replacementWorst(self, indv1, fit1, indv2, fit2):

        crpfit = np.partition(self.popfit, (1, 2))
        indx1 = np.where(self.popfit == crpfit[0])
        indx2 = np.where(self.popfit == crpfit[1])

        if type(indx1)!=int:
            indx1 = indx1[0][0]
        if type(indx2)!=int:
            indx2 = indx2[0][0]

        ch1, ch2, indr1, indr2 = self.popcheck(indv1,fit1, indv2, fit2, True)
        mrx = crpfit[0]
        if ch1 and fit1>crpfit[0]:
            if indr1 != None:

                indx1 = indr1
            self.replacements += 1
            self.population[indx1] = indv1
            self.popfit[indx1] = fit1
            mrx = crpfit[1]
        else:
            indx2 = indx1
        if ch2 and fit2 > mrx:
            if indr2 != None:

                indx2 = indr2
            self.replacements += 1
            self.population[indx2] = indv2
            self.popfit[indx2] = fit2

    """
    Replaces individual in population that has fitness closest to 
    the individual we wish to try and insert. If the closest
    indv for indv2 is indv1, replace second closest.
    """

    def replacementClosest(self, indv1, fit1, indv2, fit2):
        dr1 = np.absolute(self.popfit - fit1)
        dr2 = np.absolute(self.popfit - fit2)
        fg = False
        indx1 = dr1.argmin()
        # print(indx1)
        indx2 = dr2.argmin()
        if indx1 == indx2:
            fg = True
            dr2[indx2] = dr2[dr2.argmax()] * 10  #
            indx2 = dr2.argmin()

        ch1, ch2,indr1,indr2 = self.popcheck(indv1,fit1, indv2, fit2, True)

        if ch1 and self.popfit[indx1]<=fit1:
            self.replacements += 1
            self.population[indx1] = indv1
            self.popfit[indx1] = fit1
        elif fg == True:
            indx2 = indx1
        if ch2 and self.popfit[indx2]<=fit2:
            self.replacements += 1
            self.population[indx2] = indv2
            self.popfit[indx2] = fit2

    """
    Had an issue early where parents kept reappearing in the pop.
    This dealt with it, still does. I think its best
    we keep it in order to reduce any possible clones though
    unlikely.
    """

    def popcheck(self, indv1,fit1, indv2,fit2, v2):
        ch1 = True
        ch2 = True
        indx1 = None
        indx2 = None
        i = 0
        for (x, y) in zip(self.population,self.popfit):
            if str(x) == str(indv1):
                ch1 = False
            if str(x) == str(indv2):
                ch2 = False
            if(y==fit1 and v2):
                indx1 = i
            if(y == fit2 and v2):
                indx2 = i
            i+=1
        return ch1, ch2, indx1, indx2

    """
    Tested as much as I can, follows a simple steady state
    algorithim. Only two individuals added to a population.
    Convergence will probably take forever. 
    """

    def steadyStateAlg(self):
        i = 0
        while i < self.maxGen and self.bestFit != self.bestPosFit:
            p1, p2 = self.selectParents()
            print("version: ", i)
            print(self.popfit)
            p1p = copy.copy(self.population[p1])
            p2p = copy.copy(self.population[p2])
            # print(p1, " ",p2p)
            # print(p2, " ",p2p)
            c1, c2 = self.crossover(p1p, p2p)

            c1 = self.mutate(c1)
            c2 = self.mutate(c2)
            c1f = self.fitness(c1)
            c2f = self.fitness(c2)
            self.replacementClosest(c1, c1f, c2, c2f)  # switch between this and replacementWorst
            print("Replaced parents :", self.replacements)
            i += 1

    """
    Generational algorithim. As of now, parents create 20 children and pick the best 2
    from those 20 to replace their slots. Assume even number of individuals in pop. Can add
    a self-mutation if we want to have odd numbered pops. Assumes none of the same 
    individuals can appear in population.
    """

    def generationalAlg(self, childnum: int = 5):
        i = 0
        while i < self.maxGen and self.bestFit != self.bestPosFit:
            print("version: ", i)
            parentpairs = []
            pfitpairs = []
            # pair the parents
            while len(self.population) > 1:
                p1, p2 = self.selectParents()
                pfitpairs.append((self.popfit[p1],self.popfit[p2]))
                p1 = self.population[p1]
                p2 = self.population[p2]
                parentpairs.append((p1, p2))

                self.population.remove(p1)
                self.population.remove(p2)
                # print(len(self.population))
            jk = 0
            for x,y in zip(parentpairs,pfitpairs):
                print("Parent Combination", jk)
                children = []
                cfit = []
                r = 0
                # create the children
                while r < childnum:  # change this to change amount of children produced by parents
                    c1, c2 = self.crossover(x[0], x[1])
                    c1 = self.mutate(c1)
                    c2 = self.mutate(c2)
                    c1f = self.fitness(c1)
                    c2f = self.fitness(c2)

                    children.append(c1)
                    children.append(c2)
                    cfit.append(c1f)
                    cfit.append(c2f)
                    r += 1
                children.append(x[0])
                children.append(x[1])
                cfit.append(y[0])
                cfit.append(y[1])
                r = 0
                # select best from children
                while r < 2:
                    # print('fuck')
                    mx = max(cfit)
                    index = cfit.index(mx)
                    ch1, ch2, indr1, indr2 = self.popcheck(copy.copy(children[index]), cfit[index], 'No', 0, False)
                    if ch1:
                        self.popfit[len(self.population)] = mx
                        self.population.append(copy.copy(children[index]))
                        r += 1
                    cfit.pop(index)
                    children.pop(index)
                jk+=1
            i += 1


mr = gpalg()
