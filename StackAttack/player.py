import pygame as pg
import math as m 
from tower import tower

class player:
    def __init__(self, name = "null"):
        self.sources = 1 
        self.name = name
        self.army = [tower()] #a set of towers the player controls; this is kept in a list so more can be added and indexed without being named
        self.score = 0  #might be used for testing games
        self.pastMoves  = [[],[],[]] #will be entered pieces, directions, and movements. Not implemented yet
    
    def addPiece(self, tower, type): #see equivalent function in tower.py for details
        match type:
            case "move":
                self.army[tower].addPiece("move") #increases moves after the last direction change piece added
            case "turn":
                self.army[tower].addPiece("turn") #adds a direction change and starts a new move count
            case "control":
                self.army[tower].addPiece("control")
            case "initiative":
                self.army[tower].addPiece("initiative") #adds initiative
            case "split":
                self.army[tower].addPiece("split")
                #self.splitTower(tower)
            case "pass":
                print("input entered")
            case _:
                print("please enter a valid input")
    def removePiece(self, tower, type):
        match type:
            case "move":
                self.army[tower].removePiece("move") 
            case "turn":
                self.army[tower].removePiece("turn") 
            case "control":
                self.army[tower].removePiece("control")
            case "initiative":
                self.army[tower].removePiece("initiative") #adds initiative
            case "split":
                self.army[tower].removePiece("initiative")
            case "pass":
                print("input entered")
            case _:
                print("please enter a valid input")

    def moveTower(self, tower, directions, distances = None, Grid = 0): #directions should be a vector containing one of the hex directions (see line 29)
        distances = distances or []
        self.army[tower].move(directions, distances, grid = Grid)
    def testMoveTower(self, tower, directions, distances = None, Grid = 0): #directions should be a vector containing one of the hex directions (see line 29)
        distances = distances or []
        inBounds = self.army[tower].testMove(directions, distances, grid = Grid)
        return inBounds

    def splitTower(self, tower): #creates new tower by separating a tower's move pattern at the split point; different than adding a split piece
                                 #while each piece can do this, it is defined here because this move affects the whole army vector
        newTowerMoves = self.army[tower].sections[-1].moveCount #saves move pattern of last section
        self.army[tower].sections.pop(-1) #removes the duplicate move pattern from the old piece
        self.army.append(tower()) #adds a new tower
        self.army[tower + 1].sections[-1].moveCount = newTowerMoves #transfers move pattern to new tower

    def splitAndMoveTower(self,tower,directions,distances):
        self.splitTower(tower) 
        self.moveTower(tower+1, directions, distances)

    def actionTotal(self): #calculates the total number of actions the player can take
        actionCount = self.sources
        for towerNum in range(1,len(self.army)):
            actionCount += len(self.army[towerNum].sections)
        return actionCount
