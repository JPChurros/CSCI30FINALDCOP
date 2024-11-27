#!/usr/bin/env python3
from picture import Picture

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
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

        raise NotImplementedError

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

        seam = [(self.height()-1, startingPoint)]
        # similar logic to what you guys worked with, it ends at row 0 
        for row in range(self.height()-2, -1, -1):
            indexOfSeamBelow = seam[-1][1]
            smallestValue = 0

            #mid right and left are just essentially OnTop, TopRight, TopLeft, respectively.
            #indexOfSeamBelow is just referring to index of seam below
            if indexOfSeamBelow == 0:
                mid = minCost[row][indexOfSeamBelow]
                right = minCost[row][indexOfSeamBelow + 1]
                smallestValue = min(mid, right)
                if smallestValue == mid:
                    seam.append(row, indexOfSeamBelow)
                else:
                    seam.append(row, indexOfSeamBelow+1)

            elif indexOfSeamBelow == self.width()-1:
                mid = minCost[row][indexOfSeamBelow]
                left = minCost[row][indexOfSeamBelow - 1]
                smallestValue = min(mid, left)
                if smallestValue == mid:
                    seam.append(row, indexOfSeamBelow)
                else:
                    seam.append(row, indexOfSeamBelow - 1)
            
            else:
                mid = minCost[row][indexOfSeamBelow]
                right = minCost[row][indexOfSeamBelow+1]
                left = minCost[row][indexOfSeamBelow-1]
                smallestValue = min(mid, right, left)
                if smallestValue == mid:
                    seam.append(row, indexOfSeamBelow)
                elif smallestValue == right:
                    seam.append(row, indexOfSeamBelow + 1)
                else:
                    seam.append(row, indexOfSeamBelow - 1)

        return seam.reverse()

        raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        #Steps:
        #1 get original picture's dictionary
        #2 transpose
        #3 turn it back into a dictionary so it can be used ulit for picture
        #4 call variable.findverticalseam()
        #5 transpose the final list
        # :D

        #1, i wanna get the orig dictionary and turn it into a 2d array so its easier to transpose.
        pictureObject = Picture(self)
        origDictionary = pictureObject #now we have the orig dictionary
        width = origDictionary.width()
        height = origDictionary.height()

        #turn into 2d array
        origArray = [[0] * width for _ in range(height)]
        for row in range(height):
            for column in range(width):
                #if(row, column) in origDictionary:
                origArray[row][column] = origDictionary[row, column]
        
        #2 transpose the 2dimensional array
        n = len(origArray)
        for i in range(n):
            for j in range(1 + 1, n):
                origArray[i, j], origArray[j, i] = origArray[j][i], origArray[i, j]
        #orig array has now been transposed

        #3 turn it back into a dictionary
        transposedDictionary = Picture(self)
        for row in range(width):
            for column in range(height):
                transposedDictionary[row, column] = origArray[row][column]
        #4 call variable.findverticalseam
        seam = transposedDictionary.find_vertical_seam()
        #5 ? is there even a need to transpose the final seam
        return seam

        transposedPic = Picture()
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
