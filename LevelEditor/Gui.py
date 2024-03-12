import pygame

class GUIBase:
    def __init__(self, surface) -> None:
        self.surface = surface
        pass

    def draw(self):
        pass


class GUI:
    def __init__(self, surface : pygame.surface) -> None:
        self.elements = []
        self.surface = surface
    
    def drawElements(self):
        for element in self.elements:
            element.draw()
    
    def addElement(self, element : GUIBase):
        self.elements.append(element)


class Button (GUIBase):
    def __init__(self, pos : pygame.Vector2, size : pygame.Vector2, texture, gui : GUI) -> None:
        GUIBase.__init__(self, gui.surface)
        self.size = size
        self.texture = texture
        self.pos = pos
        gui.addElement(self)
    
    def draw(self):
        if self.texture == None:
            pygame.draw.rect(self.surface, "pink", pygame.Rect(self.pos.x - self.size.x / 2, self.pos.y - self.size.y / 2, self.pos.x + self.size.x / 2, self.pos.y + self.size.y / 2))
