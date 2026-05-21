import pygame as pg
import math as m 
from player import player as pl
from tower import tower as tr

#start object definitions

colors = {
    "fillBlue": (63,127,192),
    "borderBlue":  (63,160,192)
}

class gameArena():

    def __init__(self):

        pg.init()
        screen = pg.display.set_mode((1200, 600)) #creates a window

        surface = pg.Surface((1200, 600)) #creates a surface that can be interacted with
        surface.fill((0,63,95))   #changes the color of the surface (so we can see it)

        running = True
        self.screen = screen
        self.surface = surface
        self.running = running

        self.arenaType = "hexagonal"
        self.hexSize = 20
        self.arenaSize = 8


    def drawRegularPolygon(self, sides = 3, radius = 10 , center = [0,0], orientation = 0.0, color = (63,127,192)):
        coords = []
        for i in range(0,sides):
            xOffset = radius*m.cos(i* 2*m.pi / sides + orientation)
            yOffset = radius*m.sin(i* 2*m.pi / sides + orientation)
            x = xOffset + center[0]
            y = yOffset + center[1]
            coords.append((x,y))
        pg.draw.polygon(self.surface, color, coords)

    def drawRectangularHexGrid(self, gridOrigin, hexSize = 50, numX = 12, numY = 6, spacing = 0 , border = 5, windowSizeY=600, fillColor = (63,127,192), borderColor = (63,160,192)):
        #draw a hexagon grid
        d = int(2*hexSize*m.sqrt(3)/2) #distance between centers perpendicular to edge
        endX = int(gridOrigin[0] + numX*d)
        endY = int(gridOrigin[1]+ hexSize*3 * numY/2) # +y is down by default so I reverse it with endY -y 
        for x in range (gridOrigin[0], endX, d):
            for y in range (gridOrigin[1], endY, hexSize*3):
                self.drawRegularPolygon(6, hexSize, [x,windowSizeY-y], m.pi/6, fillColor)
                self.drawRegularPolygon(6, hexSize-border, [x,windowSizeY-y], m.pi/6, borderColor)
                
                self.drawRegularPolygon(6, hexSize, [x+d/2, windowSizeY-y-hexSize*1.5],m.pi/6, fillColor)
                self.drawRegularPolygon(6, hexSize-border, [x+d/2, windowSizeY-y-hexSize*1.5],m.pi/6, (63,160,192))

    def drawAtHexCoordinate(self, coordinate, hexSize = 20, gridOrigin = [600,300], border = 2, color1 = "orange", color2 = "yellow", windowSizeY=600):
        #y-axis on hex grid is pi/3 counterclockwise from horizontal, +y is down
        xCartesian = gridOrigin[0] + int(hexSize * ( coordinate[0]*m.sqrt(3) + coordinate[1]*m.sqrt(3)/2 ))
        yCartesian = gridOrigin[1] + int(hexSize * coordinate[1]*3/2)
        self.drawRegularPolygon(6, hexSize, [xCartesian, windowSizeY - yCartesian], m.pi/6, color1)
        self.drawRegularPolygon(6, hexSize-border, [xCartesian, windowSizeY - yCartesian], m.pi/6, color2)

    def simStack(self, coordinate, height = 1, hexSize = 20,  border = 2, gridOrigin = [600,300], color1 = "orange", color2 = "yellow", color3 = "lime", windowSizeY=600):
        #y-axis on hex grid is pi/3 counterclockwise from horizontal, +y is down
        xCartesian = gridOrigin[0] + int(hexSize * ( coordinate[0]*m.sqrt(3) + coordinate[1]*m.sqrt(3)/2 ))
        yCartesian = gridOrigin[1] + int(hexSize * coordinate[1]*3/2)
        self.drawRegularPolygon(6, hexSize, [xCartesian, windowSizeY - yCartesian], m.pi/6, color1)
        self.drawRegularPolygon(6, hexSize-border, [xCartesian, windowSizeY - yCartesian], m.pi/6, color2)
        #self.drawRegularPolygon(6, hexSize-2*border, [xCartesian, windowSizeY - yCartesian], m.pi/6, color3)
    
    def calcTileDistance(c1, c2) : # use coordinate pair as [x,y]
        d = (abs(c1[0]-c2[0])+ abs(c1[1]-c2[1]) + abs(c1[0]+c1[1]-(c2[0]+c2[1])))/2
        return d 
    
    def drawHexagonalArena(self, arenaSize, hexSize):
        currentPos = [0,0]
        for i in range(1,self.arenaSize+1):
            for loopSize in range(0, i+1):
                for dir in list([self.hexD["e"],self.hexD["nw"],self.hexD["w"],self.hexD["sw"],self.hexD["se"],self.hexD["e"],self.hexD["ne"],self.hexD["w"]]):
                    for step in range(1, loopSize+1):
                        self.drawAtHexCoordinate([currentPos[0] + dir[0], currentPos[1] + dir[1]], self.hexSize, border= self.hexSize /10, color1 = colors["fillBlue"], color2 = colors["borderBlue"])
                        currentPos[0] = currentPos[0] + dir[0]
                        currentPos[1] = currentPos[1] + dir[1]

    hexD = { #hex Direction vectors written as a dictionary for user inputs 
        "e": [1,0],
        "ne": [0,1],
        "nw": [-1,1],
        "w": [-1,0],
        "sw": [0,-1],
        "se": [1,-1]
    }
    
    #def generateArena(self, players = player()): #enter a player()       
         

    def updateArena(self, playerRoster = pl(), tracer = None): #enter a player()       
        
        self.screen.fill((0, 0, 0))          
        self.screen.blit(self.surface, (0, 0)) #pastes the surface onto the window so we can draw on part (in this case all) of the window
        self.drawHexagonalArena(self.arenaSize, 20)

        #self.drawAtHexCoordinate(tracer.pos, 20, [600,300], 2, color1 = tracer.borderColor, color2 = tracer.fillColor)
        for p in playerRoster:
            for tower in range(0,len(p.army)):
                self.drawAtHexCoordinate(p.army[tower].pos, 20, [600,300], 2, color1 = p.army[tower].borderColor, color2 = p.army[tower].fillColor)
                 #update drawing
                #print(p.army[tower].pos)
        pg.display.flip()