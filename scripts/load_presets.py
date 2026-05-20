from scripts.constants import GRID_WIDTH, GRID_HEIGHT

def find_extremes(cells : set[tuple[int,int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """Najde minimální a maximální souřadnice v seznamu buněk.

    Args:
        cells: Seznam dvojic ``(x, y)`` reprezentujících pozice buněk.

    Returns:
        Dvojice ``((max_x, min_x), (max_y, min_y))``, kde každá složka
        obsahuje maximální a minimální hodnotu dané osy.
    """
    max_x, max_y = cells[0]
    min_x, min_y = cells[0]
    for cell in cells :
        if cell[0] > max_x: max_x = cell[0]
        if cell[0] < min_x: min_x = cell[0]
        if cell[1] > max_y: max_y = cell[1]
        if cell[1] < min_y: min_y = cell[1]
    return (max_x,min_x),(max_y,min_y)
        

def preset_to_screen(preset_string : str ,filled_cells :  set[tuple[int,int]], emptied_cells :  set[tuple[int,int]],offset_x : int, offset_y : int) -> set[tuple[int,int]]:
    """Načte preset ze souboru, vystředí ho na mřížku a vymaže překryté buňky.

    Načte seznam buněk ze souboru ``presets/<preset_string>.txt``, posune ho
    do středu mřížky (dle ``GRID_WIDTH`` a ``GRID_HEIGHT``) a aplikuje
    dodatečný offset. Všechny aktuálně zaplněné buňky, které leží v oblasti
    presetu, jsou přesunuty do ``emptied_cells`` a odebrány z ``filled_cells``.

    Args:
        preset_string: Název souboru presetu bez přípony, např. ``"glider"``.
        filled_cells: Množina aktuálně zaplněných buněk. Buňky v oblasti
            presetu jsou z ní odebrány.
        emptied_cells: Množina vyprázdněných buněk. Buňky odebrané
            z ``filled_cells`` jsou do ní přidány.
        offset_x: Dodatečný posun presetu v ose x v jednotkách mřížky.
        offset_y: Dodatečný posun presetu v ose y v jednotkách mřížky.

    Returns:
        Seznam dvojic ``(x, y)`` reprezentujících buňky presetu po aplikaci
        středování a offsetu.
    """
    file  = open(f"presets/{preset_string}.txt").read()
    preset = [
        ((x + GRID_WIDTH//2) + offset_x, (y + GRID_HEIGHT//2) + offset_y)
        for x, y in (
        tuple(int(n) for n in part.strip("()").split(","))
        for part in file.split("),(") )
    ]
    ex_x, ex_y = find_extremes(preset)
    to_update = set()
    for cell in filled_cells:
        if ex_x[1] - 1 <= cell[0] <= ex_x[0] + 1 and ex_y[1] - 1 <= cell[1] <= ex_y[0] + 1:
            to_update.add(cell)
    for item in to_update:
        filled_cells.remove(item)
        emptied_cells.add(item)

    return preset