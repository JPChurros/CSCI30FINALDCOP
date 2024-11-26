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
            indexOfColumnBelow = seam[row+1]
            smallestValue = 0

            #mid right and left are just essentially OnTop, TopRight, TopLeft, respectively.
            #indexOfColumnBelow is just referring to index of seam below
            if indexOfColumnBelow == 0:
                mid = energyArray[row][indexOfColumnBelow]
                right = energyArray[row][indexOfColumnBelow + 1]
                smallestValue = min(mid, right)
                if smallestValue == mid:
                    seam[row] = indexOfColumnBelow
                else:
                    seam[row] = indexOfColumnBelow + 1

            elif indexOfColumnBelow == self.width()-1:
                mid = energyArray[row][indexOfColumnBelow]
                left = energyArray[row][indexOfColumnBelow - 1]
                smallestValue = min(mid, left)
                if smallestValue == mid:
                    seam[row] = indexOfColumnBelow
                else:
                    seam[row] = indexOfColumnBelow - 1
            
            else:
                mid = energyArray[row][indexOfColumnBelow]
                right = energyArray[row][indexOfColumnBelow+1]
                left = energyArray[row][indexOfColumnBelow-1]
                smallestValue = min(mid, right, left)
                if smallestValue == mid:
                    seam[row] = indexOfColumnBelow
                elif smallestValue == right:
                    seam[row] = indexOfColumnBelow + 1
                else:
                    seam[row] = indexOfColumnBelow - 1


        

        raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        raise NotImplementedError

class SeamError(Exception):
    pass
