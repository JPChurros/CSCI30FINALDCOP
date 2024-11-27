#!/usr/bin/env python3
import numpy as np
from picture import Picture

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        left_pixel = [self.width()-1,j] if i-1<0 else self[i-1,j]
        right_pixel = [0,j] if i+1>=self.width() else self[i+1,j]

        top_pixel = [i,self.height()-1] if j-1<0 else self[i,j-1]
        bottom_pixel = [i,0] if j+1>=self.height() else self[i,j+1]

        x_Red = abs(left_pixel[0]-right_pixel[0])
        x_Green = abs(left_pixel[1]-right_pixel[1])
        x_Blue = abs(left_pixel[2]-right_pixel[2])
        x_Delta = x_Red**2 + x_Green**2 + x_Blue**2

        y_Red = abs(top_pixel[0]-bottom_pixel[0])
        y_Green = abs(top_pixel[1]-bottom_pixel[1])
        y_Blue = abs(top_pixel[2]-bottom_pixel[2])
        y_Delta = y_Red**2 + y_Green**2 + y_Blue**2

        return (x_Delta + y_Delta)**0.5

        raise NotImplementedError

    def find_vertical_seam(self) -> list[int]: #Note, idk sometimes when to subtract one to set the size
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        energyArray = [[0] * self.width() for i in range(self.height)] #creates a 2dimensional energyArrayay of size width and height!
        #idk if this may -1 for the width and shit ah.
        for row in range(self.height()):
            for column in range(self.width()):
                energyArray[row][column] = self.energy(row, column) #populates the 2dimensional energyArrayay with the corresponding energy for each ano.
        #energyArrayay two
        
        minCost = [[0] * self.width() for i in range(self.height)]
        #idk if this has -1 for the width or height bro
        for row in range(self.height()):
            for column in range(self.width()):
                #edge case for pinakataas
                if row == 0:
                    minCost[0][column] = energyArray[0][column]
                #edge case for left corner
                if column == 0:
                    OnTop = energyArray[row-1][column]
                    TopRight = energyArray[row-1][column+1]
                    #determine the minimum and assign it
                    AssignedValue = min(OnTop, TopRight)
                #edge case for right corner idk if may minus one dito
                elif column == self.width()-1:
                    OnTop = energyArray[row-1][column]
                    TopLeft = energyArray[row-1][column-1]
                    #determine the minimum and assign it
                    AssignedValue = min(OnTop, TopLeft)

                #middle! , check first if assigned value has laman cuz if meron then its an edge case
                if AssignedValue != 0:
                    OnTop = energyArray[row-1][column]
                    TopRight = energyArray[row-1][column+1]
                    TopLeft = energyArray[row-1][column-1]
                    AssignedValue = min(OnTop, TopRight, TopLeft)
                
                minCost[row][column] = AssignedValue + energyArray[row][column]
                AssignedValue = 0

        # this part gets the index of the smallest value sa last row sa minCost 2d array
        lastRow = [0]*self.width()
        rowCounter = 0
        while rowCounter < self.width():
            lastRow[rowCounter] = minCost[self.height()-1][rowCounter]
            rowCounter += 1
        startingPoint = lastRow.index(min(lastRow))

        # this "instantiates" the seam list, and then i decided to add na agad the startingPoint variable sa last element ng list
        seam = [0]*self.height()
        seam[self.height()-1] = startingPoint
        # similar logic to what you guys worked with, it ends at row 0 
        for row in range(self.height()-2, -1, -1):
            indexOfSeamBelow = seam[row+1]
            smallestValue = 0

            #mid right and left are just essentially OnTop, TopRight, TopLeft, respectively.
            #indexOfSeamBelow is just referring to index of seam below
            if indexOfSeamBelow == 0:
                mid = minCost[row][indexOfSeamBelow]
                right = minCost[row][indexOfSeamBelow + 1]
                smallestValue = min(mid, right)
                if smallestValue == mid:
                    seam[row] = indexOfSeamBelow
                else:
                    seam[row] = indexOfSeamBelow + 1

            elif indexOfSeamBelow == self.width()-1:
                mid = minCost[row][indexOfSeamBelow]
                left = minCost[row][indexOfSeamBelow - 1]
                smallestValue = min(mid, left)
                if smallestValue == mid:
                    seam[row] = indexOfSeamBelow
                else:
                    seam[row] = indexOfSeamBelow - 1
            
            else:
                mid = minCost[row][indexOfSeamBelow]
                right = minCost[row][indexOfSeamBelow+1]
                left = minCost[row][indexOfSeamBelow-1]
                smallestValue = min(mid, right, left)
                if smallestValue == mid:
                    seam[row] = indexOfSeamBelow
                elif smallestValue == right:
                    seam[row] = indexOfSeamBelow + 1
                else:
                    seam[row] = indexOfSeamBelow - 1

        return seam

        raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        energyArray = [[0] * self.width() for i in range(self.height)] #creates a 2dimensional energyArrayay of size width and height!
        #idk if this may -1 for the width and shit ah.
        for row in range(self.height()):
            for column in range(self.width()):
                energyArray[row][column] = self.energy(row, column) #populates the 2dimensional energyArrayay with the corresponding energy for each ano.
        #create a 2d array that consists of the energy of each element

        #create 2d array numero two that consists of mincost of top 3 elements
        #initialize mincost to have appropriate size
        minCost = [[0] * self.width() for i in range(self.height)]

        #rearranged column to row so it populates by column instead of by row copared ot horiz seam
        for column in range(self.width()):
            for row in range(self.height()):
                #edge case for left wall
                if column == 0:
                    minCost[row][0] = energyArray[row][0]
                #edge case for top wall
                if row == 0:
                    Left = energyArray[row][column-1]
                    BottomLeft = energyArray[row+1][column-1]
                    #determine the minimum and assign it
                    AssignedValue = min(Left, BottomLeft)
                #edge case for bottomwall
                elif row == self.height()-1:
                    Left = energyArray[row][column-1]
                    TopLeft = energyArray[row-1][column-1]
                    #determine the minimum and assign it
                    AssignedValue = min(Left, TopLeft)

                #middle! , check first if assigned value has laman cuz if meron then its an edge case
                if AssignedValue != 0:
                    Left = energyArray[row][column-1]
                    TopLeft = energyArray[row-1][column-1]
                    BottomLeft = energyArray[row+1][column-1]
                    AssignedValue = min(Left, BottomLeft, TopLeft)
                
                minCost[row][column] = AssignedValue + energyArray[row][column]

                AssignedValue = 0

         # this part gets the index of the smallest value sa last column sa minCost 2d array
        lastColumn = [0]*self.height()
        columnCounter = 0
        while columnCounter < self.height():
            lastColumn[columnCounter] = minCost[columnCounter][self.width()-1] #for each at the pinakaright we get add them to lastcolumn list
            columnCounter += 1
        startingPoint = lastColumn.index(min(lastColumn))

         
        # this "instantiates" the seam list, and then i decided to add na agad the startingPoint variable sa last element ng list
        seam = [0]*self.width()
        seam[self.width()-1] = startingPoint
        # similar logic to what you guys worked with, it ends at row 0 
        #IDG HOW THIS FOR LOOP WORKS THERES PROBABLY AN ERROR HERE >>>>>>>>>>>>>>>>>>>
        for column in range(self.width()-2, -1, -1):
        #need to fix laman ng for loop na to
            indexOfSeamToTheRight = seam[column+1]
            smallestValue = 0

            #mid right and left are just essentially OnTop, TopRight, TopLeft, respectively.
            #indexOfSeamToTheRight is just referring to index of seam below
            if indexOfSeamToTheRight == 0:
                mid = minCost[indexOfSeamToTheRight][column]
                down = minCost[indexOfSeamToTheRight + 1][column]
                smallestValue = min(mid, down)
                if smallestValue == mid:
                    seam[column] = indexOfSeamToTheRight
                else:
                    seam[column] = indexOfSeamToTheRight + 1

            elif indexOfSeamToTheRight == self.height()-1:
                mid = minCost[indexOfSeamToTheRight][column]
                up = minCost[indexOfSeamToTheRight - 1][column]
                smallestValue = min(mid, up)
                if smallestValue == mid:
                    seam[column] = indexOfSeamToTheRight
                else:
                    seam[column] = indexOfSeamToTheRight - 1
            
            else:
                mid = minCost[indexOfSeamToTheRight][column]
                up = minCost[indexOfSeamToTheRight - 1][column]
                down = minCost[indexOfSeamToTheRight + 1][column]
                smallestValue = min(mid, up, down)
                if smallestValue == mid:
                    seam[column] = indexOfSeamToTheRight
                elif smallestValue == up:
                    seam[column] = indexOfSeamToTheRight - 1
                else:
                    seam[column] = indexOfSeamToTheRight + 1

        return seam

        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        for x, y in seam:
            for row in range(x, self.width()-1):
                self.update((row, y), self.get((row+1, y)))
            self.pop((self.width()-1, y))

        raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        for x, y in seam:
            for col in range(y, self.height()-1):
                self.update((x, col), self.get((x, col+1)))
            self.pop((x, self.height()-1))

        raise NotImplementedError

class SeamError(Exception):
    pass
