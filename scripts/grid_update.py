from scripts.constants import GRID_HEIGHT, GRID_WIDTH

def update_grid(positions : set[tuple[int,int]], margin : int = 2) -> set[tuple[int,int]]:
    """Vypočítá novou generaci buněk podle pravidel Conwayovy hry života.

    Prochází všechny živé buňky a jejich sousedy a podle následujících
    pravidel určí stav každé buňky v další generaci:

    - Živá buňka s 2 nebo 3 živými sousedy přežije.
    - Mrtvá buňka s právě 3 živými sousedy ožije.
    - Všechny ostatní buňky zůstanou nebo se stanou mrtvými.

    Args:
        positions: Množina souřadnic (x, y) aktuálně živých buněk.
        margin: Počet buněk přesahujících hranici mřížky, ve kterých může
            simulace probíhat. Výchozí hodnota je 2.

    Returns:
        ``set[tuple[int, int]]``: Množina souřadnic živých buněk v další generaci.
    """
    all_neighbours = set()
    new_positions = set()

    for pos in positions:
        neighbours = get_neighbours(pos,margin)
        all_neighbours.update(neighbours)

        neighbours = list(filter(lambda x: x in positions, neighbours))

        if len(neighbours) == 2 or len(neighbours) == 3:
            new_positions.add(pos)
    
    for pos in all_neighbours:
        neighbours = list(filter(lambda x: x in positions, get_neighbours(pos,margin)))

        if len(neighbours) == 3:
            new_positions.add(pos)
    
    return new_positions

def get_neighbours(position : set[tuple[int,int]], margin : int) -> list[tuple[int,int]]:
    """Vrátí seznam všech sousedů dané buňky.

    Prochází všech 8 okolních pozic a vrátí ty, které leží uvnitř
    hranic mřížky rozšířených o ``margin`` buněk na každou stranu.

    Args:
        position: Souřadnice buňky (x, y), jejíž sousedy hledáme.
        margin: Počet buněk přesahujících hranici mřížky, které jsou
            stále simulovány.

    Returns:
        ``list[tuple[int, int]]``: Seznam souřadnic sousedních buněk.
    """
    x,y = position
    neighbours = []
    for dx in [-1, 0, 1]:
        if x + dx < -margin or x + dx >= GRID_WIDTH + margin:continue
        
        for dy in [-1, 0, 1]:
            if y + dy < -margin or y + dy >= GRID_HEIGHT + margin:continue
            if dx == 0 and dy == 0: continue

            neighbours.append((x + dx, y + dy))
    return neighbours

