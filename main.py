import pygame as pg
from scripts.grid_update import update_grid
from scripts.overlay import HelpOverlay
from scripts.drawing import draw
from scripts.constants import UPPER_MARGIN, WIDTH, HEIGHT, TILE_SIZE, FPS

pg.init()

screen = pg.display.set_mode((WIDTH,HEIGHT - UPPER_MARGIN))
clock = pg.time.Clock()

tile_img = {
    "empty" : pg.image.load('images/empty_tile.png').convert(),
    "filled" : pg.image.load('images/filled_tile.png').convert()
}

grid = pg.Surface((WIDTH,HEIGHT))

text_images = {
    "playing" : pg.image.load("images/playing_text.png").convert_alpha(),
    "paused" : pg.image.load("images/paused_text.png").convert_alpha(),
    "speed" : pg.image.load("images/speed_text.png").convert_alpha(),
    "point_five" : pg.image.load("images/number_point_five.png").convert_alpha(),
    "one" : pg.image.load("images/number_one.png").convert_alpha(),
    "two" : pg.image.load("images/number_two.png").convert_alpha(),
    "three" : pg.image.load("images/number_three.png").convert_alpha()
}

def empty_grid() -> None:
    size_x, size_y = pg.display.get_surface().get_size()

    for x in range(0, size_x, TILE_SIZE):
        for y in range(0, size_y, TILE_SIZE):
            grid.blit(tile_img["empty"], (x, y))

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

    overlay = HelpOverlay()
    
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
        if count >= 10 + speed * 30:
            count = 0
            emptied_cells = filled_cells
            filled_cells = update_grid(filled_cells)
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
            draw(screen,grid,tile_img,text_images,emptied_cells,filled_cells,playing,speed,show_help,overlay)
            needs_redraw = False
        
        
        pg.display.flip()
    pg.quit()

if __name__ == '__main__':
    main()