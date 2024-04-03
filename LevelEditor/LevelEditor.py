import pygame
import pygame.math
import Gui
import sys
import os
import SaveSystem

# Grid constants
GRID_SIZE = 30
GRID_ROW_COUNT = 102
GRID_COLUMN_COUNT = 102

class Tile: # class to store information about tile at position in grid
    tilemap = [[None] * GRID_COLUMN_COUNT for i in range(GRID_ROW_COUNT)]
    def __init__(self, position, tileType): # important to note that position refers to the position in the tilemap's grid (position >= 0, position has to be an integer)
        self.position = position
        self.tileType = tileType
        Tile.tilemap[int(selectedTileGridPos.x)][int(selectedTileGridPos.y)] = self
    def drawTile(self):
        self.tileType.camera.drawTexture(self.tileType.texture, (self.position * self.tileType.GRID_SIZE) - pygame.Vector2(self.tileType.GRID_SIZE / 2, self.tileType.GRID_SIZE / 2), pygame.Vector2(self.tileType.GRID_SIZE, self.tileType.GRID_SIZE))

    @staticmethod
    def addTile(gridPosition, tileType):
        if gridPosition.x >= 0 and gridPosition.x < GRID_COLUMN_COUNT and gridPosition.y >= 0 and gridPosition.y < GRID_ROW_COUNT:
            Tile(gridPosition, tileType)
        else:
            print(f"Tile position at {gridPosition.x}, {gridPosition.y} is out of bounds!")
    
    @staticmethod
    def removeTile(gridPosition):
        t = Tile.tilemap[int(gridPosition.x)][int(gridPosition.y)]
        if t == None:
            print(f"Invalid tile, could not remove tile at {gridPosition.x}, {gridPosition.y}")
            return
        Tile.tilemap[int(gridPosition.x)][int(gridPosition.y)] = None
    
    @staticmethod
    def drawAllTiles(): # call this every frame to draw all the tiles
        for i in range(len(Tile.tilemap)):
            for j in range(len(Tile.tilemap)):
                if Tile.tilemap[i][j] != None:
                    Tile.tilemap[i][j].drawTile()

class TileType: # this is for the "template" of each tile
    selectedTile = None
    tiles = []

    def onClick(self):
        if TileType.selectedTile == self:
            TileType.selectedTile = None
        else:
            TileType.selectedTile = self
    def __init__(self, texture, id, camera, GRID_SIZE):
        TileType.tiles.append(self)
        self.texture = texture
        self.button = Gui.Button(pygame.Vector2(50 * len(TileType.tiles), 500), pygame.Vector2(50, 50), self.texture, gui, self.onClick)
        self.id = id
        self.camera = camera
        self.GRID_SIZE = GRID_SIZE

class Camera:
    def __init__(self, screenSize : pygame.Vector2, screen) -> None:
        self.pos = pygame.Vector2(0, 0)
        self.size = screenSize
        self.screen = screen
    
    def drawLine(self, color, start : pygame.Vector2, end : pygame.Vector2, width):
        pygame.draw.line(screen, color, start + pygame.Vector2(-self.pos.x, self.pos.y) + pygame.Vector2(self.size.x / 2, self.size.y / 2), end + pygame.Vector2(-self.pos.x, self.pos.y) + pygame.Vector2(self.size.x / 2, self.size.y / 2), width)

    def drawBoxOutline(self, color, pos, size, lineWidth):
        self.drawLine(color, pos + pygame.Vector2(-size.x / 2, size.y / 2), pos + pygame.Vector2(-size.x / 2, -size.y / 2), lineWidth)
        self.drawLine(color, pos + pygame.Vector2(-size.x / 2, -size.y / 2), pos + pygame.Vector2(size.x / 2, -size.y / 2), lineWidth)
        self.drawLine(color, pos + pygame.Vector2(size.x / 2, -size.y / 2), pos + pygame.Vector2(size.x / 2, size.y / 2), lineWidth)
        self.drawLine(color, pos + pygame.Vector2(size.x / 2, size.y / 2), pos + pygame.Vector2(-size.x / 2, size.y / 2), lineWidth)
    def getWorldMousePos(self, mousePos) -> pygame.Vector2:
        mousePos += pygame.Vector2(self.pos.x, -self.pos.y)
        mousePos += pygame.Vector2(-self.size.x / 2, -self.size.y / 2)
        return mousePos
    def drawTexture(self, texture, pos, size = pygame.Vector2(-1, -1)):
        if size != pygame.Vector2(-1, -1):
            texture = pygame.transform.scale(texture, size)
        screen.blit(texture, pos + pygame.Vector2(-self.pos.x, self.pos.y) + pygame.Vector2(self.size.x / 2, self.size.y / 2))

