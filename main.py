import pygame as pg

# okno
screen = pg.display.set_mode((1280, 768))
pg.display.set_caption("Train Simulator")

clock = pg.time.Clock()

import functions as f
import variables as v
from classes import Exit

# konverze obrázků
for znak, picture in f.tiles.items():
    f.tiles[znak] = picture.convert_alpha()

f.draw_homescreen(screen)

run = True
while run:
    clock.tick(30) 

    if v.game:
        # vykreslení mapy a ovládacího panelu
        f.game_mode_draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if f.can_press:
                for i in f.can_press:
                    if i.rect.collidepoint(event.pos):
                        if isinstance(i, Exit):
                            v.game = False
                            run = False
                        else:
                            i.click(screen) 
                for train in v.trains:
                    if train.rect.collidepoint(event.pos):
                        v.curr_train = train
                        v.mode = None
        
    # zobrazeni
    pg.display.flip()

pg.quit()