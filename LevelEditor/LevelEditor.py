import pygame
import pygame.math
import Gui
import sys
pygame.init()


tiles = [] # array to store all the active tiles so we don't need to go through the entire grid to see which tiles need to be drawn
class Tile:
    selectedTile = None
    def onClick(self):
        if Tile.selectedTile == self:
            Tile.selectedTile = None
        else:
            Tile.selectedTile = self
    def __init__(self, texture, id):
        tiles.append(self)
        self.button = Gui.Button(pygame.Vector2(50 * len(tiles), 500), pygame.Vector2(50, 50), tile1Img, gui, self.onClick)
        self.texture = texture
        self.id = id
    def draw(self):
        pass

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
            texture = pygame.transform.scale(Tile.selectedTile.texture, size)
        screen.blit(texture, pos + pygame.Vector2(-self.pos.x, self.pos.y) + pygame.Vector2(self.size.x / 2, self.size.y / 2))

screen = pygame.display.set_mode([800, 600])
running = True

camera = Camera(pygame.Vector2(800, 600), screen)
gui = Gui.GUI(screen)
tile1Img = pygame.image.load('img/dirtBlock.jpg')
tile1Img = pygame.transform.scale(tile1Img, (50, 50))
tile1 = Tile(tile1Img, 0)
tilemap = [[-1] * 100] * 100
for i in range(0, len(tilemap)):
    for j in range(0, len(tilemap[i])):
        tilemap[i][j] = -1

clock = pygame.time.Clock()
deltaTime = 0 # time in seconds between each frame
gridSize = 30
gridRowCount = 101
gridColumnCount = 102
#-------------------- MAIN LOOP -------------------------
clock.tick(30)
while running:
    events = pygame.event.get()
    # Fill the background with grey
    screen.fill((200, 200, 200))
    camera.drawBoxOutline("green", pygame.Vector2(0, 0), pygame.Vector2(32, 32), 2)
    # get input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera.pos.y += 5 * deltaTime
    if keys[pygame.K_s]:
        camera.pos.y -= 5 * deltaTime
    if keys[pygame.K_d]:
        camera.pos.x += 5 * deltaTime
    if keys[pygame.K_a]:
        camera.pos.x -= 5 * deltaTime

    # draw a preview of the tile at the mouse poisition if it is selected
    if Tile.selectedTile != None:
        p = pygame.mouse.get_pos()
        mousePos = pygame.Vector2(p[0], p[1])
        mousePos = camera.getWorldMousePos(mousePos)
        mousePos = pygame.Vector2(round(mousePos.x / gridSize) * gridSize, round(mousePos.y / gridSize) * gridSize) - pygame.Vector2(gridSize / 2, gridSize / 2)
        #print("MOUSE POS: " + str(mousePos.x) + " " + str(mousePos.y))
        #print(str(tileZone.x) + " " + str(tileZone.y))
        camera.drawTexture(tile1Img, mousePos, pygame.Vector2(30, 30))

    # draw the grid
    width = gridColumnCount * gridSize
    height = gridRowCount * gridSize
    for i in range(0, gridColumnCount + 1):
        camera.drawLine("black", pygame.Vector2(i * gridSize, 0) - pygame.Vector2(gridSize / 2, gridSize / 2), pygame.Vector2(i * gridSize, height) - pygame.Vector2(gridSize / 2, gridSize / 2), 2)
    for i in range(0, gridRowCount + 1):
        camera.drawLine("black", pygame.Vector2(0, i * gridSize) - pygame.Vector2(gridSize / 2, gridSize / 2), pygame.Vector2(width, i * gridSize) - pygame.Vector2(gridSize / 2, gridSize / 2), 2)

    gui.drawElements()
    gui.checkInput(events)
    for i in tiles:
        i.draw()

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