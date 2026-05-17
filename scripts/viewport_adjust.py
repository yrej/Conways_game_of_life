from __future__ import annotations
from scripts.drawing import empty_grid,draw
from scripts.constants import TILE_SIZE

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygame import Surface

def sub_tuples(a : tuple[int,int], b : tuple[int,int]) -> tuple[int, int]:
    """Odečte dva tuply od sebe"""
    return (a[0] - b[0], a[1] - b[1])


def cell_to_screen(filled_cells : set[tuple[int,int]], offset_x : int, offset_y : int) -> set[tuple[int,int]]:
    """Převede souřadnice buněk do souřadnic obrazovky odečtením offsetu.

    Args:
        filled_cells: Množina souřadnic buněk ve formátu (x, y).
        offset_x: Posun v ose X.
        offset_y: Posun v ose Y.

    Returns:
        ``set[tuple[int,int]]`` : Množina souřadnic převedených do prostoru obrazovky.
    """
    new_filled = set()
    for pos in filled_cells:
        new_filled.add(sub_tuples(pos,(offset_x,offset_y)))
    return new_filled

def draw_new_viewport(screen : Surface,
         grid : Surface,
         tile_img : dict[str, Surface],
         text_images : dict[str, Surface], 
         filled_cells : set[tuple[int,int]], 
         playing : bool,
         slowed_by : int,
         offset_x : int,
         offset_y : int) -> None:
    """Vykreslí snímek po posunu obrazovky.

    Aktualizuje mřížku podle změněných buněk, vykreslí informační panel
    a v případě potřeby zobrazí nápovědu. Voláno pouze pokud je nastaven
    příkaz ``needs_redraw``.

    Args:
        screen: Hlavní zobrazovací povrch.
        grid: Povrch mřížky se stavem buněk.
        tile_img: Slovník obrázků dlaždic s klíči ``"empty"`` a ``"filled"``.
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
    
    empty_grid(grid,tile_img)
    draw(screen,grid,tile_img,text_images,set(),cell_to_screen(filled_cells,offset_x,offset_y),playing,slowed_by,False)
