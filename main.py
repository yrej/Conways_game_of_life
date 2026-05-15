import pygame as pg
from grid_update import update_grid
from overlay import HelpOverlay
from info_panel import create_info_panel

pg.init()

UPPER_MARGIN = 50
WIDTH, HEIGHT = 1000,1000 + UPPER_MARGIN
TILE_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = WIDTH // TILE_SIZE, HEIGHT - UPPER_MARGIN // TILE_SIZE 
FPS = 60

screen = pg.display.set_mode((WIDTH,HEIGHT - UPPER_MARGIN))
clock = pg.time.Clock()

empty_tile_img = pg.image.load('images/empty_tile.png').convert()
filled_tile_img = pg.image.load('images/filled_tile.png').convert()

grid = pg.Surface((WIDTH,HEIGHT))

def fill_cells(positions):
    for pos in positions:
        col, row = pos
        if 0 <= col < GRID_WIDTH and 0 <= row < GRID_HEIGHT:
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
    speed = 2

    filled_cells = set()
    emptied_cells = set()

    empty_grid()
    pg.display.set_caption("Conways game of life")

    overlay = HelpOverlay(WIDTH, HEIGHT)
    
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
        if count >= 10 + speed * 30:
            count = 0
            emptied_cells = filled_cells
            filled_cells = update_grid(filled_cells, GRID_WIDTH, GRID_HEIGHT)
            emptied_cells = emptied_cells - filled_cells 
            needs_redraw = True

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

                if event.button == 1 and not playing:
                    curr_col, curr_row = mouse_x // TILE_SIZE, (mouse_y - UPPER_MARGIN) // TILE_SIZE
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
                    needs_redraw = True
                if event.key == pg.K_c:
                    empty_grid()
                    count = 0
                    filled_cells = set()
                    emptied_cells = set()
                    needs_redraw = True
                    playing = False
                if event.key == pg.K_UP and speed > 0:
                   speed -= 1
                   needs_redraw = True
                if event.key == pg.K_DOWN and speed < 3:
                    speed += 1
                    needs_redraw = True
    
        if needs_redraw:
            empty_cells(emptied_cells)
            fill_cells(filled_cells)
            emptied_cells = set()
            screen.blit(create_info_panel(WIDTH,UPPER_MARGIN,playing,speed),(0,0))
            screen.blit(grid, (0, UPPER_MARGIN))
            if show_help:
                overlay.draw(screen)
            needs_redraw = False
        
        
        pg.display.flip()
    pg.quit()

if __name__ == '__main__':
    main()