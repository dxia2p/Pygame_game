import pygame
import pygame.math
pygame.init()


class Camera:
    def __init__(self, screenSize : pygame.Vector2) -> None:
        self.pos = pygame.Vector2(0, 0)
        self.size = screenSize
    
    def drawLine(self, color, start : pygame.Vector2, end : pygame.Vector2, width):
        pygame.draw.line(screen, color, start + self.pos + pygame.Vector2(self.size.x / 2, self.size.y / 2), end + self.pos + pygame.Vector2(self.size.x / 2, self.size.y / 2), width)

screen = pygame.display.set_mode([800, 600])
running = True

camera = Camera(pygame.Vector2(800, 600))
clock = pygame.time.Clock()
deltaTime = 0 # time in seconds between each frame
gridSize = 60
gridRowCount = 10
gridColumnCount = 10
#-------------------- MAIN LOOP -------------------------
clock.tick(30)
while running:
    #print(deltaTime)
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    camera.drawLine("green", pygame.Vector2(100, 100), pygame.Vector2(750, 750), 5)
    
    # get input
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                camera.pos.y += 1 * deltaTime
            if event.key == pygame.K_s:
                lcamera.pos.y -= 1 * deltaTime

    # draw the grid
    width = gridColumnCount * gridSize
    height = gridRowCount * gridSize
    for i in range(int(-width / 2), int(width / 2) + 1, gridSize):
        camera.drawLine("black", pygame.Vector2(i, -height / 2), pygame.Vector2(i, height / 2), 2)
    for i in range(int(-height / 2), int(height / 2) + 1, gridSize):
        camera.drawLine("black", pygame.Vector2(-width / 2,i), pygame.Vector2(width / 2,i), 2)

    # Flip the display
    pygame.display.flip()
    deltaTime = clock.get_time() / 1000
    #print(deltaTime)
# Done! Time to quit.
pygame.quit()