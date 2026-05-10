import pygame as pg
import numpy as np
from scipy.sparse import coo_matrix

pg.init()

screen = pg.display.set_mode((920,920))

empty_tile_img = pg.image.load('images/empty_tile.png').convert()

grid = pg.Surface((920,920), pg.SRCALPHA) 

running = True
x = 0
y = 0

size_x, size_y = pg.display.get_surface().get_size()

coo = coo_matrix((size_x, size_y), dtype=np.int8).toarray()

for _ in range(size_x):
    for _ in range(size_y):
        grid.blit(empty_tile_img, (x, y))
        x += empty_tile_img.get_width()
    x = 0
    grid.blit(empty_tile_img, (x, y))
    y += empty_tile_img.get_height()

clock = pg.time.Clock()
delta_time = 0.1

while running:
    screen.fill((255,255,255))

    screen.blit(grid, (0,0))

    delta_time = clock.tick(60)
    delta_time = max(0.001, min(0.1, delta_time))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
    pg.display.flip()

pg.quit()