import pygame as pg
from grid_update import update_grid
from overlay import HelpOverlay

pg.init()

WIDTH, HEIGHT = 920,920
TILE_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE 
FPS = 60

screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
delta_time = 0.1

empty_tile_img = pg.image.load('images/empty_tile.png').convert()
filled_tile_img = pg.image.load('images/filled_tile.png').convert()

grid = pg.Surface((WIDTH,HEIGHT))

def fill_cells(positions):
    for pos in positions:
        col, row = pos
        grid.blit(filled_tile_img, (col * TILE_SIZE, row * TILE_SIZE))

def empty_cells(positions):
    for pos in positions:
        col, row = pos
        grid.blit(empty_tile_img, (col * TILE_SIZE, row * TILE_SIZE))

def empty_grid():
    size_x, size_y = pg.display.get_surface().get_size()

    for x in range(0, size_x, TILE_SIZE):
        for y in range(0, size_y, TILE_SIZE):
            grid.blit(empty_tile_img, (x, y))

def main():
    running = True
    playing = False
    show_help = True
    needs_redraw = True


    count = 0
    update_freq = 60

    filled_cells = set()
    emptied_cells = set()

    empty_grid()

    overlay = HelpOverlay(WIDTH, HEIGHT)
    
    while running:
        delta_time = clock.tick(FPS)
        delta_time = max(0.001, min(0.1, delta_time))

        if playing:
            count += 1
        if count >= update_freq:
            count = 0
            emptied_cells = filled_cells
            filled_cells = update_grid(filled_cells, GRID_WIDTH, GRID_HEIGHT)
            emptied_cells = emptied_cells - filled_cells 
            needs_redraw = True

        pg.display.set_caption("Playing" if playing else "Paused")

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if show_help:
                if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.KEYDOWN:
                    show_help = False
                    needs_redraw = True
                continue

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()

                if event.button == 1:
                    curr_col, curr_row = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
                    position = (curr_col, curr_row)
                    if position in filled_cells:
                        filled_cells.remove(position)
                        emptied_cells.add(position)
                    else:
                        filled_cells.add(position)
                    needs_redraw = True

                if event.button == 3:
                    pass

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    playing = not playing
                if event.key == pg.K_c:
                    empty_grid()
                    count = 0
                    filled_cells = set()
                    emptied_cells = set()
                    needs_redraw = True
                    playing = False
                if event.key == pg.K_UP and update_freq > 45:
                    update_freq -= 30
                if event.key == pg.K_DOWN and update_freq < 120:
                    update_freq += 30
    
        if needs_redraw:
            empty_cells(emptied_cells)
            fill_cells(filled_cells)
            emptied_cells = set()
            screen.blit(grid, (0, 0))
            if show_help:
                overlay.draw(screen)
            needs_redraw = False
        
        
        pg.display.flip()
    pg.quit()

if __name__ == '__main__':
    main()