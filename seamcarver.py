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
        arr = [[0] * self.width() for i in range(self.height)] #creates a 2dimensional array of size width and height!
        #idk if this may -1 for the width and shit ah.
        for row in range(self.height()):
            for column in range(self.width()):
                arr[row][column] = self.energy(row, column) #populates the 2dimensional array with the corresponding energy for each ano.
        #array two
        
        mincostarray = [[0] * self.width() for i in range(self.height)]
        #idk if this has -1 for the width or height bro
        for row in range(self.height()):
            for column in range(self.width()):
                #edge case for pinakataas
                if row == 0:
                    mincostarray[0][column] = arr[0][column]
                #edge case for left corner
                if column == 0:
                    OnTop = arr[row-1][column]
                    TopRight = arr[row-1][column+1]
                    #determine the minimum and assign it
                    AssignedValue = min(OnTop, TopRight)
                #edge case for right corner idk if may minus one dito
                if column == self.width():
                    OnTop = arr[row-1][column]
                    TopLeft = arr[row-1][column-1]
                    #determine the minimum and assign it
                    AssignedValue = min(OnTop, TopLeft)

                #middle! , check first if assigned value has laman cuz if meron then its an edge case
                if AssignedValue != 0:
                    OnTop = arr[row-1][column]
                    TopRight = arr[row-1][column+1]
                    TopLeft = arr[row-1][column-1]
                    AssignedValue = min(OnTop, TopRight, TopLeft)
                
                mincostarray[row][column] = AssignedValue

                AssignedValue = 0
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
