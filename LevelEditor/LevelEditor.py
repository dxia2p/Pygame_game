import pygame
import pygame.math
import GuiLib as GuiLib
import sys
import os
import SaveSystem
from tkinter import filedialog
from PIL import Image

# Grid constants
GRID_SIZE = 30
GRID_ROW_COUNT = 51
GRID_COLUMN_COUNT = 51

class Tile: # class to store information about tile at position in grid
    tilemap = [[None] * GRID_COLUMN_COUNT for i in range(GRID_ROW_COUNT)]
    def __init__(self, position, tileType): # important to note that position refers to the position in the tilemap's grid (position >= 0, position has to be an integer)
        self.position = position
        self.tileType = tileType
        Tile.tilemap[int(position.x)][int(position.y)] = self
    def drawTile(self):
        Camera.drawTexture(self.tileType.texture, (self.position * self.tileType.GRID_SIZE) - pygame.Vector2(self.tileType.GRID_SIZE / 2, self.tileType.GRID_SIZE / 2), pygame.Vector2(self.tileType.GRID_SIZE, self.tileType.GRID_SIZE))

    @staticmethod
    def addTile(gridPosition, tileType):
        if gridPosition.x >= 0 and gridPosition.x < GRID_COLUMN_COUNT and gridPosition.y >= 0 and gridPosition.y < GRID_ROW_COUNT:
            return Tile(gridPosition, tileType)
        #else:
            #print(f"Tile position at {gridPosition.x}, {gridPosition.y} is out of bounds!")
    
    @staticmethod
    def removeTile(gridPosition):
        t = Tile.tilemap[int(gridPosition.x)][int(gridPosition.y)]
        if t == None:
            #print(f"Invalid tile, could not remove tile at {gridPosition.x}, {gridPosition.y}")
            return
        Tile.tilemap[int(gridPosition.x)][int(gridPosition.y)] = None
    
    @staticmethod
    def drawAllTiles(): 
        """This must be called every frame to draw all the tiles"""
        for i in range(len(Tile.tilemap)):
            for j in range(len(Tile.tilemap)):
                if Tile.tilemap[i][j] != None:
                    Tile.tilemap[i][j].drawTile()

class TileType: # this is for the "template" of each tile
    selectedTile = None
    tiles = []
    tilesDict = {}

    def onClick(self):
        """This function is meant to be used in a Button, do not call this function directly"""
        if TileType.selectedTile == self:
            TileType.selectedTile = None
        else:
            TileType.selectedTile = self

    def __init__(self, texture, id, GRID_SIZE, previewImg, texturePath):
        TileType.tiles.append(self)
        self.texture = texture
        self.button = GuiLib.Button(pygame.Vector2(60 * len(TileType.tiles), 720), pygame.Vector2(50, 50), self.texture, self.onClick)
        self.id = id
        self.GRID_SIZE = GRID_SIZE
        self.previewImg = previewImg
        self.texturePath = texturePath
        TileType.tilesDict[id] = self

    @staticmethod
    def addTileType(texturePath, GRID_SIZE):
        newTileImg = pygame.image.load(texturePath).convert_alpha()
        newTileImgPreview = pygame.Surface((newTileImg.get_width(), newTileImg.get_height()), pygame.SRCALPHA)
        newTileImgPreview.set_alpha(128)
        newTileImgPreview.blit(newTileImg, pygame.Vector2(0, 0))
        # Create the new tile
        TileType(newTileImg, len(TileType.tiles), GRID_SIZE, newTileImgPreview, texturePath)

    @staticmethod 
    def removeTileType():
        pass

