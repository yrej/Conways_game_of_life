from __future__ import annotations

from pygame import  Surface
from scripts.info_panel import create_info_panel
from scripts.constants import WIDTH,HEIGHT, GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, UPPER_MARGIN


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.overlay import HelpOverlay

def empty_grid(grid : Surface,tile_img : dict[str, Surface],mode : str) -> None:
    """Vyplní celý povrch mřížky prázdnými dlaždicemi.

    Prochází povrch displeje po krocích velikosti TILE_SIZE a na každou
    pozici vykreslí obrázek prázdné dlaždice, čímž efektivně vymaže mřížku.

    Args:
        grid: Povrch mřížky, na který se buňky vykreslují.
        tile_img: Slovník obrázků dlaždic s klíči ``"empty"`` a ``"filled"``.
        mode : string s klíči ``"empty_light"`` a ``"empty_dark"`` pro slovník tile_img
    
    Returns:
        None
    """
    size_x, size_y = WIDTH, HEIGHT - UPPER_MARGIN

    for x in range(0, size_x, TILE_SIZE):
        for y in range(0, size_y, TILE_SIZE):
            grid.blit(tile_img[mode], (x, y))


def fill_cells(positions : set[tuple[int,int]],grid : Surface, filled_tile_img : Surface) -> None:
    """Vykreslí živé buňky na mřížku.

    Prochází zadané pozice a na každou vykreslí obrázek živé buňky.
    Pozice mimo hranice mřížky jsou přeskočeny.

    Args:
        positions: Množina souřadnic (x, y) buněk k vykreslení.
        grid: Povrch mřížky, na který se buňky vykreslují.
        filled_tile_img: Obrázek živé buňky.

    Returns:
        None
    """

    for pos in positions:
        col, row = pos
        if 0 <= col < GRID_WIDTH and 0 <= row < GRID_HEIGHT:
            grid.blit(filled_tile_img, (col * TILE_SIZE, row * TILE_SIZE))

def empty_cells(positions : set[tuple[int,int]],grid : Surface,empty_tile_img : Surface) -> None:
    """Vykreslí mrtvé buňky na mřížku.

    Prochází zadané pozice a na každou vykreslí obrázek prázdné buňky,
    čímž ji vizuálně označí jako mrtvou.

    Args:
        positions: Množina souřadnic (x, y) buněk k vymazání.
        grid: Povrch mřížky, na který se buňky vykreslují.
        empty_tile_img: Obrázek prázdné (mrtvé) buňky.

    Returns:
        None
    """

    for pos in positions:
        col, row = pos
        grid.blit(empty_tile_img, (col * TILE_SIZE, row * TILE_SIZE))

def draw(screen : Surface,
         grid : Surface,
         tile_img : dict[str, Surface],
         mode : str,
         text_images : dict[str, Surface],
         emptied_cells : set[tuple[int,int]], 
         filled_cells : set[tuple[int,int]], 
         playing : bool,
         slowed_by : int,
         show_help : bool,
         overlay : HelpOverlay = None) -> None:
    """Vykreslí celý aktuální snímek na obrazovku.

    Aktualizuje mřížku podle změněných buněk, vykreslí informační panel
    a v případě potřeby zobrazí nápovědu. Voláno pouze pokud je nastaven
    příkaz ``needs_redraw``.

    Args:
        screen: Hlavní zobrazovací povrch.
        grid: Povrch mřížky se stavem buněk.
        tile_img: Slovník obrázků dlaždic s klíči ``"empty"`` a ``"filled"``.
        mode : string s klíči ``"empty_light"`` a ``"empty_dark"`` pro slovník tile_img
        text_images: Slovník obrázků textů pro informační panel.
        emptied_cells: Množina buněk, které byly v této generaci zabity.
        filled_cells: Množina aktuálně živých buněk.
        playing: ``True`` pokud simulace běží, ``False`` pokud je pozastavena.
        slowed_by: Úroveň zpomalení simulace v rozsahu 0–3.
        show_help: ``True`` pokud má být zobrazena nápověda.
        overlay: Instance třídy ``HelpOverlay`` zodpovědná za vykreslení nápovědy.

    Returns:
        None
    """
    empty_cells(emptied_cells,grid,tile_img[mode])
    fill_cells(filled_cells,grid,tile_img["filled"])
    emptied_cells = set()
    screen.blit(create_info_panel(playing,slowed_by,text_images,tile_img,mode),(0,0))
    screen.blit(grid, (0, UPPER_MARGIN))
    if show_help:
        if overlay != None:
            overlay.draw(screen)
        else:
            raise AttributeError("Byl poslán ``show_help`` jako true s prázdným overlay")
