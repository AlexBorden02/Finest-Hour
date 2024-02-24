
import pygame

class Button:
    def __init__(self, text, x, y, width, height, color, callback=None, callback_args=(), image=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.callback = callback  # Function to call when the button is clicked
        self.callback_args = callback_args
        self.image = image

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.image!=None:
            screen.blit(self.image, (self.x, self.y))
        else:
            font = pygame.font.Font(None, 36)
            text = font.render(self.text, True, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            print(self.rect)
            if self.rect.collidepoint(event.pos):
                print("Button clicked")
                if self.callback:
                    self.callback(self.callback_args)
                return True
            