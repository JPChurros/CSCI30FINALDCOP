#!/usr/bin/env python3
from picture import Picture
from PIL import Image

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        
        if i < 0 or i >= self.width() or j < 0 or j >= self.height():       #error handling case 1: pixel is not part of image anymore
            raise IndexError("Pixel is out of bounds.")

        if i-1 < 0:                                                         #handling of the left and right pixels and their wrapping
            left_pixel = self[self.width()-1,j]
            right_pixel = self[i+1,j]
        elif i+1 >= self.width():
            left_pixel = self[i-1,j]
            right_pixel = self[0,j]
        else:
            left_pixel = self[i-1,j]
            right_pixel = self[i+1,j]

        if j-1 < 0:                                                         #handling of top and bottom pixels and their wrapping            
            top_pixel = self[i,self.height()-1]
            bottom_pixel = self[i,j+1]
        elif j+1 >= self.height():
            top_pixel = self[i,j-1]
            bottom_pixel = self[i,0]
        else:
            top_pixel = self[i,j-1]
            bottom_pixel = self[i,j+1]

        x_Red = abs(left_pixel[0]-right_pixel[0])
        x_Green = abs(left_pixel[1]-right_pixel[1])
        x_Blue = abs(left_pixel[2]-right_pixel[2])
        x_Delta = x_Red**2 + x_Green**2 + x_Blue**2

        y_Red = abs(top_pixel[0]-bottom_pixel[0])
        y_Green = abs(top_pixel[1]-bottom_pixel[1])
        y_Blue = abs(top_pixel[2]-bottom_pixel[2])
        y_Delta = y_Red**2 + y_Green**2 + y_Blue**2

        return (x_Delta + y_Delta)**0.5

    def find_vertical_seam(self) -> list[int]: 
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        energyArray = [[0] * self.width() for i in range(self.height())]    #creates a 2dimensional array of size width and height!

        for row in range(self.height()):                                    #populates the 2dimensional array with the corresponding energy for each ano
            for column in range(self.width()):
                energyArray[row][column] = self.energy(column, row) 
        

        minCost = [[0] * self.width() for i in range(self.height())]        #creates 2d array to contain the minimum cost energies
        for row in range(self.height()):
            for column in range(self.width()):
                if row == 0:                                                #edge case for topmost
                    minCost[0][column] = energyArray[0][column]
                else:
                    if column == 0:                                         #edge case for left corner
                        OnTop = minCost[row-1][column]
                        TopRight = minCost[row-1][column+1]
                        minCost[row][column] = energyArray[row][column] + min(OnTop, TopRight)  #determine the minimum and assign it
                    elif column == self.width()-1:                          #edge case for right corner 
                        OnTop = minCost[row-1][column]
                        TopLeft = minCost[row-1][column-1]
                        minCost[row][column] = energyArray[row][column] + min(OnTop, TopLeft)   #determine the minimum and assign it
                    else:
                        OnTop = minCost[row-1][column]
                        TopRight = minCost[row-1][column+1]
                        TopLeft = minCost[row-1][column-1]
                        minCost[row][column] = energyArray[row][column] + min(OnTop,TopRight,TopLeft)   #determine the minimum and assign it

        lastRow = [0]*self.width()                                                  #code until line 92 is to find the minimum energy pixel of the final row
        rowCounter = 0
        while rowCounter < self.width():
            lastRow[rowCounter] = minCost[self.height()-1][rowCounter]
            rowCounter += 1
        startingPoint = lastRow.index(min(lastRow))
        seam = [startingPoint]                                                      #we then create a list containing the index of the column of the pixel with lowest mincost

        for row in range(self.height()-2, -1, -1):                                  #range arguments are: starting value, bound, and step
            indexOfSeamBelow = seam[-1]                                             #always get the item that is added last into the list to get the most recent index of the seam
            smallestValue = 0                                                       #smallestValue will be used to determine whether the middle, left, or right pixel will be the next seam index

            if indexOfSeamBelow == 0:
                mid = minCost[row][indexOfSeamBelow]
                right = minCost[row][indexOfSeamBelow + 1]
                smallestValue = min(mid, right)
                if smallestValue == mid:
                    seam.append(indexOfSeamBelow)
                else:
                    seam.append(indexOfSeamBelow+1)

            elif indexOfSeamBelow == self.width()-1:
                mid = minCost[row][indexOfSeamBelow]
                left = minCost[row][indexOfSeamBelow - 1]
                smallestValue = min(mid, left)
                if smallestValue == mid:
                    seam.append(indexOfSeamBelow)
                else:
                    seam.append(indexOfSeamBelow - 1)
            
            else:
                mid = minCost[row][indexOfSeamBelow]
                right = minCost[row][indexOfSeamBelow+1]
                left = minCost[row][indexOfSeamBelow-1]
                smallestValue = min(mid, right, left)
                if smallestValue == mid:
                    seam.append(indexOfSeamBelow)
                elif smallestValue == right:
                    seam.append(indexOfSeamBelow + 1)
                else:
                    seam.append(indexOfSeamBelow - 1)

        seam.reverse()                                                                  #reversed at the end since the order of this was bottom up, and new values were appended so the first value in the index is the seam at the bottom.
        return seam                                                         

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        
        newImage = {}                                                                   #instantiate new dictionary for new set of pixels
        for row in range(self.height()):
            for col in range(self.width()):
                newImage[(row, col)] = self[(col, row)]                                 #switch the x to y and y to x to amke the pic flip in the y = x line

        width = self.height()                                                           #makes it easier for us to create our new image 
        height = self.width()

        tempPic = Image.new('RGB', (width, height))                                     #new image created based on new dictionary
        pixels = [newImage[(x, y)] for y in range(height) for x in range(width)]        #new list of pixels based on newImage

        tempPic.putdata(pixels)                                                         #put new pixels into old canvas

        seamCarveClass = SeamCarver(tempPic)                                            #run seamCarver findvertical on the flipped image, giving the the horizontal seam
        seam = seamCarveClass.find_vertical_seam()

        return seam

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        if self.width() == 1:                                                           #error handling
            raise SeamError("Cannot remove vertical seam. Image only has a width of 1.")
        elif len(seam) != self.height():
            raise SeamError("Invalid seam length.")
        for element in range(len(seam)-1):
            difference = abs(seam[element] - seam[element+1])
            if difference > 1:
                raise SeamError("Invalid seam.")

        for row in range(self.height()):
            seamColumn = seam[row]                                                      #means that it will start from the column of the seam
            for column in range(seamColumn, self.width()-1):
                self[column, row] = self[column+1, row]                                 #then it shifts all columns to the left except for the last one
            del self[self.width()-1, row]                                               #then delete the last column 
                                                                                        #repeat until all the seams are gone
        self._width -= 1                                                                #then update width of image                    
        

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''

        newImage = {}                                                                   #same as find_horizontal, where we transpose picture
        for row in range(self.height()):
            for col in range(self.width()):
                newImage[(row, col)] = self[(col, row)]

        width = self.height()
        height = self.width()

        tempPic = Image.new('RGB', (width, height))
        pixels = [newImage[(x, y)] for y in range(height) for x in range(width)]
        tempPic.putdata(pixels)

        seamCarveClass = SeamCarver(tempPic)

        seamCarveClass.remove_vertical_seam(seam)                                       #run remove vertical seam on transposed

        self._height -= 1                                                               #edit the height 
        self.clear()

        for row in range(seamCarveClass.height()):                                      #repopulate the image
            for col in range(seamCarveClass.width()):
                self[(row, col)] = seamCarveClass[(col, row)]
        
class SeamError(Exception):
    pass