# initializing things
pygame.init()

screen = pygame.display.set_mode([1024, 768])
running = True

camera = Camera(pygame.Vector2(1024, 768), screen)
gui = Gui.GUI(screen)

# ----------- loading tile 1 ----------
tile1Img = pygame.image.load('img/dirtBlock.jpg')
tile1Img = pygame.transform.scale(tile1Img, (50, 50))
tile1 = TileType(tile1Img, 0, camera, GRID_SIZE)
tile1ImgPreview = pygame.Surface((tile1Img.get_width(), tile1Img.get_height()), pygame.SRCALPHA)
tile1ImgPreview.set_alpha(128)
tile1ImgPreview.blit(tile1Img, pygame.Vector2(0, 0))



clock = pygame.time.Clock()
deltaTime = 0 # time in seconds between each frame

#----------------------- Save Button ---------------------------
#saveButton = Gui.Button()

#-------------------- MAIN LOOP -------------------------
mouseLeftButtonHeld = False # a bool to store if the mouse button is held down
clock.tick(60)
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseLeftButtonHeld = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouseLeftButtonHeld = False
    # Fill the background with grey
    screen.fill((200, 200, 200))
    screen.fill((255, 255, 255))

    # get input
    keys = pygame.key.get_pressed()
    cameraSpeed = 0
    fastCameraSpeed = 80
    normalCameraSpeed = 30
    if keys[pygame.K_LSHIFT]:
        cameraSpeed = fastCameraSpeed
    else:
        cameraSpeed = normalCameraSpeed

    if keys[pygame.K_w]:
        camera.pos.y += cameraSpeed * deltaTime
    if keys[pygame.K_s]:
        camera.pos.y -= cameraSpeed * deltaTime
    if keys[pygame.K_d]:
        camera.pos.x += cameraSpeed * deltaTime
    if keys[pygame.K_a]:
        camera.pos.x -= cameraSpeed * deltaTime

    # draw a preview of the tile at the mouse poisition if it is selected
    if TileType.selectedTile != None:
        p = pygame.mouse.get_pos()
        mousePos = pygame.Vector2(p[0], p[1])
        mousePos = camera.getWorldMousePos(mousePos)
        mousePos = pygame.Vector2(round(mousePos.x / GRID_SIZE) * GRID_SIZE, round(mousePos.y / GRID_SIZE) * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2)
        selectedTileGridPos = pygame.Vector2(int((mousePos.x + GRID_SIZE / 2) / GRID_SIZE), int((mousePos.y + GRID_SIZE / 2) / GRID_SIZE))
        #print("MOUSE POS: " + str(mousePos.x) + " " + str(mousePos.y))
        #print(str(tileZone.x) + " " + str(tileZone.y))
        camera.drawTexture(tile1ImgPreview, mousePos, pygame.Vector2(30, 30))
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Tile.addTile(selectedTileGridPos, TileType.selectedTile)
                elif event.button == 3:
                    Tile.removeTile(selectedTileGridPos)
            elif mouseLeftButtonHeld:
                Tile.addTile(selectedTileGridPos, TileType.selectedTile)

    # draw the grid ----------------------
    width = GRID_COLUMN_COUNT * GRID_SIZE
    height = GRID_ROW_COUNT * GRID_SIZE
    gridColor = "#b8c7de"
    for i in range(0, GRID_COLUMN_COUNT + 1): # draw thicker lines every 3 tiles
        if(i % 3 == 0):
            camera.drawLine(gridColor, pygame.Vector2(i * GRID_SIZE, 0) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), pygame.Vector2(i * GRID_SIZE, height) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), 2)
        else:
            camera.drawLine(gridColor, pygame.Vector2(i * GRID_SIZE, 0) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), pygame.Vector2(i * GRID_SIZE, height) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), 1)
    for i in range(0, GRID_ROW_COUNT + 1):
        if(i % 3 == 0):
            camera.drawLine(gridColor, pygame.Vector2(0, i * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), pygame.Vector2(width, i * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), 2)
        else:
            camera.drawLine(gridColor, pygame.Vector2(0, i * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), pygame.Vector2(width, i * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), 1)
    # GUI functions
    gui.drawElements()
    gui.checkInput(events)
    Tile.drawAllTiles()
    # Did the user click the window close button?
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Flip the display
    pygame.display.flip()
    deltaTime = clock.get_time() / 1000
 
# Done! Time to quit.
pygame.quit()
sys.exit()