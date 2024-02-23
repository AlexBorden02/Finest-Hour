
import pygame

class Camera:
    def __init__(self, init_pos=(0, 0), zoom=1, min_zoom=1, max_zoom=10, border=None):
        self.offset = pygame.Vector2(-init_pos[0], -init_pos[1])
        self.zoom = zoom
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.border = border if border else pygame.Rect(-float('inf')/2, -float('inf')/2, float('inf'), float('inf'))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Mouse wheel up
                self.zoom_in(event.pos)
            elif event.button == 5:  # Mouse wheel down
                self.zoom_out(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left mouse button
                new_offset = self.offset + event.rel
                new_pos = pygame.Vector2(-new_offset.x/self.zoom, -new_offset.y/self.zoom)
                if not self.border.collidepoint(new_pos):
                    new_pos.x = min(max(new_pos.x, self.border.left), self.border.right)
                    new_pos.y = min(max(new_pos.y, self.border.top), self.border.bottom)
                    new_offset = pygame.Vector2(-new_pos.x*self.zoom, -new_pos.y*self.zoom)
                self.offset = new_offset

    def zoom_in(self, mouse_pos):
        new_zoom = self.zoom * 1.1
        if new_zoom <= self.max_zoom:
            new_offset = self.offset - (mouse_pos - self.offset) * (0.1)
            new_pos = pygame.Vector2(-new_offset.x/new_zoom, -new_offset.y/new_zoom)
            if not self.border.collidepoint(new_pos):
                new_pos.x = min(max(new_pos.x, self.border.left), self.border.right)
                new_pos.y = min(max(new_pos.y, self.border.top), self.border.bottom)
                new_offset = pygame.Vector2(-new_pos.x*new_zoom, -new_pos.y*new_zoom)
            self.zoom = new_zoom
            self.offset = new_offset

    def zoom_out(self, mouse_pos):
        new_zoom = self.zoom / 1.1
        if new_zoom >= self.min_zoom:
            new_offset = self.offset + (mouse_pos - self.offset) * (1 - 1/1.1)
            new_pos = pygame.Vector2(-new_offset.x/new_zoom, -new_offset.y/new_zoom)
            if not self.border.collidepoint(new_pos):
                new_pos.x = min(max(new_pos.x, self.border.left), self.border.right)
                new_pos.y = min(max(new_pos.y, self.border.top), self.border.bottom)
                new_offset = pygame.Vector2(-new_pos.x*new_zoom, -new_pos.y*new_zoom)
            self.zoom = new_zoom
            self.offset = new_offset

    def move(self, dx, dy):
        new_offset = self.offset + pygame.Vector2(dx, dy)
        new_pos = pygame.Vector2(-new_offset.x/self.zoom, -new_offset.y/self.zoom)
        if not self.border.collidepoint(new_pos):
            new_pos.x = min(max(new_pos.x, self.border.left), self.border.right)
            new_pos.y = min(max(new_pos.y, self.border.top), self.border.bottom)
            new_offset = pygame.Vector2(-new_pos.x*self.zoom, -new_pos.y*self.zoom)
        self.offset = new_offset

    def apply(self, pos):
        return tuple(map(int, (self.zoom * pos[0] + self.offset.x, self.zoom * pos[1] + self.offset.y)))
    
    def unapply(self, pos):
        return ((pos[0] - self.offset.x) / self.zoom, (pos[1] - self.offset.y) / self.zoom)