class Camera:
    size = pygame.Vector2(0, 0)
    screen = None
    pos = pygame.Vector2(0, 0)
    
    @staticmethod
    def drawLine(color, start : pygame.Vector2, end : pygame.Vector2, width):
        """Draws a line based in world coordinates based on the start and end values given"""
        pygame.draw.line(screen, color, start + pygame.Vector2(-Camera.pos.x, Camera.pos.y) + pygame.Vector2(Camera.size.x / 2, Camera.size.y / 2), end + pygame.Vector2(-Camera.pos.x, Camera.pos.y) + pygame.Vector2(Camera.size.x / 2, Camera.size.y / 2), width)

    @staticmethod
    def drawBoxOutline(color, pos, size, lineWidth):
        """Draws the outline of a box in world coordinates based on the position, size and lineWidth given"""
        Camera.drawLine(color, pos + pygame.Vector2(-size.x / 2, size.y / 2), pos + pygame.Vector2(-size.x / 2, -size.y / 2), lineWidth)
        Camera.drawLine(color, pos + pygame.Vector2(-size.x / 2, -size.y / 2), pos + pygame.Vector2(size.x / 2, -size.y / 2), lineWidth)
        Camera.drawLine(color, pos + pygame.Vector2(size.x / 2, -size.y / 2), pos + pygame.Vector2(size.x / 2, size.y / 2), lineWidth)
        Camera.drawLine(color, pos + pygame.Vector2(size.x / 2, size.y / 2), pos + pygame.Vector2(-size.x / 2, size.y / 2), lineWidth)
    
    @staticmethod
    def getWorldMousePos(mousePos) -> pygame.Vector2:
        """Returns the position of the mouse in world coordinates"""
        mousePos += pygame.Vector2(Camera.pos.x, -Camera.pos.y)
        mousePos += pygame.Vector2(-Camera.size.x / 2, -Camera.size.y / 2)
        return mousePos
    
    @staticmethod
    def drawTexture(texture, pos, size = pygame.Vector2(-1, -1)):
        """Draws a texture in world coordinates, if the size is pygame.Vector2(-1, -1), the size of the original texture will be used"""
        if size != pygame.Vector2(-1, -1):
            texture = pygame.transform.scale(texture, size)
        Camera.screen.blit(texture, pos + pygame.Vector2(-Camera.pos.x, Camera.pos.y) + pygame.Vector2(Camera.size.x / 2, Camera.size.y / 2))

# initializing things
pygame.init()

