from gameArena import gameArena
from player import player #(from fileName, import className): the class has the same name as the file and I don't want to type tower.tower or player.player 
from tower import tower
import math as m
import pygame as pg

players = []
hexGrid = gameArena()

players.append(player("Player 1"))
#players.append(player("Player 2"))

playerDirs = []
playerDist = []

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

while running:
    
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False 
        elif event.type == pg.KEYDOWN:

            #piece modification using keyboard
            if event.key == pg.K_KP_PLUS:
                players[testP].addPiece(testTower, "move")
                print(players[testP].army[testTower].getMovePattern())

            if event.key == pg.K_KP_MINUS:
                players[testP].removePiece(testTower, "move")
                print(players[testP].army[testTower].getMovePattern())

            if event.key == pg.K_PERIOD:
                players[testP].addPiece(testTower, "turn")
                print(players[testP].army[testTower].getMovePattern())
            
            if event.key == pg.K_KP_MULTIPLY:
                players[testP].addPiece(testTower,"control")
                print(players[testP].army[testTower].getMovePattern())
            
            if event.key == pg.K_KP_DIVIDE:
                players[testP].addPiece(testTower,"split")
                print(players[testP].army[testTower].getMovePattern())

            #direction inputs using keyboard
            if event.key == pg.K_SLASH:
                players[testP].moveTower(testTower, [gameArena.hexD["e"]], Grid = hexGrid )
                print(players[testP].army[testTower].pos)

            if event.key == pg.K_COMMA:
                players[testP].moveTower(testTower, [gameArena.hexD["w"]], Grid = hexGrid )
                print(players[testP].army[testTower].pos)

            if event.key == pg.K_RCTRL:
                players[testP].moveTower(testTower, [gameArena.hexD["se"]], Grid = hexGrid )
                print(players[testP].army[testTower].pos)

            if event.key == pg.K_RALT:
                players[testP].moveTower(testTower, [gameArena.hexD["sw"]], Grid = hexGrid )
                print(players[testP].army[testTower].pos)

            if event.key == pg.K_SEMICOLON:
                players[testP].moveTower(testTower, [gameArena.hexD["ne"]], Grid = hexGrid )
                print(players[testP].army[testTower].pos)

            if event.key == pg.K_l:
                players[testP].moveTower(testTower, [gameArena.hexD["nw"]], Grid = hexGrid )
                print(players[testP].army[testTower].pos)
        
        hexGrid.updateArena(players)
        # hexGrid.screen.fill((0, 0, 0))          
        # hexGrid.screen.blit(hexGrid.surface, (0, 0)) #pastes the surface onto the window so we can draw on part (in this case all) of the window
        # hexGrid.drawHexagonalArena(8, 20)
        # for p in players:
        #     for tower in range(0,len(p.army)):
        #         hexGrid.drawAtHexCoordinate(p.army[tower].pos, 20, [600,300], 2)
        #         pg.display.flip() #update drawing
        #         #print(p.army[tower].pos)

    


pg.quit()

#whole arena
# self.screen.fill((0, 0, 0))          
# self.screen.blit(hexGrid.surface, (0, 0)) #pastes the surface onto the window so we can draw on part (in this case all) of the window
# self.drawHexagonalArena(8, 20)

#just the hex



