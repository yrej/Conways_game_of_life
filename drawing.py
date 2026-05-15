from pygame import image, Surface, display
from info_panel import create_info_panel
from constants import WIDTH, GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, UPPER_MARGIN

def fill_cells(positions,grid,filled_tile_img):
    for pos in positions:
        col, row = pos
        if 0 <= col < GRID_WIDTH and 0 <= row < GRID_HEIGHT:
            grid.blit(filled_tile_img, (col * TILE_SIZE, row * TILE_SIZE))

def empty_cells(positions,grid,empty_tile_img):
    for pos in positions:
        col, row = pos
        grid.blit(empty_tile_img, (col * TILE_SIZE, row * TILE_SIZE))

def draw(screen,grid,tile_img,text_images,emptied_cells, filled_cells, playing,speed,show_help,overlay):
    empty_cells(emptied_cells,grid,tile_img["empty"])
    fill_cells(filled_cells,grid,tile_img["filled"])
    emptied_cells = set()
    screen.blit(create_info_panel(playing,speed,text_images),(0,0))
    screen.blit(grid, (0, UPPER_MARGIN))
    if show_help:
        overlay.draw(screen)
