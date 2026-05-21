#setup for a game concept in which the players build their own pieces and their movement patterns
#the game is turn/round based, however the players move pieces by their initiative (like players/monsters in D&D);
#however, unlike other games, there is no tiebreaker. Players will race to move their pieces of the same initiative.

#towers cannot move through each other
#towers are captured by surrounding them on at least three sides
#towers have one turn to escape ~completely surrou

#towers can be collapsed in a line, (or other patterns later if determined)
#towers can be split at designated split pieces into smaller towers, and move normally 

import pygame as pg
import math as m 

#start object definitions

#colors 
fillBlue = (63,127,192)
borderBlue = (63,160,192)

class gameMap():    
    def __init__(self):
        pass
    def drawRegularPolygon(self, sides = 3, radius = 10 , center = 0, orientation = 0, color = (63,127,192)):
        coords = []
        for i in range(0,sides):
            xOffset = radius*m.cos(i* 2*m.pi / sides + orientation)
            yOffset = radius*m.sin(i* 2*m.pi / sides + orientation)
            x = xOffset + center[0]
            y = yOffset + center[1]
            coords.append((x,y))
        pg.draw.polygon(surface, color, coords)

    def drawRectHexGrid(self, gridOrigin, hexSize = 50, numX = 12, numY = 6, spacing = 0 , border = 5, windowSizeY=600, fillColor = (63,127,192), borderColor = (63,160,192)):
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

    def drawAtHexCoordinate(self, coordinate, gridOrigin = [600,300], hexSize = 50, border = 5, color1 = "orange", color2 = "yellow", windowSizeY=600):
        #y-axis on hex grid is pi/3 counterclockwise from horizontal, +y is down
        xCartesian = gridOrigin[0] + int(hexSize * ( coordinate[0]*m.sqrt(3) + coordinate[1]*m.sqrt(3)/2 ))
        yCartesian = gridOrigin[1] + int(hexSize * coordinate[1]*3/2)
        self.drawRegularPolygon(6, hexSize, [xCartesian, windowSizeY - yCartesian], m.pi/6, color1)
        self.drawRegularPolygon(6, hexSize-border, [xCartesian, windowSizeY - yCartesian], m.pi/6, color2)


class tower:  #game piece made of stacks of smaller sections that the player moves
    def  __init__(self, id = 0, pos = [0,0], freemove = True):
        self.id = id
        self.freemove = freemove
        self.pos = pos # x, y hex position coordinates
        self.sections = [self.section()] #start with a default section
    
    def addPiece(self, type):
        match type:
            case "move":
                self.sections[-1].moveCount[-1] += 1 #increases moves after the last direction change piece added
            case "turn":
                self.sections[-1].moveCount.append(0) #adds a direction change and starts a new move count
            case "initiative":
                self.sections[-1].initiative += 1 #adds initiative
            case "split":
                self.sections.append(self.section())
            case "pass":
                print("input entered")
            case _:
                print("please enter a valid input")       

    def move(self, directions, distances = "placeholder"): #directions should be a vector containing one of the hex directions (see line 29)
        for sectNum in range (0, len(self.sections)): #iterates through all sections
            j = 0
            for moveDist in self.sections[sectNum].moveCount: #iterates through each movement
                
                if len(distances) == len(self.sections[sectNum].moveCount):
                    if distances[j] < moveDist and self.freemove : #movement limiter
                        moveDist = distances[j]

                for i in [0,1]: #iterates through each coordinate
                    self.pos[i] += moveDist * directions[j][i] #for each section, follow move instructions
                
                j += 1
                print(j)
                print(self.pos)
    class section: #tower section made of smaller pieces. can split off to become new tower or rejoin

        def  __init__(self, id = 0, initiative = 0, moveCount = [0] ):
            self.id = id
            self.initiative = initiative
            self.moveCount = moveCount #number of moves in each direction, seperated by each direction changes
            turns = len(moveCount) #total number of direction changes

