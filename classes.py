import pygame as pg
from pygame.sprite import *
import variables as v
from pygame.math import Vector2 as Vec 

pg.font.init()

# třídy obrázkové a textové tlačítko
class ImageButton():
    def __init__(self, image_path, x, y):
        self.image = pg.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

    def draw(self, surface):
        surface.blit(self.image, self.rect) # vykreslení tlačítka

class Button:
    def __init__(self, text, x, y, h, w, color, text_color, text_size = 24):
        self.text = text
        self.rect = pg.Rect(x, y, h, w)
        self.color = color
        self.tc = text_color
        self.clicked = False
        self.text_size = text_size
        self.font = pg.font.Font("fonty/PressStart2P.ttf", self.text_size)

    def draw(self, surface):
        # vykreslení tlacitka
        pg.draw.rect(surface, self.color, self.rect)

        #vykreslení textu
        text = self.font.render(self.text, True, self.tc)
        text_pos = text.get_rect(center = self.rect.center)
        surface.blit(text, text_pos)

# třída pro segment trati
class Segment:
    def __init__(self, start, end, dx, dy, lights = None, switch = None, black_hole = False):
        self.s = start
        self.e = end
        self.vect = (dx//abs(dx), 0) if dy == 0 else (0, dy//abs(dy))
        self.dx = dx
        self.dy = dy
        self.black_hole = black_hole
        self.light = lights
        self.switch = switch

# třídy pro jednotlivé objekty
# vlaky

angle = {   # rotace pro jednotlivé směry
            (1, 0): 0, 
            (0, -1): 90, 
            (-1, 0): 180,  
            (0, 1): 270 
        }

class Train(Sprite):
    def __init__(self, image_path, pos, segment, number_in_set, direction = "right"):
        super().__init__()
        global angle
        self.segment = segment
        self.original_image = pg.image.load(image_path).convert_alpha()

        self.image = pg.transform.rotate(self.original_image, angle[self.segment.vect])
        self.rect = self.image.get_rect(center = pos)
        self.pos = pos
        self.speed = 0
        self.dir = direction

        self.segment = segment
        self.number = number_in_set

        self.stop = 64
        self.curr_speed = self.speed
        self.time = 0

    def update(self, surface):
        self.move(surface)

    def move(self, surface):
        from functions import find_new_segment
        global angle

        if self.time > 0:
            if self.curr_speed != 0:
                self.time = 0
            self.time -= 1
            return
        else:
            self.curr_speed = self.speed

        to_end = Vec(self.segment.e) - Vec(self.pos)
        dist_from_end = to_end.length()

        next_segment = find_new_segment(self.segment.e, self.segment.s, self.dir)

        if dist_from_end <= self.stop :
            if next_segment or self.segment.black_hole:
                self.curr_speed = self.speed
            else:
                self.curr_speed = 0
        else:
            self.curr_speed = self.speed

        move_dist = min(dist_from_end, self.curr_speed)
        if dist_from_end != 0:
            self.pos += to_end.normalize() * move_dist

        if dist_from_end <= self.curr_speed and (next_segment or self.segment.black_hole):
                if self.segment.black_hole:
                    self.kill_train(surface)
                    return
                self.segment = next_segment
                self.dir = "right" if self.segment.dx > 0 else "left" if self.segment.dx < 0 else "up" if self.segment.dy < 0 else "down"
                self.image = pg.transform.rotate(self.original_image, angle[self.segment.vect])
                self.rect = self.image.get_rect(center = self.pos)
        self.rect.center = self.pos

        if tuple(self.pos) in v.station_loc:
            self.time = 200
            self.curr_speed = 0
            return
    
    def kill_train(self, surface):  # odstranění vlaku
        # obrázek exploze
        explosion_pos = self.pos
        explosion_img = pg.image.load("images/vybuch.png").convert_alpha()
        explosion_rect = explosion_img.get_rect(center=explosion_pos)
        surface.blit(explosion_img, explosion_rect)

        self.kill()
        if v.curr_train and self.number == v.curr_train.number:
            v.curr_train = None
        del v.train_set[self.number]
        v.number_of_trains -= 1

# návěstidla
class Light(ImageButton):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y)
        self.rect = self.image.get_rect(topleft = (x, y))
        self.color = "green"

    def click(self, surface):
        image_path = "images/semafory/sg.png"
        if self.color == "green":
            self.color = "red"
            image_path = "images/semafory/sr.png"
        else:
            self.color = "green"
        self.image = pg.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        v.mode = None

