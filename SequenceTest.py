from gameArena import gameArena
from player import player #(from fileName, import className): the class has the same name as the file and I don't want to type tower.tower or player.player 
from tower import tower
import math as m
import pygame as pg

players = [] #vector for storing players
hexGrid = gameArena() #does not build the grid, but creates an object that can

#tracer = tower(freemove = True, fillColor = "orange") #shows moves before they are confirmed
players.append(player("Player 1"))
#players.append(player("Player 2"))

playerDirs = []
playerDist = []

hexD = { #hex Direction vectors written as a dictionary for user inputs 
        "e": [1,0],
        "ne": [0,1],
        "nw": [-1,1],
        "w": [-1,0],
        "sw": [0,-1],
        "se": [1,-1]
    }

print("\n")
print(len(players))
print("\n")
print(len(players[0].army))
print("\n")
#print(len(players[1].army))
print("\n")

pieceType = "null"
pieceAddingInput = ", you may add a piece to tower " + ". Enter 'move', 'initiative', 'turn', or 'split' to choose the piece type: \n"


pg.init()
screen = pg.display.set_mode((1200, 600)) #creates a window

surface = pg.Surface((1200, 600)) #creates a surface that can be interacted with
surface.fill((0,63,95))   #changes the color of the surface (so we can see it)
running = True 
testP = 0 #  player number 
testTower = 0
directionInput = []
testMovePattern = players[testP].army[testTower].getMovePattern()
moveNum = 0

print("press '+' to add a movement to a piece, '.' to add a direction change, and '-' to remove a piece")
print("To move, use the six keys surrounding the period to enter the directions you want to go in a sequence.")
print("If you want to undo the movement, press Z (no ctrl). To begin moving, press enter/return.")

while running:
    
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False 
        elif event.type == pg.KEYDOWN:
            testMovePattern = players[testP].army[testTower].getMovePattern()

            #piece modification using keyboard
            if event.key == pg.K_KP_PLUS:
                players[testP].addPiece(testTower, "move")
                #tracer.addPiece("move")
                print(testMovePattern)

            if event.key == pg.K_KP_MINUS:
                players[testP].removePiece(testTower, "move")
                print(testMovePattern)
                #tracer.removePiece("m")
                print(testMovePattern)

            if event.key == pg.K_PERIOD:
                players[testP].addPiece(testTower, "turn")
                #tracer.addPiece("turn")
                print(testMovePattern)

            if event.key == pg.K_KP_MULTIPLY:
                players[testP].addPiece(testTower,"control")
                #tracer.addPiece("control")
                print(testMovePattern)
            
            if event.key == pg.K_KP_DIVIDE:
                players[testP].addPiece(testTower,"split")
                #tracer.addPiece("split")
                print(testMovePattern)
            
            #direction inputs using keyboard
            if event.key == pg.K_SLASH:
                #if len(directionInput) <= len(players[testP].army[testTower].getMovePattern()) :
                directionInput.append([1,0]) #east
                print(directionInput)
                # if tracer.testMove([[1,0]], testMovePattern[moveNum], grid=hexGrid):
                #     tracer.move([[1,0]], testMovePattern[moveNum], grid=hexGrid)
                # moveNum += 1
                # print(len(directionInput))
                # print(players[testP].army[testTower].getMovePattern())
                # print(len(players[testP].army[testTower].getMovePattern()))

            if event.key == pg.K_SEMICOLON:
                #if len(directionInput) <= len(players[testP].army[testTower].getMovePattern()):
                directionInput.append([0,1]) #northeast
                print(directionInput)
                #print(tracer.pos)
                #if tracer.testMove([[0,1]], testMovePattern[moveNum], grid=hexGrid):
                    #tracer.move([[0,1]], testMovePattern[moveNum], grid=hexGrid)
                    #print(tracer.pos)
                #moveNum += 1

            if event.key == pg.K_l:
                #if len(directionInput) <= len(players[testP].army[testTower].getMovePattern()):
                directionInput.append([-1,1]) #northwest
                print(directionInput)
                # if tracer.testMove([[-1,1]], testMovePattern[moveNum], grid=hexGrid):
                #     tracer.move([[-1,1]], testMovePattern[moveNum], grid=hexGrid)
                # moveNum += 1

            if event.key == pg.K_COMMA:
                #if len(directionInput) <= len(players[testP].army[testTower].getMovePattern()):
                directionInput.append([-1,0]) #west
                print(directionInput)
                # if tracer.testMove([[-1,0]], testMovePattern[moveNum], grid=hexGrid):
                #     tracer.move([[-1,0]], testMovePattern[moveNum], grid=hexGrid)
                # moveNum += 1

            if event.key == pg.K_RALT:
                #if len(directionInput) <= len(players[testP].army[testTower].getMovePattern()):    
                directionInput.append([0,-1]) #southwest
                print(directionInput)
                # if tracer.testMove([[0,-1]], testMovePattern[moveNum], grid=hexGrid):
                #     tracer.move([[0,-1]], testMovePattern[moveNum], grid=hexGrid)
                # moveNum += 1

            if event.key == pg.K_RCTRL:
                #if len(directionInput) <= len(players[testP].army[testTower].getMovePattern()):
                directionInput.append([1,-1]) #southeast    
                print(directionInput)
                # if tracer.testMove([[1,-1]], testMovePattern[moveNum], grid=hexGrid):
                #     tracer.move([[1,-1]], testMovePattern[moveNum], grid=hexGrid)
                # moveNum += 1

            #confirm movements
            if event.key == pg.K_z:
                if directionInput != []:
                    directionInput.pop(-1) #undo button
                    print(directionInput)

            if event.key == pg.K_RETURN: #moves player after confirmation
                moveNum = 0
                if len(directionInput) >= len(players[testP].army[testTower].getMovePattern()): #makes sure direction input is long enough
                    
                    print(hexGrid.arenaSize)
                    print(m.hypot(players[testP].army[testTower].pos[0], players[testP].army[testTower].pos[1]))
                          
                    if players[testP].testMoveTower(testTower, directionInput, Grid = hexGrid): #tests if move is out of bounds
                        players[testP].moveTower(testTower, directionInput, Grid = hexGrid)
                        print(players[testP].army[testTower].pos) 
                    else:
                        print("move would be out of bounds")
                    directionInput = [] #clear directionInput
                else:
                    print("please enter more directions")
        

        hexGrid.updateArena(players)

pg.quit()

#whole arena
# self.screen.fill((0, 0, 0))          
# self.screen.blit(hexGrid.surface, (0, 0)) #pastes the surface onto the window so we can draw on part (in this case all) of the window
# self.drawHexagonalArena(8, 20)

#just the hex



