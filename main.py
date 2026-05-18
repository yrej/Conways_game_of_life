import pygame as pg
from scripts.grid_update import update_grid
from scripts.overlay import HelpOverlay
from scripts.drawing import draw, empty_grid
from scripts.viewport_adjust import draw_new_viewport
from scripts.constants import UPPER_MARGIN, WIDTH, HEIGHT, TILE_SIZE, FPS

pg.init()

screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()

tile_img = {
    "empty_light" : pg.image.load('images/empty_tile_light.png').convert(),
    "empty_dark" : pg.image.load('images/empty_tile_dark.png').convert(),
    "filled" : pg.image.load('images/filled_tile.png').convert()
}

grid = pg.Surface((WIDTH,HEIGHT - UPPER_MARGIN))

text_images = {
    "playing" : pg.image.load("images/playing_text.png").convert_alpha(),
    "paused" : pg.image.load("images/paused_text.png").convert_alpha(),
    "mode" : pg.image.load("images/mode_text.png").convert_alpha(),
    "speed" : pg.image.load("images/speed_text.png").convert_alpha(),
    "point_five" : pg.image.load("images/number_point_five.png").convert_alpha(),
    "one" : pg.image.load("images/number_one.png").convert_alpha(),
    "two" : pg.image.load("images/number_two.png").convert_alpha(),
    "three" : pg.image.load("images/number_three.png").convert_alpha()
}

def main():
    """Hlavní vstupní bod simulace Conwayovy hry života.

    Inicializuje herní stav, spravuje hlavní smyčku událostí, zpracovává
    vstup uživatele a každý snímek posouvá v simulaci vpřed.

    Smyčka zajišťuje následující:
        - Posun simulace o jednu generaci vpřed.
        - Přepínání jednotlivých buněk levým kliknutím (pouze při pauze).
        - Pozastavení a spuštění simulace mezerníkem.
        - Vymazání mřížky klávesou C.
        - Úpravu rychlosti simulace šipkami nahoru/dolů.
        - Zavření nápovědy kliknutím nebo stiskem libovolné klávesy.

    Returns:
        None
    """
        
    running = True
    playing = False
    show_help = True
    needs_redraw = True
    dragging = False
    play_b4_drag = False
    mode = "empty_light"

    count = 0
    speed = 2

    offset_x, offset_y = 0, 0
    last_mouse_pos = (0,0)

    filled_cells = set()
    emptied_cells = set()

    empty_grid(grid,tile_img,mode)
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
                    curr_col = mouse_x // TILE_SIZE + offset_x
                    curr_row = (mouse_y - UPPER_MARGIN) // TILE_SIZE + offset_y
                    position = (curr_col, curr_row)
                    if position in filled_cells:
                        filled_cells.remove(position)
                        emptied_cells.add(position)
                    else:
                        filled_cells.add(position)
                    needs_redraw = True

                if event.button == 3:
                    dragging = True
                    last_mouse_pos = pg.mouse.get_pos()
                    if playing:
                        playing = False
                        play_b4_drag = True
            
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    dragging = False
                    if play_b4_drag: 
                        playing = True
                        play_b4_drag = False

            if event.type == pg.MOUSEMOTION:
                if dragging:
                    mx,my = pg.mouse.get_pos()
                    dx = last_mouse_pos[0] - mx
                    dy = last_mouse_pos[1] - my
                    offset_x += dx // TILE_SIZE
                    offset_y += dy // TILE_SIZE
                    last_mouse_pos = (mx + dx % TILE_SIZE, my + dy % TILE_SIZE)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and speed > 0:
                   speed -= 1
                   needs_redraw = True
                if event.key == pg.K_DOWN and speed < 3:
                    speed += 1
                    needs_redraw = True
                
                if event.key == pg.K_m and not playing:
                    if mode == "empty_dark":
                        mode = "empty_light"
                    elif mode == "empty_light":
                        mode = "empty_dark"
                    empty_grid(grid,tile_img,mode)
                    needs_redraw = True

                if dragging:continue
                if event.key == pg.K_SPACE:
                    playing = not playing
                    needs_redraw = True
                if event.key == pg.K_r:
                    empty_grid(grid,tile_img,mode)
                    count = 0
                    filled_cells = set()
                    emptied_cells = set()
                    offset_x,offset_y = 0,0
                    needs_redraw = True
                    playing = False
        
        if offset_x != 0 or offset_y != 0:
            draw_new_viewport(screen,grid,tile_img,mode,text_images,filled_cells,playing,speed,offset_x,offset_y)
            needs_redraw = False

        if needs_redraw:
            draw(screen,grid,tile_img,mode,text_images,emptied_cells,filled_cells,playing,speed,show_help,overlay)
            needs_redraw = False
        
        pg.display.flip()
    pg.quit()

if __name__ == '__main__':
    main()