import pygame as pg

GREY = (130,130,130) # RGB value for my grey
MARGIN = 20

def create_info_panel(WIDTH,HEIGHT, playing, slowed_by):
    panel = pg.Surface((WIDTH,HEIGHT),pg.SRCALPHA)
    panel.fill(GREY)

    if playing:
        image = pg.image.load("images/playing_text.png")
    else:
        image = pg.image.load("images/paused_text.png")
    
    panel.blit(image, (WIDTH//2 - image.get_width(), (HEIGHT - 40)//2))

    if(slowed_by == 3):
        number = pg.image.load("images/number_point_five.png")
    elif (slowed_by == 2):
        number = pg.image.load("images/number_one.png")
    elif (slowed_by == 1):
        number = pg.image.load("images/number_two.png")
    elif (slowed_by == 0):
        number = pg.image.load("images/number_three.png")
    
    image = pg.image.load("images/speed_text.png")
    panel.blit(image, (WIDTH - image.get_width() - number.get_width() - 2*MARGIN, (HEIGHT - 40)//2))

    panel.blit(number, (WIDTH - number.get_width() - MARGIN, (HEIGHT - 40)//2))

    return panel

