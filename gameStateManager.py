
from ui_manager import UIManager
from states.main_menu import main_menu
from states.game import GameInterface
from settings import hidden_variables as settings
from grid.grid import Grid
from player import Player
from computer import Computer

import pygame
import json

class GameStateManager:
    _instance = None

    def __new__(cls, grid=None, save_map=None):
        if cls._instance is None:
            cls._instance = super(GameStateManager, cls).__new__(cls)
            # Initial game state
            cls._instance.state = 'main_menu'
            cls._instance.interface = None
            cls._instance.ui_manager = UIManager(cls._instance)
            cls._instance.player = Player()
            cls._instance.grid = grid
            cls._instance.save_map = save_map
            cls._instance.map_name = None
            cls._instance.npcs = []
        return cls._instance

    def get_state(self):
        return self._instance.state
    
    def get_player(self):
        return self._instance.player
    
    def set_state(self, new_state):
        self._instance.state = new_state
        print(f"Game state changed to: {self._instance.state}")
        return self._instance.state
    
    def get_ui_manager(self):
        return self._instance.ui_manager
    
    def get_grid(self):
        return self._instance.grid
    
    def run(self, screen, game_state_manager, camera, events, SCREEN_WIDTH, SCREEN_HEIGHT):
        if self._instance.state == 'main_menu':
            main_menu(screen, game_state_manager)
        elif self._instance.state == 'game':
            self._instance.interface.run()
            game_state_manager.get_ui_manager().update(events)
            game_state_manager.get_ui_manager().render(screen)

    def save_game(self, save_name, *args, **kwargs):
        # Prepare the data to be saved
        save_data = {
            'save_name': save_name,
            'player_id': self._instance.get_player().get_player_id(),
            'map': {
                # map details to be added later
                'map_name': self._instance.map_name,
                'map_width': self._instance.grid.width,
                'map_height': self._instance.grid.height
            },
            'player': {
                'grid': {
                    'claimed_cells': [
                        {
                            'id': cell.id,
                            'cell_makeup': cell.cell_makeup,
                            'cell_type': cell.cell_type,
                            'claimed': cell.claimed,
                            'owner': cell.owner if cell.claimed else 'None'
                            # add other cell attributes here
                        }
                        for cell in self._instance.grid.cells if cell.claimed and cell.owner == self._instance.get_player().get_player_id()
                    ]
                }
            },
            'npcs': [
                {
                    'npc_id': npc.get_computer_id(),
                    'color': npc.get_color(), 
                    'grid': {
                        'claimed_cells': [
                            {
                                'id': cell.id,
                                'cell_makeup': cell.cell_makeup,
                                'cell_type': cell.cell_type,
                                'claimed': cell.claimed,
                                'owner': cell.owner if cell.claimed else 'None'
                                # add other cell attributes here
                            }
                            for cell in self._instance.grid.cells if cell.claimed and cell.owner == npc.get_computer_id()
                        ]
                    }
                }
                for npc in self._instance.npcs
            ]
        }

        # Serialize the data to a JSON file
        with open(f'{save_name}.json', 'w') as f:
            json.dump(save_data, f)

        print(f"Game saved as: {save_name}.json")     

    def new_game(self, *args, **kwargs):
        self._instance.reset()
        print("Starting new game")
        load_map = pygame.image.load('map_italy.png') # will be picked from a list of maps in the future

        cell_size = settings['cell_size'] # will be a map dependent setting in the future
        load_grid = Grid(load_map.get_rect().width, load_map.get_rect().height, cell_size, self._instance)
        
        # populate the cell makeup
        self._scan_map(load_grid, load_map, 20)

        self._instance.grid = load_grid
        self._instance.save_map = load_map
        self._instance.map_name = 'map_italy.png' # will be picked from a list of maps in the future
        self._instance.npcs.append(Computer(color=(255, 0, 0)))
        self._instance.ui_manager.reset()
        self._instance.interface = GameInterface(self._instance, load_map)
        return self._instance.set_state('game')

    def load_game(self, save_file_name):
        self._instance.reset()
        print(f"Loading game from: {save_file_name}.json")
        # Open the JSON file and load its content
        with open(f'{save_file_name}.json', 'r') as f:
            save_file = json.load(f)

        save_map = save_file['map']['map_name']
        saved_player_data = save_file['player']
        saved_npc_data = save_file['npcs']

        self._instance.player.player_id = save_file['player_id']

        load_map = pygame.image.load(save_map)

        cell_size = settings['cell_size'] # will be a map dependent setting in the future
        load_grid = Grid(load_map.get_rect().width, load_map.get_rect().height, cell_size, self._instance)
        
        # populate the cell makeup
        self._scan_map(load_grid, load_map, 50)

        # replace cells in load_grid with cells saved in save_grid
        for cell in saved_player_data['grid']['claimed_cells']:
            cell_id = tuple(cell['id'])  # Convert list to tuple
            load_cell = load_grid.get_cell_by_id(cell_id)
            load_cell.set_makeup(cell['cell_makeup'])
            load_cell.set_type(cell['cell_type'])
            self._instance.player.claim_cell(load_cell)

        for npc in saved_npc_data:
            computer = Computer()
            computer.computer_id = npc['npc_id']
            computer.color = npc['color']
            self._instance.npcs.append(computer)

            for cell in npc['grid']['claimed_cells']:
                cell_id = tuple(cell['id'])  # Convert list to tuple
                load_cell = load_grid.get_cell_by_id(cell_id)
                load_cell.set_makeup(cell['cell_makeup'])
                load_cell.set_type(cell['cell_type'])
                computer.claim_cell(load_cell)

        self._instance.grid = load_grid
        self._instance.save_map = load_map
        self._instance.map_name = save_map
        
        self._instance.ui_manager.reset()
        self._instance.interface = GameInterface(self._instance, load_map)
        self._instance.set_state('game')
        # move camera to mid point of map
        self._instance.get_ui_manager().get_camera().set_camera_position(load_map.get_rect().width/2, load_map.get_rect().height/2)
    
    def get_save_map(self):
        return self._instance.save_map
    
    def set_save_map(self, map):
        self._instance.save_map = map
        return self._instance.save_map
    

    
    # private methods
    def _scan_map(self, grid, load_map, band_factor):
        # Colors
        WATER = (0, 168, 243)  # Blue
        LAND = (16, 216, 0)  # Green
        SHORELINE = (0, 0, 0)  # Black

        def color_in_band(color1, color2, band_factor):
            return all(abs(c1 - c2) <= band_factor for c1, c2 in zip(color1, color2))
        
        cell_size = grid.cell_size

        # Loop through each cell in the grid
        for cell in grid.cells:
            # Loop through each pixel in the cell
            for x in range(cell.id[0]*cell_size, (cell.id[0]+1)*cell_size):
                for y in range(cell.id[1]*cell_size, (cell.id[1]+1)*cell_size):
                    try:
                        # Get the color of the pixel
                        color = load_map.get_at((x, y))
                    except IndexError:
                        continue

                    # Increment the count of this color in the cell
                    if color_in_band(color, WATER, band_factor):
                        cell.increment_makeup('water')
                    elif color_in_band(color, LAND, band_factor):
                        cell.increment_makeup('land')
                    elif color_in_band(color, SHORELINE, band_factor):
                        cell.increment_makeup('shoreline')

            # once the cell has been analyzed, set the type
            if cell.cell_makeup['shoreline'] > 0:
                cell.set_type('shoreline')
            elif cell.cell_makeup['water'] > cell.cell_makeup['land']:
                cell.set_type('water')
            else:
                cell.set_type('land')
        return True
    
    def quit(self, *args, **kwargs):
        pygame.quit()
        quit()

    def add_computer(self, computer):
        self._instance.npcs.append(computer)

    def reset(self):
        self._instance.player = Player()
        self._instance.grid = None
        self._instance.save_map = None
        self._instance.map_name = None
        self._instance.npcs = []
        
