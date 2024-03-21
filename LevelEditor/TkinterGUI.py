import os
import tkinter as tk
from tkinter import *
import pygame
import sys

root = tk.Tk()
embed = tk.Frame(root, width = 500, height = 500)
embed.grid(columnspan = (600), rowspan = (500))
embed.pack(side = LEFT)
buttonwin = tk.Frame(root, width = 75, height = 500)
buttonwin.pack(side = LEFT)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
screen = pygame.display.set_mode((500, 500))
screen.fill(pygame.Color(255, 255, 255))
pygame.display.init()
pygame.display.update()
clock = pygame.time.Clock()
clock.tick(60)
running = True

drawCircle = False
def yes():
    drawCircle=True


def draw():
    pygame.draw.circle(screen, (0, 0, 0), (250, 250), 125)
    pygame.display.update()

def on_destroy(event):
    if event.widget != root:
        return
    while True:
        print("just closed")
        sys.exit()
    running = False
    print(running)


root.bind("<Destroy>", on_destroy)

button1 = Button(buttonwin, text='Draw', command=yes)
button1.pack(side = LEFT)


while running:
    print(running)
    if drawCircle:
        draw()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    root.update()

print("ASDASDSADASDSASD")
pygame.quit()
