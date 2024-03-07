import pygame
import pygame.math
pygame.init()


class Camera:
    def __init__(self, screenSize : pygame.Vector2) -> None:
        self.pos = pygame.Vector2(0, 0)
        self.size = screenSize
    
    def drawLine(self, color, start : pygame.Vector2, end : pygame.Vector2, width):
        pygame.draw.line(screen, color, start + self.pos, end + self.pos, width)

screen = pygame.display.set_mode([800, 600])
running = True

camera = Camera(pygame.Vector2(800, 600))
clock = pygame.time.Clock()
deltaTime = 0 # time in seconds between each frame
clock.tick(30)
#-------------------- MAIN LOOP -------------------------
while running:
    #print(deltaTime)
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    camera.drawLine("green", pygame.Vector2(100, 100), pygame.Vector2(750, 750), 5)
    camera.pos.x += 1 * deltaTime
    # Flip the display
    pygame.display.flip()
    deltaTime = clock.get_time() / 1000
    print(deltaTime)
# Done! Time to quit.
pygame.quit()