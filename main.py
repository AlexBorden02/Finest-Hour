import pygame
import sys
import math

# Initialize Pygame
pygame.init()
map_italy = pygame.image.load('map_italy.svg')

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Basic setup for menu and game states
game_state = 'menu'

class Button:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (0, 0, 0))
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_clicked(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

def start_menu():
    global game_state
    buttons = [
        Button('New Game', 100, 100, 200, 50, BLUE),
        Button('Load Game', 100, 200, 200, 50, BLUE),
        Button('Settings', 100, 300, 200, 50, BLUE),
        Button('Quit', 100, 400, 200, 50, BLUE)
    ]
    for button in buttons:
        button.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.is_clicked(pos):
                    if button.text == 'New Game':
                        game_state = 'game'
                    elif button.text == 'Quit':
                        pygame.quit()
                        sys.exit()

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

    def apply(self, pos):
        return tuple(map(int, (self.zoom * pos[0] + self.offset.x, self.zoom * pos[1] + self.offset.y)))
    
    def unapply(self, pos):
        return ((pos[0] - self.offset.x) / self.zoom, (pos[1] - self.offset.y) / self.zoom)

camera = Camera(init_pos=(800, 1400), zoom=3, border=pygame.Rect(-1600, -900, 3200, 1800))

class Cell:
    def __init__(self, x, y, size, selected=False):
        self.rect = pygame.Rect(x, y, size, size)
        self.selected = selected 
        self.id = (x/10, y/10)

class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cells = [Cell(x, y, cell_size) for x in range(0, width, cell_size) for y in range(0, height, cell_size)]

    def get_cell(self, pos, camera):
        transformed_pos = camera.unapply(pos)
        for cell in self.cells:
            if cell.rect.collidepoint(transformed_pos):
                return cell
        return None

    def get_cell_by_id(self, id):
        for cell in self.cells:
            if cell.id == id:
                return cell
        return None

    def get_neighbors(self, cell):
        neighbors = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                neighbor = self.get_cell_by_id((cell.id[0] + x, cell.id[1] + y))
                if neighbor:
                    neighbors.append(neighbor)
        return neighbors
    
    def unselect_all(self):
        for cell in self.cells:
            cell.selected = False

cell_size = math.floor(map_italy.get_rect().width / 100)
grid = Grid(map_italy.get_rect().width, map_italy.get_rect().height, cell_size)

def game_interface():
    global game_state
    # Calculate the visible portion of the map
    visible_rect = pygame.Rect(-camera.offset.x / camera.zoom, -camera.offset.y / camera.zoom, SCREEN_WIDTH / camera.zoom, SCREEN_HEIGHT / camera.zoom)
    # Create a new surface that is the size of the visible area
    visible_surface = pygame.Surface((visible_rect.width, visible_rect.height))
    # Fill the new surface with white
    visible_surface.fill((255, 255, 255))

    # Blit the map onto the new surface at the appropriate offset
    visible_surface.blit(map_italy, (0, 0), visible_rect)

    # Calculate the position of the circle relative to the map
    circle_pos = (map_italy.get_width() // 2 - visible_rect.x, map_italy.get_height() // 2 - visible_rect.y)
    # Draw a circle at the calculated position
    pygame.draw.circle(visible_surface, (255, 0, 0), circle_pos, 50)

    for cell in grid.cells:
        cell_pos = (cell.rect.x - visible_rect.x, cell.rect.y - visible_rect.y)
        pygame.draw.rect(visible_surface, (0, 255, 0) if cell.selected else (0, 0, 0), cell_pos + (cell_size, cell_size), 1, 1)

    # Scale the visible surface to the screen size
    scaled_surface = pygame.transform.scale(visible_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Draw the scaled surface onto the screen
    screen.blit(scaled_surface, (0, 0))

class PopupWindow:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def add_text(self, screen, text):
        font = pygame.font.Font(None, 36)
        text = font.render(text, True, (0, 0, 0))
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

# Main game loop
mouse_down_pos = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state == 'game':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = 'menu'
            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    mouse_down_pos = event.pos
            # mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                # left click
                if event.button == 1:
                    window_pos = event.pos
                    map_pos = camera.unapply(event.pos)
                    if mouse_down_pos == window_pos:
                        cell = grid.get_cell(window_pos, camera)
                        if cell:
                            grid.unselect_all()
                            cell.selected = not cell.selected
                            print("Cell: "+str(cell.id))
                            print("Cell Neighbours: "+str([cell.id for cell in grid.get_neighbors(cell)]))
                        
            camera.handle_event(event)

    screen.fill(WHITE)

    if game_state == 'menu':
        start_menu()
    elif game_state == 'game':
        game_interface()
    
    pygame.display.flip()
