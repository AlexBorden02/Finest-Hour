
import pygame

def game_interface(screen, game_state_manager, camera, events, grid, world_map, cell_size, SCREEN_WIDTH, SCREEN_HEIGHT):
    # Calculate the visible portion of the map
    visible_rect = pygame.Rect(-camera.offset.x / camera.zoom, -camera.offset.y / camera.zoom, SCREEN_WIDTH / camera.zoom, SCREEN_HEIGHT / camera.zoom)
    # Create a new surface that is the size of the visible area
    visible_surface = pygame.Surface((visible_rect.width, visible_rect.height))
    # Fill the new surface with white
    visible_surface.fill((255, 255, 255))

    # Blit the map onto the new surface at the appropriate offset
    visible_surface.blit(world_map, (0, 0), visible_rect)

    # Calculate the position of the circle relative to the map
    circle_pos = (world_map.get_width() // 2 - visible_rect.x, world_map.get_height() // 2 - visible_rect.y)
    # Draw a circle at the calculated position
    pygame.draw.circle(visible_surface, (255, 0, 0), circle_pos, 50)

    for cell in grid.cells:
        cell_pos = (cell.rect.x - visible_rect.x, cell.rect.y - visible_rect.y)
        if cell.selected:
            pygame.draw.rect(visible_surface, (0, 255, 0), (cell_pos[0], cell_pos[1], cell_size, cell_size), 1, 1)

    # Scale the visible surface to the screen size
    scaled_surface = pygame.transform.scale(visible_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Draw the scaled surface onto the screen
    screen.blit(scaled_surface, (0, 0))

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state_manager.set_state('main_menu')
        # mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN:
            # left click
            if event.button == 1:
                game_state_manager.set_mouse_down_pos(event.pos)
        # mouse button up
        if event.type == pygame.MOUSEBUTTONUP:
            # left click
            if event.button == 1:
                window_pos = event.pos
                map_pos = camera.unapply(event.pos)
                print("Mouse Clicked: "+str(window_pos))
                if game_state_manager.get_mouse_down_pos() == window_pos:
                    cell = grid.get_cell(window_pos, camera)
                    if cell:
                        cell.selected = not cell.selected
                        print("Cell: "+str(cell.id))
                        print("Cell Neighbours: "+str([cell.id for cell in grid.get_neighbors(cell)]))