class player:
    def __init__(self):
        self.army = [tower()] #a set of towers the player controls; this is kept in a list so more can be added and indexed without being named
        self.score = 0  #might be used for testing games

    def split(self, towerNum, direction): #creates new tower by separating a tower's move pattern at the split point
                                          #while each piece can do this, it is defined here because this move affects the whole army vector
        newTowerMoves = self[towerNum].moveCount[-1]
        self.append(towerNum(moveCount = newTowerMoves)) #takes the move pattern after the split point, and adds it as a separate piece
        self[towerNum].moveCount.pop(-1) #removes the duplicate move pattern from the old piece, now the 

def calcTileDistance(c1,c2) : # use coordinate pair as [x,y]; no need for this yet
    d = (abs(c1[0]-c2[0])+ abs(c1[1]-c2[1]) + abs(c1[0]+c1[1]-(c2[0]+c2[1])))/2
    return d 

hexD = { #hex Direction vectors written as a dictionary for user inputs 
    "e": [1,0],
    "ne": [0,1],
    "nw": [-1,1],
    "w": [-1,0],
    "sw": [0,-1],
    "se": [1,-1]
}

#distance = (abs(x)+ abs(y) + abs(x+y))/2

#colors


#test tower move function

#testTower = tower(1, [0, 0])
#print(testTower.pos)
#testTower.sections[0].moveCount = [4,1,2,2]
#print(testTower.sections[0].moveCount)
#testTower.move([hexD["e"],hexD["sw"],hexD["ne"],hexD["nw"]],[3,1,2,6])
#print('\n')

#test creating pieces for player
# p1 = player()
# for i in range(0,7):
#     p1.army[0].addPiece("move")
# print(p1.army[0].sections[0].moveCount)

# p1.army[0].move([e],[7])
# pos1 = p1.army[0].pos.copy()

# p1.army[0].addPiece("turn")
# print(p1.army[0].sections[0].moveCount)
# for i in range(0,1):
#     p1.army[0].addPiece("move")
# print(p1.army[0].sections[0].moveCount)

# p1.army[0].move(["ne","nw"],[2,2])


pieceType = "placeholder"
playerDirs = []
playerDist = []
samplePlayer = player()

towerNum = 1
pieceAddingMessage = "You may add a piece to tower " + str(towerNum) + ". Enter move, initiative, turn, or split to choose the piece type: \n"
while pieceType != "pass":
    pieceType = input(pieceAddingMessage)
    samplePlayer.army[0].addPiece(pieceType)
for i in range(0, len(samplePlayer.army[0].sections[0].moveCount)):
    directionInput = input("Enter the direction you want to move:\n")
    playerDirs.append(hexD[directionInput])

print(playerDirs)
samplePlayer.army[0].move(playerDirs)


    #     playerDist.append(int(input("Enter the distance you want to move \n")))


#     print(playerDirs)
#     print(playerDist)
#     p1.army[0].move(playerDirs, playerDist)
#     print(p1.army[0].pos)
#     towerNum +=1


map1 = gameMap()
pg.init()
screen = pg.display.set_mode((1200, 600)) #creates a window

surface = pg.Surface((1200, 600)) #creates a surface that can be interacted with
surface.fill((0,63,95))   #changes the color of the surface (so we can see it)


def updateMap(samplePlayer): #enter a player object
    
    running = True
    
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))          
        screen.blit(surface, (0, 0)) #pastes the surface onto the window so we can draw on part (in this case all) of the window  
        
        #test coordinate grid
        map1.drawRectHexGrid([100,100], 50)
        map1.drawAtHexCoordinate(samplePlayer.army[0].pos, [100,100])
        pg.display.flip() #update drawing

    pg.quit()

updateMap(samplePlayer)







# idea for power up piece (can be collected)): 
    # wheel (common): direction changes do not have to be used for towers, and pieces may move backwards (might be the default)
    # blade (common): towers can collapse in symmetrical directions (2,3,or 6 if hex)
    # weight (common): one tower can collapse other towers like dominos and capture any overlapping pieces ~probably hard to implement and/or strategize around

    # source (rare): one extra piece can be added for each turn ~probably necessary to make games faster
    # brakes (rare) : movements do not have to be used for tower
    # ghost (rare): pieces can move through others, but piece does not count in scoring (does not need to be captured to win)

    # crusher (very rare): one tower can capture other towers by landing on it 
    # gear (extremely rare): collapsing can happen in a chain (any direction other than backwards) for any one piece ~probably hard to implement and strategize around
