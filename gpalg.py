# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import generator
import gphelpers
import random
from deap import gp
from gpfunctions import gpfunctions
import copy

from timeit import default_timer as timer


class gpalg:

    def __init__(self, x: int = 30, y: int = 16, popnuml: int = 20, gen: int = 1000):
        self.minefields = []  # collection of minefields
        self.minefieldcords = []  # collection of cords for minefields
        self.mfdummyfields = []  # collection of dummyfields for GP compilation
        self.population = []  # collection of individuals in population, might be best to tuple of (gp,fitness)
        self.popfit = []  # collection of fitnesses, remove if the tuple system is better
        self.funcObj = gpfunctions()  # this will hold the funcObj, we do this so we can change the field and mine cord
        self.orgPset = gp.PrimitiveSet('main',0)  # this will hold the original set of callable functions, this is mainly for mutations after setPop
        self.maxGen = gen
        self.replacements = 0 #replacement stat, mainly for steady state GA
        self.x = x  # number of rows
        self.y = y  # number of columns
        self.popnum = popnuml
        self.setMinefields()
        start = timer()
        self.setPop()

        self.generationalAlg() #change to steadyStateAlg() for steady state var
        print("Time Taken:", timer() - start)  # 215.2650292

    """
    Creates 100 testing minefields, most likely changed if we have a set of
    desired minefields. calls a helper function to deal with denumerated cords.
    """

    def setMinefields(self):
        i = 0

        while i < 3:
            _minefield, _mines = generator.create_consistent_field(self.x, self.y)
            md, cords = gphelpers.dummymf(_minefield)
            _mines = gphelpers.cordadjust(_mines, self.y)
            _mines = _mines + cords
            self.minefields.append(_minefield)
            self.mfdummyfields.append(md)
            self.minefieldcords = _mines

            i += 1

    """
    Apparently deap needs function objects for expressions. Assume pset is 
    original indivudal pset. (this is funked)
    """

    def getExpr(self, pset, type_):

        expr = gp.genGrow(pset, min_=1, max_=5)
        return expr

    """
    Used for pop creation, min and max refer to treedepth.
    Min of 5 seems to run optimally, max depth doesnt seem to be
    reached. genGrow does uneven branches.
    """
    def genIndv(self, min: int = 5, max: int = 40):
        tempPset = copy.copy(self.orgPset)
        expr = gp.genGrow(tempPset, min_=min, max_=max)
        # print(expr)

        return expr

    """
    Gets every possible tupled offset and adds
    them as a terminal. Might be better to limit
    them to (k,n) k <= x//2 and n <= y//2, this may 
    be too much.
    """
    def combl(self):

        i = self.x * -1
        while i < self.x:
            j = self.y * -1
            while j < self.y:
                tul = (i, j)
                # (type(tul))
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
        self.orgPset.addPrimitive(self.funcObj.eightCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.emptyCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.neighborCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.outerNeighborCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.numCheck, 2)
        self.orgPset.addPrimitive(self.funcObj.unknownCheck, 2)
        self.combl()

        i = 0
        while i < self.popnum:
            expr = self.genIndv(5, 40)
            indv = gp.PrimitiveTree(expr)
            self.population.append(indv)
            self.popfit.append(self.fitness(indv))

            i = i + 1
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
        tree = indv
        i = 0
        for mf in self.mfdummyfields:
            # print(i)
            self.funcObj.setMinefield(mf)
            total = 0
            cur = 0
            for cd in self.minefieldcords:
                total += 1
                self.funcObj.setCord(cd)
                # print(tree)
                gp.compile(tree, self.orgPset)
                if (self.funcObj.getResult()) and mf[cd[0]][cd[1]]==0:
                    cur += 1
            i += 1
            if cur == total:
                fit += 10
            fit = fit + cur
        #print(fit)
        return fit

    # crossovers and mutations seem to return tuples with 1 index

    def mutate(self, indv):
        pset = copy.copy(self.orgPset)
        tree = indv
        r = random.randrange(0, 8)
        # mutshrink depends on arguments, we dont have arguments as of now
        if r == 0:
            tree = gp.mutUniform(tree, self.getExpr, pset)
            # print("1")
        if r == 1 or r == 3:
            tree = gp.mutNodeReplacement(tree, pset)
            # print("2")
        if r == 2:
            tree = gp.mutInsert(tree, pset)
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
        print(p1)
        print(p2)
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
        if type(indx1 == tuple):
            indx1 = [0][0]
        if type(indx2 == tuple):
            indx2 = [0][0]

        ch1, ch2 = self.popcheck(indv1, indv2)

        if ch1:

            self.replacements += 1
            self.population[indx1] = indv1
            self.popfit[indx1] = fit1
        else:
            indx2 = indx1
        if ch2:
            self.replacements +=1
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
        #print(indx1)
        indx2 = dr2.argmin()
        if indx1 == indx2:
            fg = True
            dr2[indx2] = dr2[dr2.argmax()]*10 #
            indx2 = dr2.argmin()

        ch1, ch2 = self.popcheck(indv1, indv2)

        if ch1:

            self.replacements += 1
            self.population[indx1] = indv1
            self.popfit[indx1] = fit1
        elif fg == True:
            indx2 = indx1
        if ch2:
            self.replacements += 1
            self.population[indx2] = indv2
            self.popfit[indx2] = fit2

    """
    Had an issue early where parents kept reappearing in the pop.
    This dealt with it, still does. I think its best
    we keep it in order to reduce any possible clones though
    unlikely.
    """
    def popcheck(self, indv1, indv2):
        ch1 = True
        ch2 = True
        for x in self.population:
            if str(x) == str(indv1):
                ch1 = False
            if str(x) == str(indv2):
                ch2 = False
        return ch1, ch2

    """
    Tested as much as I can, follows a simple steady state
    algorithim. Only two individuals added to a population.
    Convergence will probably take forever. 
    """
    def steadyStateAlg(self):
        i = 0
        while i < self.maxGen:

            p1, p2 = self.selectParents()
            print("version: ",i)
            p1p = copy.copy(self.population[p1])
            p2p = copy.copy(self.population[p2])
            print(p1, " ",p2p)
            print(p2, " ",p2p)
            c1, c2 = self.crossover(p1p, p2p)

            c1 = self.mutate(c1)
            c2 = self.mutate(c2)
            c1f = self.fitness(c1)
            c2f = self.fitness(c2)
            self.replacementClosest(c1, c1f, c2, c2f) #switch between this and replacementWorst
            print("Replaced parents :", self.replacements)
            i += 1

    """
    Generational algorithim. As of now, parents create 20 children and pick the best 2
    from those 20 to replace their slots. Assume even number of individuals in pop. Can add
    a self-mutation if we want to have odd numbered pops. Assumes none of the same 
    individuals can appear in population.
    """
    def generationalAlg(self, childnum: int = 20):
        i = 0
        while i < self.maxGen:
            parentpairs = []
            #pair the parents
            while len(self.population) > 1:
                p1, p2 = self.selectParents()
                p1 = self.population[p1]
                p2 = self.population[p2]
                parentpairs.append((p1, p2))
                self.population.remove(p1)
                self.population.remove(p2)
                print(len(self.population))
            for x in parentpairs:

                children = []
                cfit = []
                r = 0
                #create the children
                while r < childnum: #change this to change amount of children produced by parents
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
                r = 0
                #select best from children
                while r < 2:
                    print('fuck')
                    mx = max(cfit)
                    index = cfit.index(mx)
                    ch1, ch2 = self.popcheck(copy.copy(children[index]), 'No')
                    if ch1:
                        self.popfit[len(self.population)] = mx
                        self.population.append(copy.copy(children[index]))
                        r += 1
                    cfit.pop(index)
                    children.pop(index)

            i += 1


mr = gpalg()
