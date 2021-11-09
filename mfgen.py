# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 16:16:09 2021

@author: Ethan Bray
"""

from random import randrange
import numpy as np

"""
The following class creates a minefield with atleast one correct configuration.
Create an object, call makeminefield(x,y,mines).
"""
class mfgenCorrect:
    xlen = 0 #xlength
    ylen = 0 #ylength
    field = None #minefield
    
   
    """
    Sets up appropriate numbers on corresponding cells newly made 'mines'
    8 places to setup for each mine
    """
    def numSet(self,x,y):
       #tl
       if((x-1)>=0) and ((y-1)>=0):
           self.assignVal(x-1,y-1)
       #tc
       if((x-1)>=0): 
           self.assignVal(x-1,y)
       #tr
       if((x-1)>=0) and ((y+1)<self.ylen): 
           self.assignVal(x-1,y+1)
       #left 
       if((y-1)>=0): 
          self.assignVal(x,y-1)
       #right
       if((y+1)<self.ylen): 
           self.assignVal(x,y+1)
       #bl
       if((x+1)<self.xlen) and ((y-1)>=0): 
           self.assignVal(x+1,y-1)
       #bc
       if((x+1)<self.xlen): 
           self.assignVal(x+1,y)
       #br
       if((x+1)<self.xlen) and ((y+1)<self.ylen): 
           self.assignVal(x+1,y+1)
           
    """
    Sets up number cells around mined cells
    """
    def assignVal(self,x,y):
        if isinstance(self.field[x][y],str) and (self.field[x][y] !='*'):
            self.field[x][y] = 1
        elif isinstance(self.field[x][y],int):
            self.field[x][y] += 1
               
            
    """
    Checks if a cell is near a numbered cell.
    """
    def checkForNum(self,x,y):
       mlo = 0
       #tl
       if((x-1)>=0) and ((y-1)>=0):
           if isinstance(self.field[x-1][y-1],int) and self.field[x-1][y-1] >=1:
               mlo+=1
       #tc
       if((x-1)>=0): 
           if isinstance(self.field[x-1][y],int) and self.field[x-1][y] >=1:
               mlo+=1
       #tr
       if((x-1)>=0) and ((y+1)<self.ylen): 
           if isinstance(self.field[x-1][y+1],int) and self.field[x-1][y+1]>=1:
               mlo+=1
       #left 
       if((y-1)>=0): 
          if isinstance(self.field[x][y-1],int) and self.field[x][y-1]>=1:
               mlo+=1
       #right
       if((y+1)<self.ylen): 
           if isinstance(self.field[x][y+1],int) and self.field[x][y+1]>=1:
               mlo+=1
       #bl
       if((x+1)<self.xlen) and ((y-1)>=0): 
           if isinstance(self.field[x+1][y-1],int) and self.field[x+1][y-1]>=1:
               mlo+=1
       #bc
       if((x+1)<self.xlen): 
           if isinstance(self.field[x+1][y],int) and self.field[x+1][y]>=1:
               mlo+=1
       #br
       if((x+1)<self.xlen) and ((y+1)<self.ylen): 
           if isinstance(self.field[x+1][y+1],int) and self.field[x+1][y+1]>=1:
               mlo+=1
           
       return mlo
    
    """
    Gets the cordinates of all spots on the minefield that are either free or 
    hold a mine, this should be used for offsets in the EP and relations to 
    the binary in the GA possibly.
    """
    def getFreeCords(self):
        cords = []
        numbd = []
        x = 0
        
        while x < self.xlen:
            y = 0
            while y < self.ylen:
                if isinstance(self.field[x][y],str):
                    cords.append((x,y))  
                    if self.field[x][y] =='*' :
                        self.field[x][y] = -1
                        
                    elif self.checkForNum(x,y)!=0:
                        self.field[x][y] = -2
                       
                    else:
                        self.field[x][y] = 0
                else:
                    numbd.append((x,y))
                y+=1
            x+=1
        return cords, numbd
        
    
    """
    Assumes correct input, x and y dictates numpy array x and y length.
    Mines dictates the number of mines desired in the list.
    Returns the minefield and list of 'unopened' cells.
    (x and y and mines) >= 1
    """
    def makeField(self,x,y,mines):
        self.xlen = x    
        self.ylen = y
        i = 0
        #make initial list
        field = []
        while i < x:
            s = ['-']*y
            field.append(s)
            i+=1
            
        i = 0
        self.field = field
        while i < mines:
            jx = randrange(x)
            jy = randrange(y)
            if(isinstance(self.field[jx][jy],str) and field[jx][jy]!='*' ) or isinstance(self.field[jx][jy],int):
                self.field[jx][jy] = '*'
                self.numSet(jx,jy)
                
                
                i+=1
        
        #for m in self.field:
           # print(m)   
  
        mr,l = self.getFreeCords()
        return np.array(self.field), mr,l
        
    """
    Uses a different method to make minefield, random set number of mines.
    Check the makeMinefield function for more info.
    """
class mfgenRand:
    xlen = 0 #xlength
    ylen = 0 #ylength
    field = None #minefield
    
    """
    Sets up appropriate numbers on corresponding cells newly made mines.
    8 Places to setup for each mine.
    """
    def setupMine(self,x,y):
       self.field[x][y] = '*'
       #tl
       if((x-1)>=0) and ((y-1)>=0):
           self.assignVal(x-1,y-1)
       #tc
       if((x-1)>=0): 
           self.assignVal(x-1,y)
       #tr
       if((x-1)>=0) and ((y+1)<self.ylen): 
           self.assignVal(x-1,y+1)
       #left 
       if((y-1)>=0): 
          self.assignVal(x,y-1)
       #right
       if((y+1)<self.ylen): 
           self.assignVal(x,y+1)
       #bl
       if((x+1)<self.xlen) and ((y-1)>=0): 
           self.assignVal(x+1,y-1)
       #bc
       if((x+1)<self.xlen): 
           self.assignVal(x+1,y)
       #br
       if((x+1)<self.xlen) and ((y+1)<self.ylen): 
           self.assignVal(x+1,y+1)
    """
    Checks if there is  a mine or a free cell near the cordinates. 
    Mark == True is for freeCells, mark==False is for numbered cells
    This is redundant, could just have it count freecells then do 8-freecell
    count, but I wasnt thinking hard enough when I first made this.
    """
    def checkFor(self,x,y,mark):
       free = 0
       mlo = 0
       #tl
       if((x-1)>=0) and ((y-1)>=0):
           if isinstance(self.field[x-1][y-1],str) or self.field[x-1][y-1] <0:
               if self.field[x-1][y-1] != '*' or self.field[x-1][y-1] != -1: 
                   free+=1
           else:
               mlo+=1
       #tc
       if((x-1)>=0): 
           if isinstance(self.field[x-1][y],str) or self.field[x-1][y] <0:
               if self.field[x-1][y] != '*' or self.field[x-1][y] != -1: 
                   free+=1
           else:
               mlo+=1
       #tr
       if((x-1)>=0) and ((y+1)<self.ylen): 
           if isinstance(self.field[x-1][y+1],str)or self.field[x-1][y+1]  <0:
               if self.field[x-1][y+1] != '*' or self.field[x-1][y+1] != -1: 
                   free+=1
           else:
               mlo+=1
       #left 
       if((y-1)>=0): 
          if isinstance(self.field[x][y-1],str)or self.field[x][y-1]  <0:
               if self.field[x][y-1] != '*' or self.field[x][y-1] != -1: 
                   free+=1
          else:
               mlo+=1
       #right
       if((y+1)<self.ylen): 
           if isinstance(self.field[x][y+1],str) or self.field[x][y+1]  <0:
               if self.field[x][y+1] != '*' or self.field[x][y+1] != -1: 
                   free+=1
           else:
               mlo+=1
       #bl
       if((x+1)<self.xlen) and ((y-1)>=0): 
           if isinstance(self.field[x+1][y-1],str)or self.field[x+1][y-1]  <0:
               if self.field[x+1][y-1] != '*' or self.field[x+1][y-1] != -1: 
                   free+=1
           else:
               mlo+=1
       #bc
       if((x+1)<self.xlen): 
           if isinstance(self.field[x+1][y],str)or self.field[x+1][y]  <0:
               if self.field[x+1][y] != '*' or self.field[x+1][y] != -1: 
                   free+=1
           else:
               mlo+=1
       #br
       if((x+1)<self.xlen) and ((y+1)<self.ylen): 
           if isinstance(self.field[x+1][y+1],str)or self.field[x+1][y+1]  <0:
               if self.field[x+1][y+1] != '*' or self.field[x+1][y+1] != -1:    
                   free+=1
           else:
               
               mlo+=1
           
       if mark:
           return free
       else:
           return mlo
  
    """
    Sets up number cells around mined cells
    """
    def assignVal(self,x,y):
        mlk = self.checkFor(x, y,True)
        if isinstance(self.field[x][y],str):
            if mlk>0 and self.field[x][y]!= '*':
                self.field[x][y] = 1
                
        elif isinstance(self.field[x][y],int):
            
                self.field[x][y] += 1
    
    """
    Returns the cordinates for each unopened cell next to
    numbered cells and each numbered cell. 
    """
    def getCords(self):
        cords = []
        numbd = []
        x = 0
        
        while x < self.xlen:
            y = 0
            while y < self.ylen:
                if isinstance(self.field[x][y],str):
                    cords.append((x,y))
                
                    if self.field[x][y] =='*' :
                        self.field[x][y] = -1
                    elif self.checkFor(x,y,False)!=0:
                        self.field[x][y] = -2
                    else:
                        self.field[x][y] = 0
                    
                else:
                    numbd.append((x,y))
                y+=1
            x+=1
        return cords,numbd
    
    """
    Creates the minefield, calls the other functions. 
    (x and y)>= 4 for optimal use, mark is a bool, if set to True,
    we can get minefields that will have an inconsistent config.
    Each cell has a 1/5 chance of having a mine placed in it.
    returns the minefield, the coordinates for cells that may or may not
    have a mine, and the coordinates for cells that are numbered.
    """
    def makeField(self,x,y,mark):
        self.xlen = x
        self.ylen = y
        self.field = None
        i = 0
        field = []
        while i < x:
            s = ['-']*y
            field.append(s)
            i+=1
        self.field = field
        #setup possibly incorrect minefield
        
        i = 0
        while i < x:
            j = 0
            while j < y:
                num = randrange(5)
                if num==3:
                    self.setupMine(i,j)
                if num==4 and mark:
                    self.assignVal(i,j)
                
                
                j+=1
            
            i+=1
       
        mk,vx = self.getCords() 
        return np.array(self.field), mk,vx  
#uncomment following to test    
"""
mk = mfgenCorrect()
mx = 20
my = 20
mf,l,o = mk.makeField(mx,my,(mx*my)//20)
for i in mf:
    word = ''
    for z in i:
        if z > -1:
            word+= str(z) + '  '
        else:
            word+= str(z) + ' '
    print(word) 
    
print("mfgenCorrect")
mr = mfgenRand()
kl, o, mj = mr.makeField(mx,my,False)
for i in kl:
    
    word = ''
    for z in i:
        
        if z > -1:
            word+= str(z) + '  '
        else:
            word+= str(z) + ' '
    print(word)  

print("mfgenRand")
"""