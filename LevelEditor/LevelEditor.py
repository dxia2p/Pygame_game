import pygame
import pygame.math
import Gui
import sys
pygame.init()

class Tile: # class to store information about tile at position in grid
    tiles = []
    def __init__(self, position, tileType):
        self.position = position
        self.tileType = tileType
        self.tiles.append(self)
    def drawTile(self):
        self.tileType.camera.drawTexture(self.tileType.texture, (self.position * self.tileType.GRID_SIZE) - pygame.Vector2(self.tileType.GRID_SIZE / 2, self.tileType.GRID_SIZE / 2), pygame.Vector2(self.tileType.GRID_SIZE, self.tileType.GRID_SIZE))
    
    @staticmethod
    def drawAll():
        for t in Tile.tiles:
            t.drawTile()
class TileType: # this is for the gui of each different tile and stores the id for each one
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

screen = pygame.display.set_mode([800, 600])
running = True

# Grid constants
GRID_SIZE = 30
GRID_ROW_COUNT = 101
GRID_COLUMN_COUNT = 102

camera = Camera(pygame.Vector2(800, 600), screen)
gui = Gui.GUI(screen)
tile1Img = pygame.image.load('img/dirtBlock.jpg')
tile1Img = pygame.transform.scale(tile1Img, (50, 50))
tile1 = TileType(tile1Img, 0, camera, GRID_SIZE)
tilemap = [[-1] * 100] * 100
for i in range(0, len(tilemap)):
    for j in range(0, len(tilemap[i])):
        tilemap[i][j] = -1

clock = pygame.time.Clock()
deltaTime = 0 # time in seconds between each frame

def addTile(selectedTileGridPos):
    t = Tile(selectedTileGridPos, TileType.selectedTile)
    tilemap[int(selectedTileGridPos.x)][int(selectedTileGridPos.y)] = t

#-------------------- MAIN LOOP -------------------------
#sclock.tick(60)
while running:
    events = pygame.event.get()
    # Fill the background with grey
    screen.fill((200, 200, 200))
    camera.drawBoxOutline("green", pygame.Vector2(0, 0), pygame.Vector2(32, 32), 2)
    # get input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera.pos.y += 15 * deltaTime
    if keys[pygame.K_s]:
        camera.pos.y -= 15 * deltaTime
    if keys[pygame.K_d]:
        camera.pos.x += 15 * deltaTime
    if keys[pygame.K_a]:
        camera.pos.x -= 15 * deltaTime

    # draw a preview of the tile at the mouse poisition if it is selected
    if TileType.selectedTile != None:
        p = pygame.mouse.get_pos()
        mousePos = pygame.Vector2(p[0], p[1])
        mousePos = camera.getWorldMousePos(mousePos)
        mousePos = pygame.Vector2(round(mousePos.x / GRID_SIZE) * GRID_SIZE, round(mousePos.y / GRID_SIZE) * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2)
        selectedTileGridPos = pygame.Vector2(int((mousePos.x + GRID_SIZE / 2) / GRID_SIZE), int((mousePos.y + GRID_SIZE / 2) / GRID_SIZE))
        #print("MOUSE POS: " + str(mousePos.x) + " " + str(mousePos.y))
        #print(str(tileZone.x) + " " + str(tileZone.y))
        camera.drawTexture(tile1Img, mousePos, pygame.Vector2(30, 30))
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                addTile(selectedTileGridPos)


    # draw the grid
    width = GRID_COLUMN_COUNT * GRID_SIZE
    height = GRID_ROW_COUNT * GRID_SIZE
    for i in range(0, GRID_COLUMN_COUNT + 1):
        camera.drawLine("black", pygame.Vector2(i * GRID_SIZE, 0) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), pygame.Vector2(i * GRID_SIZE, height) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), 2)
    for i in range(0, GRID_ROW_COUNT + 1):
        camera.drawLine("black", pygame.Vector2(0, i * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), pygame.Vector2(width, i * GRID_SIZE) - pygame.Vector2(GRID_SIZE / 2, GRID_SIZE / 2), 2)

    gui.drawElements()
    gui.checkInput(events)
    Tile.drawAll()

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