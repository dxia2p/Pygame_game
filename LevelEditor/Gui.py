import pygame

class GUIBase:
    def __init__(self, surface) -> None:
        self.surface = surface
        pass

    def draw(self):
        pass
    
    def checkInput(self, event):
        pass

class GUI:
    def __init__(self, surface : pygame.surface) -> None:
        self.elements = []
        self.surface = surface
    
    def drawElements(self):
        for element in self.elements:
            element.draw()
    
    def checkInput(self):
        ev = pygame.event.get()
        for element in self.elements:
            element.checkInput(ev)

    def addElement(self, element : GUIBase):
        self.elements.append(element)


class Button (GUIBase):
    def __init__(self, pos : pygame.Vector2, size : pygame.Vector2, texture, gui : GUI, func) -> None:
        GUIBase.__init__(self, gui.surface)
        self.size = size
        self.texture = texture
        self.pos = pos
        self.func = func
        gui.addElement(self)
    
    def draw(self):
        if self.texture == None:
            pygame.draw.rect(self.surface, "pink", pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y))
        else:
            self.surface.blit(self.texture, self.pos - (self.size / 2))

    def checkInput(self, event):
        p = pygame.mouse.get_pos()
        clickPos = pygame.Vector2(p[0], p[1])
        #print(str(clickPos.x) + " " + str(clickPos.y))
        for ev in event:
            if ev.type == pygame.MOUSEBUTTONUP:  
                left = self.pos.x - self.size.x / 2
                right = self.pos.x + self.size.x / 2
                top = self.pos.y - self.size.y / 2
                bottom = self.pos.y + self.size.y / 2
                if clickPos.x > left and clickPos.x < right and clickPos.y < bottom and clickPos.y > top:
                    self.func()