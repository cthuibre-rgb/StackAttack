import pygame as pg
import math as m 

class tower:  #game piece made of stacks of smaller sections that the player moves
    def  __init__(self, id = 0, pos = None, freemove = True, fillColor = "yellow", borderColor = "orange"):
        self.id = id
        self.freemove = freemove
        self.pos = pos or [0,0] # x, y hex position coordinates; x is right or east, y is up-right or northeast
        self.sections = [self.section()] #start with a default section, sections contain the move patterns so that they can be split off later
        self.validMove = False
        self.testPos = self.pos.copy()
        self.fillColor = fillColor
        self.borderColor = borderColor
    
    
    def addPiece(self, type): #from now on use add piece in player
        match type:
            case "move":  #this increases max movement. You can only maxmove if freemove is off.
                self.sections[-1].moveCount[-1] += 1 #increases moves after the last direction change piece added
                self.endPiece = "m"
                if self.sections[-1].PTS[-1] != "m": #adds next move to movement tracker sequence
                    self.sections[-1].PTS.append("m")
                else:
                    self.sections[-1].PTQ[-1] += 1
            case "turn":
                self.sections[-1].moveCount.append(0) #adds a direction change and starts a new move count
                self.sections[-1].maxVariance.append(0) #aligns move variance index (control pieces) with move index
                self.endPiece = "turn"
                if self.sections[-1].PTS[-1] != "t":
                    self.sections[-1].PTS.append("t")
                else:
                    self.sections[-1].PTQ[-1] += 1
            case "control": #each of these added after a turn piece (not game turn) allows the player to move one less than the maximum if freemove is off
                self.sections[-1].maxVariance[-1] += 1
                self.endPiece = "control"
                if self.sections[-1].PTS[-1] != "c":
                    self.sections[-1].PTS.append("c")
                else:
                    self.sections[-1].PTQ[-1] += 1
            case "initiative":
                self.sections[-1].initiative += 1 #adds initiative
                self.endPiece = "initiative"
                if self.sections[-1].PTS[-1] != "i":
                    self.sections[-1].PTS.append("i")
                else:
                    self.sections[-1].PTQ[-1] += 1
            case "split":
                self.sections.append(self.section())
                if self.sections[-1].PTS[-1] != "s":
                    self.sections[-1].PTS.append("s")
                else:
                    self.sections[-1].PTQ[-1] += 1
            case "pass":
                print("input entered")
            case _:
                print("please enter a valid input")  

    def removePiece(self, type = "lastPiece"):
        #warning: the order they are added is not tracked. only turns can be distinguished as they add an element to the moveCount/max move and moveVariance/control vectors
        #by default pieces are removed in the following order
            # 1. last piece added
            # 2. controls after last turn
            # 3. moves after last turn
            # 4. last turn
            # 5. initiative

        if type == "lastPiece":
            type = self.sections[-1].PTS[-1]
        if self.sections[-1].PTQ[-1] > 0:
            self.sections[-1].PTQ[-1] -= 1
        else:
            self.sections[-1].PTS.pop(-1)

        match type:
            case "m":
                self.sections[-1].moveCount[-1] -= 1   
            case "t":
                self.sections[-1].moveCount.pop(-1) 
                self.sections[-1].maxVariance.pop(-1)
            case "c":
                self.sections[-1].maxVariance[-1] -= 1
            case "i":
                self.sections[-1].initiative -= 1 
            case "s":
                self.sections.remove(self.section(-1))


    def tileMove(self, direction, grid):
        self.pos[0] += direction[0]
        self.pos[1] += direction[1]
        grid.screen.fill((0, 0, 0))          
        grid.screen.blit(grid.surface, (0, 0)) #pastes the surface onto the window so we can draw on part (in this case all) of the window
        grid.drawHexagonalArena(8, 20)
        grid.drawAtHexCoordinate(self.pos, 20, [600,300], 2)
        pg.time.delay(100)
        pg.display.flip()

    #move uses the grid variables as a parameter. This makes gameArena and tower interdependent, although gameArena is not imported

    def move(self, directions, distances = [], gameSpeed = 20, grid = 0): #directions should be a vector containing one of the hex directions (see line 29)
        
        for sectNum in range (0, len(self.sections)): #iterates through all sections

            j = 0 #loop defaults to max movement; these two lines only affect function when freemove is enabled or maxVariance is changed
            #not reset in loop to allow multiple sections to take affect
            maxVariance = self.sections[sectNum].maxVariance
            
            for moveDist in self.sections[sectNum].moveCount: #iterates through each movement after the last direction change. defaults to max movement stored in move count

                if len(distances) == len(self.sections[sectNum].moveCount):  #this container allows adjustment of movement from moveDist 
                    if self.freemove or (distances[j] < moveDist or self.freemove and distances[j] > moveDist - maxVariance[j]) :
                        moveDist = distances[j]
                    elif distances[j] < moveDist - maxVariance[j]:
                        moveDist =  moveDist - maxVariance
                    #else: original (maximum) value                    
                        
                for i in range(0, int(moveDist)): #new move command, increments for smooth animation
                    print(directions[j])
                    self.tileMove(directions[j], grid)
                    self.validMove = True
                    self.testPos = self.pos

                j += 1 #the original loop used moveCount only, so an increment variable was added
                print(j)
                print(sectNum)
                print(self.sections[sectNum].moveCount)

    

    #def updatePastPos(self):    # used to make movement smooth  
        #self.pastPos = self.pos      

    def testMove(self, directions, distances = [], gameSpeed = 20, grid = 0):
        self.validMove = True
        self.testPos = self.pos.copy()
        for sectNum in range (0, len(self.sections)): #iterates through all sections

            j = 0 #loop defaults to max movement; these two lines only take affect when freemove is enabled or maxVariance is changed
            #not reset in loop to allow multiple sections to take affect
            maxVariance = self.sections[sectNum].maxVariance

            for moveDist in self.sections[sectNum].moveCount: #iterates through each movement after the last direction change. defaults to max movement stored in move count
                
                    if len(distances) == len(self.sections[sectNum].moveCount):  #this container allows adjustment of movement from moveDist given user input
                        if self.freemove or (distances[j] < moveDist or self.freemove and distances[j] > moveDist - maxVariance[j]) :
                            moveDist = distances[j]
                        elif distances[j] < moveDist - maxVariance[j]:
                            moveDist -=  maxVariance

                    for i in [0,1]: #old move command, repurposed for testing boundaries to prevent illegal movement
                        self.testPos[i] += moveDist*directions[j][i] #for each section, follow move instructions
                    

                    if m.hypot(self.testPos[0], self.testPos[1]) > grid.arenaSize : #test if coordinate is outside the arena
                        self.validMove = False

        return self.validMove



    class section: #tower section made of smaller pieces. can split off to become new tower or rejoin

        def  __init__(self, id = 0, initiative = 0, moveCount = None, maxVariance = None,  PTS = None, PTQ = None):
            self.id = id
            self.initiative = initiative
            self.moveCount = moveCount or [0] #number of moves in each direction, seperated by each direction changes
            self.maxVariance = maxVariance or [0]
            self.PTS = PTS or ["i"] #piece type sequence
            self.PTQ = PTQ or [0] #piece type quantity

    def getMovePattern(self):
        self.totalMovePattern = []
        for sectNum in self.sections:
            self.totalMovePattern.append(sectNum.moveCount)
        return self.totalMovePattern
    

#strategy thoughts: 
# adding move pieces (max movement) could decrease chance of getting trapped, but also limit moves.
# direction changes help create a variety of unique move needed for a strategically complicated setups (like how knights and queens fork can fork each other in chess, but likely more complicated)
# control pieces preven the piece from being trapped in small areas such as opponent wall or corners, but must be balanced with (and are useless without) move pieces