from pygame import Surface
from scripts.constants import WIDTH, UPPER_MARGIN, INFO_MARGIN as MARGIN, COLOR_DARK_GREY as GREY

def create_info_panel(playing : bool, slowed_by : int,text_images : dict[str, Surface],tile_img : dict[str, Surface],mode : str) -> Surface:
    """Vytvoří informační panel zobrazený v horní části okna.

    Vykreslí panel s aktuálním stavem simulace (běží / pozastaveno) a
    aktuální rychlostí simulace. Panel je vykreslen jako povrch s šedým pozadím.
    Nakteré je vykreslován stylyzovaný text

    Rychlost simulace je určena hodnotou ``slowed_by``:

    +------------+----------+
    | slowed_by  | rychlost |
    +============+==========+
    | 0          | 3x       |
    +------------+----------+
    | 1          | 2x       |
    +------------+----------+
    | 2          | 1x       |
    +------------+----------+
    | 3          | 0.5x     |
    +------------+----------+

    Args:
        playing: ``True`` pokud simulace běží, ``False`` pokud je pozastavena.
        slowed_by: Úroveň zpomalení simulace v rozsahu 0–3.
        text_images: Slovník povrchů s textovými obrázky. Očekávané klíče:
            ``"playing"``, ``"paused"``, ``"mode"``, ``"speed"``, ``"point_five"``,
            ``"one"``, ``"two"``, ``"three"``.
        tile_img: Slovník obrázků dlaždic s klíči ``"empty"`` a ``"filled"``.
        mode : string s klíči ``"empty_light"`` a ``"empty_dark"`` pro slovník tile_img

    Returns:
        Surface: Vykreslený informační panel připravený k zobrazení na obrazovce.
    """
    panel = Surface((WIDTH,UPPER_MARGIN))
    panel.fill(GREY)

    panel.blit(text_images["mode"], (10, (UPPER_MARGIN - 40)//2))
    panel.blit(tile_img[mode], (text_images["mode"].get_width() + tile_img[mode].get_width(), (UPPER_MARGIN - 40)//2))

    if playing:
        text_status_image = text_images["playing"]
    else:
        text_status_image = text_images["paused"]
    
    panel.blit(text_status_image, ((WIDTH - text_status_image.get_width())//2, (UPPER_MARGIN - 40)//2))

    if(slowed_by == 3):
        number = text_images["point_five"]
    elif (slowed_by == 2):
        number = text_images["one"]
    elif (slowed_by == 1):
        number = text_images["two"]
    elif (slowed_by == 0):
        number = text_images["three"]
    
    panel.blit(text_images["speed"], (WIDTH - text_images["speed"].get_width() - number.get_width() - 2*MARGIN, (UPPER_MARGIN - 40)//2))

    panel.blit(number, (WIDTH - number.get_width() - MARGIN, (UPPER_MARGIN - 40)//2))

    return panel

