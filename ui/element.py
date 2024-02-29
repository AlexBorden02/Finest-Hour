
import pygame

class Element:
    def __init__(self, x, y, width, height, color, image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)  # Adjust the rectangle's coordinates
        self.color = color
        self.image = image
        self.buttons = []
        self.surface = pygame.Surface((width, height))  # Create a surface for the element
        self.needs_redraw = True  # Flag to indicate whether the element needs to be redrawn

    def render(self, screen):
        if self.needs_redraw:
            # If the element needs to be redrawn, clear the surface and redraw the element and its buttons
            self.surface.fill((0, 0, 0, 0))
            pygame.draw.rect(self.surface, self.color, self.rect)
            for button in self.buttons:
                button.render(self.surface)  # Make sure the button's render method uses the correct coordinates
            self.needs_redraw = False
        # Blit the element's surface onto the screen
        screen.blit(self.surface, (self.x, self.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                for button in self.buttons:
                    button.handle_event(event)
                return True
            
    def add_button(self, button):
        self.buttons.append(button)
        self.needs_redraw = True  # The element needs to be redrawn when a button is added
        return self.buttons
            