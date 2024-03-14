import pygame
import pygame.math
import Gui
pygame.init()

tiles = []

class Tile: # fix this
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

class Camera:
    def __init__(self, screenSize : pygame.Vector2) -> None:
        self.pos = pygame.Vector2(0, 0)
        self.size = screenSize
    
    def drawLine(self, color, start : pygame.Vector2, end : pygame.Vector2, width):
        pygame.draw.line(screen, color, start + pygame.Vector2(-self.pos.x, self.pos.y) + pygame.Vector2(self.size.x / 2, self.size.y / 2), end + pygame.Vector2(-self.pos.x, self.pos.y) + pygame.Vector2(self.size.x / 2, self.size.y / 2), width)

screen = pygame.display.set_mode([800, 600])
running = True

camera = Camera(pygame.Vector2(800, 600))
gui = Gui.GUI(screen)
tile1Img = pygame.image.load('img/dirtBlock.jpg')
tile1Img = pygame.transform.scale(tile1Img, (50, 50))
tile1 = Tile(tile1Img, 0)
tilemap = [100][100]
for i in range(0, len(tilemap)):
    for j in range(0, len(tilemap[i])):
        tilemap[i][j] = -1

clock = pygame.time.Clock()
deltaTime = 0 # time in seconds between each frame
gridSize = 30
gridRowCount = 30
gridColumnCount = 30
#-------------------- MAIN LOOP -------------------------
clock.tick(30)
while running:
    #print(deltaTime)
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with grey
    screen.fill((200, 200, 200))
    
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
        tileZone = None
        mousePos = pygame.Vector2(p[0], p[1])
        texture = pygame.transform.scale(Tile.selectedTile.texture, (30, 30))
        screen.blit(texture, mousePos - (pygame.Vector2(gridSize) / 2))

    # draw the grid
    width = gridColumnCount * gridSize
    height = gridRowCount * gridSize
    for i in range(int(-width / 2), int(width / 2) + 1, gridSize):
        camera.drawLine("black", pygame.Vector2(i, -height / 2), pygame.Vector2(i, height / 2), 2)
    for i in range(int(-height / 2), int(height / 2) + 1, gridSize):
        camera.drawLine("black", pygame.Vector2(-width / 2,i), pygame.Vector2(width / 2,i), 2)

    gui.drawElements()
    gui.checkInput()
    # Flip the display
    pygame.display.flip()
    deltaTime = clock.get_time() / 1000
# Done! Time to quit.
pygame.quit()
