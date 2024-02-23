
import pygame

class Cell:
    def __init__(self, x, y, size, selected=False):
        self.rect = pygame.Rect(x, y, size, size)
        self.selected = selected 
        self.id = (x/10, y/10)