screen = pygame.display.set_mode([1024, 768], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
pygame.display.set_caption("David's Tilemap Editor")
running = True

Camera.size = pygame.Vector2(1024, 768)
Camera.screen = screen

GuiLib.GUI.initialize(screen) # make gui class static???

# Making a panel for the tiles to be displayed on (this is for decoration)
tilePanel = GuiLib.Panel(pygame.Vector2(512, 720), pygame.Vector2(1024, 100), (230, 95, 85))

# ----------- loading tile 1 ----------
tile1Img = pygame.image.load("img/dirtBlock.jpg").convert_alpha()

tile1ImgPreview = pygame.Surface((tile1Img.get_width(), tile1Img.get_height()), pygame.SRCALPHA)
tile1ImgPreview.set_alpha(128)
tile1ImgPreview.blit(tile1Img, pygame.Vector2(0, 0))
tile1 = TileType(tile1Img, 0, GRID_SIZE, tile1ImgPreview, "img/dirtBlock.jpg")

clock = pygame.time.Clock()

deltaTime = 0 # time in seconds between each frame

#----------------------- Save Tiles Button ---------------------------
def saveButtonFunc():
    print("Saving tilemap...")
    SaveSystem.SaveTilemap(Tile.tilemap)

saveButtonImg = pygame.image.load("img/SaveButton.png")
saveButton = GuiLib.Button(pygame.Vector2(70, 60), pygame.Vector2(130, 75), saveButtonImg, saveButtonFunc)

#----------------------- Load Tiles Button -----------------------------
def loadButtonFunc():
    print("Loading tilemap...")
    tilemapData = SaveSystem.LoadTilemap()
    for tileData in tilemapData:
        Tile.addTile(pygame.Vector2(tileData["Position"][0], tileData["Position"][1]), TileType.tiles[tileData["id"]])
    print("Finished loading tilemap")

loadButtonImg = pygame.image.load("img/LoadButton.png")
loadButton = GuiLib.Button(pygame.Vector2(70, 160), pygame.Vector2(130, 75), loadButtonImg, loadButtonFunc)

# ---------------------------- Add Tile Button --------------------
def addTileFunc():
    filename = filedialog.askopenfilename(initialdir="/", title="select an image for new tile", filetypes=(("JPG File","*.jpg*"), ("PNG File","*.png*"),("all files", "*.*")))
    TileType.addTileType(filename, GRID_SIZE)

addTileButtonImg = pygame.image.load("img/PlusButton.png")
addTileButton = GuiLib.Button(pygame.Vector2(980, 720), pygame.Vector2(50, 50), addTileButtonImg, addTileFunc)

#-------------------- MAIN LOOP -------------------------
mouseLeftButtonHeld = False # a bool to store if the mouse button is held down
mouseRightButtonHeld = False
while running:
    deltaTime = clock.tick() / 1000

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseLeftButtonHeld = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouseLeftButtonHeld = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouseRightButtonHeld = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            mouseRightButtonHeld = False

    # Fill the background with grey
    screen.fill((255, 255, 255))

    # get input
    keys = pygame.key.get_pressed()
    cameraSpeed = 0
    fastCameraSpeed = 800
    normalCameraSpeed = 400
    if keys[pygame.K_LSHIFT]:
        cameraSpeed = fastCameraSpeed
    else:
        cameraSpeed = normalCameraSpeed

    if keys[pygame.K_w]:
        Camera.pos.y += cameraSpeed * deltaTime
    if keys[pygame.K_s]:
        Camera.pos.y -= cameraSpeed * deltaTime
    if keys[pygame.K_d]:
        Camera.pos.x += cameraSpeed * deltaTime
    if keys[pygame.K_a]:
        Camera.pos.x -= cameraSpeed * deltaTime

    # Mouse input
    screenMousePos = pygame.mouse.get_pos()
    screenMousePos = pygame.Vector2(screenMousePos[0], screenMousePos[1]) # must convert to a vector2
    positionIsOnGUI = GuiLib.GUI.positionIsOnGUI(screenMousePos)

    mousePos = Camera.getWorldMousePos(screenMousePos)
    mousePos = pygame.Vector2(round(mousePos.x / GRID_SIZE) * GRID_SIZE, round(mousePos.y / GRID_SIZE) * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2)
    selectedTileGridPos = pygame.Vector2(int((mousePos.x + GRID_SIZE / 2) / GRID_SIZE), int((mousePos.y + GRID_SIZE / 2) / GRID_SIZE))
    # draw a preview of the tile at the mouse poisition if it is selected
    if TileType.selectedTile != None and (not positionIsOnGUI):
        Camera.drawTexture(TileType.selectedTile.previewImg, mousePos, pygame.Vector2(30, 30))
        if mouseLeftButtonHeld:
            Tile.addTile(selectedTileGridPos, TileType.selectedTile)

    if not positionIsOnGUI and mouseRightButtonHeld:
        # Removing tiles
        Tile.removeTile(selectedTileGridPos)

    # ------------------------- draw the grid ----------------------
    width = GRID_COLUMN_COUNT * GRID_SIZE
    height = GRID_ROW_COUNT * GRID_SIZE
    gridColor = "#b8c7de"
    for i in range(0, GRID_COLUMN_COUNT + 1): # draw thicker lines every 3 tiles
        if(i % 3 == 0):
            Camera.drawLine(gridColor, pygame.Vector2(i * GRID_SIZE, 0) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), pygame.Vector2(i * GRID_SIZE, height) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), 2)
        else:
            Camera.drawLine(gridColor, pygame.Vector2(i * GRID_SIZE, 0) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), pygame.Vector2(i * GRID_SIZE, height) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), 1)
    for i in range(0, GRID_ROW_COUNT + 1):
        if(i % 3 == 0):
            Camera.drawLine(gridColor, pygame.Vector2(0, i * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), pygame.Vector2(width, i * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), 2)
        else:
            Camera.drawLine(gridColor, pygame.Vector2(0, i * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), pygame.Vector2(width, i * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), 1)


    Tile.drawAllTiles()
    # GUI functions
    GuiLib.GUI.drawElements()
    GuiLib.GUI.checkInput(events)
    # Did the user click the window close button?
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Flip the display
    pygame.display.flip()
# Done! Time to quit.
pygame.quit()
sys.exit()