# výhybka
class Switch(ImageButton):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y)
        self.dir = "straight"
        self.rect = self.image.get_rect(topleft = (x+16, y + 44))

    def click(self, surface):
        image_path = "images/vyhybky/vr.png"
        if self.dir == "straight":
            self.dir = "turn"
            image_path = "images/vyhybky/vl.png"
        else:
            self.dir = "straight"
        self.image = pg.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        v.mode = None

# ukončení programu
class Exit(Button):
    pass

# domovská obrazovka
class ToHomescreen(Button):
    def click(self, surface):
        from functions import draw_homescreen

        v.game = False
        draw_homescreen(surface)

# výběr mapy
class SelectMap(Button):
    def click(self, surface):
        from functions import draw_selection

        v.game = False
        draw_selection(surface)

# popis ovládání
class Turotial(Button):
    def click(self, surface):
        from functions import draw_tutorial

        v.game = False
        draw_tutorial(surface)

# výběr mapy
class Mapa(ImageButton):
    def __init__(self, image_path, x, y, kind):
        super().__init__(image_path, x, y)
        self.kind = kind
    def click(self, surface):
        from functions import draw_map, read_map, map_to_graph

        v.game = True
        if self.kind == 1:
            read_map("kolejiste1.txt")
            v.povrch = pg.image.load("images/podklady/pozadi1.png").convert_alpha()
        elif self.kind == 2:
            read_map("kolejiste2.txt")
            v.povrch = pg.image.load("images/podklady/pozadi2.png").convert_alpha()
        draw_map(v.mapa, v.povrch, v.lights, v.switches, surface)
        map_to_graph(v.mapa, v.lights, v.switches)
        v.mode = None

# výběr nového vláčku
class SelectTrain(ImageButton):
    def __init__(self, image_path, x, y, kind):
        super().__init__(image_path, x, y)
        self.kind = kind

    def click(self, surface):
        if v.number_of_trains == 9:
            v.mode = "full"
        else:
            v.chosen_train = self.kind
            v.mode = "station"

# výběr výchozího směru
class SelectDirection(Button):
    def click(self, surface):
        from functions import find_segment, find_index
        im = {
            1: "images/vlaky/nakladni2.png",
            2: "images/vlaky/rychlik2.png",
            3:"images/vlaky/parni2.png",
            4: "images/vlaky/elektricka2.png"
        }

        chosen_dir = "right"
        if self.text == "<-":
            chosen_dir = "left"

        index = find_index(v.train_set)
        v.number_of_trains += 1
        segment = find_segment(v.pos, chosen_dir)

        if segment:
            v.train_set[index] = Train(im[v.chosen_train], v.pos, segment, index, chosen_dir)
            v.curr_train = v.train_set[index]
            v.trains.add(v.train_set[index])
            v.mode = None
        else: 
            v.mode = "error"
        print(v.train_set)

# výběr stanice
class SelectStation(Button):
    def click(self, surface):
        tracks = {
            "Plzeň": "p",
            "Nepomuk": "n",
            "Blovice": "b",
            "Šťáhlavy": "s"
        }
    
        v.pos = None
        if v.stations[tracks[self.text]]:
            for position in v.stations[tracks[self.text]]:
                t = pg.Rect(0, 0, 68, 38)
                t.center = position
                if all(not train.rect.colliderect(t) for train in v.trains):
                    v.pos = position
                    break
        if v.pos:
            v.mode = "direction"
        else:
            v.mode = "error"

# odstranění vlaku
class Remove(Button):
    def click(self, surface):
       v.curr_train.kill_train(surface)

# nastavení rychlosti
class Speed(ImageButton):
    def __init__(self, image_path, x, y, kind):
        super().__init__(image_path, x, y)
        self.kind = kind

    def click(self, surface):
            if not v.curr_train:
                return
            i = v.curr_train.number
            if self.kind == 1:
                v.train_set[i].speed += 1
            else:
                if v.train_set[i].speed != 0:
                    v.train_set[i].speed -= 1
            v.train_set[i].curr_speed = v.train_set[i].speed
            v.curr_train.curr_speed = v.train_set[i].speed