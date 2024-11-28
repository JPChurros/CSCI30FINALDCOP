#!/usr/bin/env python3
from picture import Picture
from PIL import Image

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        if i < 0 or i >= self.width() or j < 0 or j >= self.height():
            raise IndexError("Pixel is out of bounds.")

        if i-1 < 0: 
            left_pixel = self[self.width()-1,j]
            right_pixel = self[i+1,j]
        elif i+1 >= self.width():
            left_pixel = self[i-1,j]
            right_pixel = self[0,j]
        else:
            left_pixel = self[i-1,j]
            right_pixel = self[i+1,j]

        if j-1 < 0:            
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

    def find_vertical_seam(self) -> list[int]: #Note, idk sometimes when to subtract one to set the size
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        energyArray = [[0] * self.width() for i in range(self.height())] #creates a 2dimensional energyArrayay of size width and height!
        #idk if this may -1 for the width and shit ah.
        for row in range(self.height()):
            for column in range(self.width()):
                energyArray[row][column] = self.energy(column, row) #populates the 2dimensional energyArrayay with the corresponding energy for each ano.
        #energyArrayay two
        
        minCost = [[0] * self.width() for i in range(self.height())]
        #idk if this has -1 for the width or height bro
        for row in range(self.height()):
            for column in range(self.width()):
                #edge case for pinakataas
                if row == 0:
                    minCost[0][column] = energyArray[0][column]
                else:
                    #edge case for left corner
                    if column == 0:
                        OnTop = minCost[row-1][column]
                        TopRight = minCost[row-1][column+1]
                        #determine the minimum and assign it
                        minCost[row][column] = energyArray[row][column] + min(OnTop, TopRight)
                    #edge case for right corner idk if may minus one dito
                    elif column == self.width()-1:
                        OnTop = minCost[row-1][column]
                        TopLeft = minCost[row-1][column-1]
                        #determine the minimum and assign it
                        minCost[row][column] = energyArray[row][column] + min(OnTop, TopLeft)
                    else:
                        OnTop = minCost[row-1][column]
                        TopRight = minCost[row-1][column+1]
                        TopLeft = minCost[row-1][column-1]
                        minCost[row][column] = energyArray[row][column] + min(OnTop,TopRight,TopLeft)

                # #middle! , check first if assigned value has laman cuz if meron then its an edge case
                # if AssignedValue == 0:
                #     OnTop = energyArray[row-1][column]
                #     TopRight = energyArray[row-1][column+1]
                #     TopLeft = energyArray[row-1][column-1]
                #     AssignedValue = min(OnTop, TopRight, TopLeft)   
                
                # minCost[row][column] = AssignedValue + energyArray[row][column]
        # this part gets the index of the smallest value sa last row sa minCost 2d array
        lastRow = [0]*self.width()
        rowCounter = 0
        while rowCounter < self.width():
            lastRow[rowCounter] = minCost[self.height()-1][rowCounter]
            rowCounter += 1
        startingPoint = lastRow.index(min(lastRow))

        # this "instantiates" the seam list, and then i decided to add na agad the startingPoint variable sa last element ng list

        seam = [startingPoint]
        # similar logic to what you guys worked with, it ends at row 0 
        for row in range(self.height()-2, -1, -1):
            indexOfSeamBelow = seam[-1]
            smallestValue = 0

            #mid right and left are just essentially OnTop, TopRight, TopLeft, respectively.
            #indexOfSeamBelow is just referring to index of seam below
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

        seam.reverse()
        return seam

        raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        #instantiate new dictionary for new set of pixels
        newImage = {}
        for row in range(self.height()):
            for col in range(self.width()):
                #switch the x to y and y to x to amke the pic flip in the y = x line
                newImage[(row, col)] = self[(col, row)]

        #makes it easier for us to create our new image
        width = self.height()
        height = self.width()

        #new image created based on new dictionary
        tempPic = Image.new('RGB', (width, height))
        #new list of pixels based on newImage
        pixels = [newImage[(x, y)] for y in range(height) for x in range(width)]
        #put new pixels into old canvas
        tempPic.putdata(pixels)

        #run seamCarver findvertical on the flipped image, giving the the horizontal seam
        seamCarveClass = SeamCarver(tempPic)
        seam = seamCarveClass.find_vertical_seam()

        return seam
    
        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        if self.width() == 1:
            raise SeamError("Cannot remove vertical seam. Image only has a width of 1.")
        elif len(seam) != self.height():
            raise SeamError("Invalid seam length.")
        for element in range(len(seam)-1):
            difference = abs(seam[element] - seam[element+1])
            if difference > 1:
                raise SeamError("Invalid seam.")

        for row in range(self.height()):
            seamColumn = seam[row]
            for column in range(seamColumn, self.width()-1):
                self[column, row] = self[column+1, row]
            del self[self.width()-1, row]
        self._width -= 1
        

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''

        #basically the same as find_horizontal, where we transpose picture
        newImage = {}
        for row in range(self.height()):
            for col in range(self.width()):
                newImage[(row, col)] = self[(col, row)]

        width = self.height()
        height = self.width()

        tempPic = Image.new('RGB', (width, height))
        pixels = [newImage[(x, y)] for y in range(height) for x in range(width)]
        tempPic.putdata(pixels)

        seamCarveClass = SeamCarver(tempPic)

        #run remove vertical seam on transposed
        seamCarveClass.remove_vertical_seam(seam)

        #edit the height to be the removed amount
        self._height -= 1
        self.clear()

        #repopulate the image
        for row in range(seamCarveClass.height()):
            for col in range(seamCarveClass.width()):
                self[(row, col)] = seamCarveClass[(col, row)]
        
class SeamError(Exception):
    pass
