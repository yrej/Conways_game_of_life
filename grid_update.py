def update_grid(positions, g_width, g_height):
    all_neighbours = set()
    new_positions = set()

    for pos in positions:
        neighbours = get_neighbours(pos,g_width, g_height)
        all_neighbours.update(neighbours)

        neighbours = list(filter(lambda x: x in positions, neighbours))

        if len(neighbours) == 2 or len(neighbours) == 3:
            new_positions.add(pos)
    
    for pos in all_neighbours:
        neighbours = list(filter(lambda x: x in positions, get_neighbours(pos,g_width, g_height)))

        if len(neighbours) == 3:
            new_positions.add(pos)
    
    return new_positions

def get_neighbours(position, g_width, g_height):
    x,y = position
    neighbours = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx >= g_width:continue
        
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy >= g_height:continue
            if dx == 0 and dy == 0: continue

            neighbours.append((x + dx, y + dy))
    return neighbours

