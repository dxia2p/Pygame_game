import pygame
import sys

class GUIBase:
    def __init__(self) -> None:
        GUI.addElement(self)
        pass

    def draw(self):
        pass
    
    def checkInput(self, event):
        pass

class GUI:
    elements = []
    surface = None

    @staticmethod
    def initialize(surface):
        GUI.surface = surface
    
    @staticmethod
    def drawElements():
        for element in GUI.elements:
            element.draw()
    
    @staticmethod
    def checkInput(events):
        for element in GUI.elements:
            element.checkInput(events)

    @staticmethod
    def addElement(element : GUIBase):
        GUI.elements.append(element)

class Button (GUIBase):
    def __init__(self, pos : pygame.Vector2, size : pygame.Vector2, texture, func) -> None:
        GUIBase.__init__(self)
        self.size = size
        self.pos = pos
        self.func = func
        self.texture = texture
        if texture != None:
            self.texture = pygame.transform.scale(texture, self.size)
    
    def draw(self): # draw function which overrides GUIBase's draw function
        if self.texture == None: # Draw a pink rectangle in case of missing texture
            rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
            rect.center = self.pos
            pygame.draw.rect(self.surface, "pink", rect)
        else: # Draw the texture normally
            GUI.surface.blit(self.texture, self.pos - (self.size / 2))

    def checkInput(self, event):
        p = pygame.mouse.get_pos()
        clickPos = pygame.Vector2(p[0], p[1])
        
        for ev in event:
            if ev.type == pygame.MOUSEBUTTONUP: # Check if mouse input is within the rect of the button
                left = self.pos.x - self.size.x / 2
                right = self.pos.x + self.size.x / 2
                top = self.pos.y - self.size.y / 2
                bottom = self.pos.y + self.size.y / 2
                if clickPos.x > left and clickPos.x < right and clickPos.y < bottom and clickPos.y > top:
                    self.func()

class Text (GUIBase):
    def __init__(self, pos, fontSize, fontPath):
        GUIBase.__init__(self)
        self.pos = pos
        self.font = pygame.font.Font(fontPath, fontSize)
        self.text = ""
        self.textColor = (0, 0, 0)
        self.backgroundColor = (255, 255, 255)
        self.textRender = self.font.render(self.text, True, self.textColor, self.backgroundColor) # text render is the pygame object for text, while text is a string of text
        self.textRect = self.textRender.get_rect()
        self.textRect.center = pos
    
    def changeTextColor(self, newTextColor):
        self.textColor = newTextColor
        self.textRender = self.font.render(self.text, True, self.textColor, self.backgroundColor)

    def changeBackgroundColor(self, newBackgroundColor):
        self.backgroundColor = newBackgroundColor
        self.textRender = self.font.render(self.text, True, self.textColor, self.backgroundColor)

    def changeText(self, newText):
        self.text = newText
        self.textRender = self.font.render(self.text, True, self.textColor, self.backgroundColor)
    
    def draw(self):
        GUI.surface.blit(self.textRender, self.textRect)

class Panel (GUIBase):
    def __init__(self, pos):
        pass