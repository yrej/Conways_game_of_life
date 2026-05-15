from pygame import image, Surface, display
from scripts.info_panel import create_info_panel
from scripts.constants import WIDTH, GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, UPPER_MARGIN

def fill_cells(positions : set[tuple[int,int]],grid : Surface,filled_tile_img : Surface) -> None:
    for pos in positions:
        col, row = pos
        if 0 <= col < GRID_WIDTH and 0 <= row < GRID_HEIGHT:
            grid.blit(filled_tile_img, (col * TILE_SIZE, row * TILE_SIZE))

def empty_cells(positions : set[tuple[int,int]],grid : Surface,empty_tile_img : Surface) -> None:
    for pos in positions:
        col, row = pos
        grid.blit(empty_tile_img, (col * TILE_SIZE, row * TILE_SIZE))

def draw(screen : Surface,grid : Surface,tile_img : dict[str, Surface],text_images : dict[str, Surface],emptied_cells : set[tuple[int,int]], filled_cells : set[tuple[int,int]], playing : bool,speed : int,show_help : bool,overlay) -> None:
    empty_cells(emptied_cells,grid,tile_img["empty"])
    fill_cells(filled_cells,grid,tile_img["filled"])
    emptied_cells = set()
    screen.blit(create_info_panel(playing,speed,text_images),(0,0))
    screen.blit(grid, (0, UPPER_MARGIN))
    if show_help:
        overlay.draw(screen)
