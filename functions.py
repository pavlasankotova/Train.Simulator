import pygame as pg
from classes import *
from objects import *
import variables as v

# dlaždice pro vykreslování
tiles = {
    "home": pg.image.load("images/home_screen.png"),
    "4": pg.image.load("images/koleje/z4.png"),
    "=": pg.image.load("images/koleje/r.png"),
    "3": pg.image.load("images/koleje/z3.png"),
    "+": pg.image.load("images/koleje/k.png"),
    "|": pg.image.load("images/koleje/s.png"),
    "2": pg.image.load("images/koleje/z2.png"),
    "1": pg.image.load("images/koleje/z1.png"),
    "P": pg.image.load("images/nadrazi/plzen.png"),
    "p": pg.image.load("images/koleje/r.png"),
    "B": pg.image.load("images/nadrazi/blovice.png"),
    "b": pg.image.load("images/koleje/r.png"),
    "S": pg.image.load("images/nadrazi/stahlavy.png"),
    "s": pg.image.load("images/koleje/r.png"),
    "N": pg.image.load("images/nadrazi/nepomuk.png"),
    "n": pg.image.load("images/koleje/r.png"),
    "W": pg.image.load("images/krajinky/S1.png"),
    "w": pg.image.load("images/krajinky/s.png"),
    "5": pg.image.load("images/koleje/v5.png"),
    "6": pg.image.load("images/koleje/v6.png"),
    "7": pg.image.load("images/koleje/v7.png"),
    "8": pg.image.load("images/koleje/v8.png"),
    "a": pg.image.load("images/koleje/va.png"),
    "k": pg.image.load("images/krajinky/k.png"),
    "K": pg.image.load("images/krajinky/K1.png"),
    "r": pg.image.load("images/krajinky/r.png"),
    "J": pg.image.load("images/krajinky/J1.png"),
    "j": pg.image.load("images/krajinky/j.png"),
    "T": pg.image.load("images/krajinky/T.png"),
}

# tlačítka, která lze zmáčknout
can_press = []

# vyhreslení domovské obrazovky
def draw_homescreen(surface):
    from objects import homescreen_buttons
    global can_press

    home_screen = tiles["home"]
    surface.blit(home_screen, (0, 0))
    for button in homescreen_buttons:
        button.draw(surface)
    can_press = homescreen_buttons
    return can_press

# vykreslení nápovědy
def draw_tutorial(surface):
    from objects import tutorial_buttons, tut_can_click
    global can_press

    surface.fill((220, 215, 200))
    for button in tutorial_buttons:
        button.draw(surface)
    can_press = tut_can_click
    return can_press

# vykreslení výběru map
def draw_selection(surface):
    from objects import selection_buttons, sel_can_click
    global can_press

    surface.fill((220, 215, 200))
    for button in selection_buttons:
        button.draw(surface)
    can_press = sel_can_click
    return can_press

# načtení souboru s mapou
def read_map(soubor):
    v.mapa = []
    v.trains = Group()
    v.train_set = {}
    v.number_of_trains = 0
    v.stations = {
        "p": [],
        "n": [],
        "b": [],
        "s": []
    }
    v.segments = {}
    v.lights = {}
    v.switches = {}

    with open(soubor, "r") as op:
        lines = op.readlines()
        for i, radek in enumerate(lines):
            r = []  # řádek mapy
            for j, znak in enumerate(radek.rstrip("\n")):
                r.append(znak)
                if znak == ":":
                    v.lights[(i, j)] = Light("images/semafory/sg.png", j * 64, i * 64)
                if znak == "v":
                    v.switches[(i, j)] = Switch("images/vyhybky/vr.png", j * 64, i * 64)
            v.mapa.append(r)
    return

# kontrola souřadnic
def is_in_map(x, y, mapa):
   return 0 <= x < len(mapa) and 0 <= y < len(mapa[0])

# uložení mapy do grafu
def map_to_graph(mapa, lights, switches):
    from classes import Segment
    nodes = {}
    
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if mapa[i][j] in "pnbs+12345678a":
                nodes[(j, i)] = {
                    "pos": (64*j + 32, 64*i + 32),
                }
                if mapa[i][j] in "pbns":
                    v.stations[mapa[i][j]].append(nodes[(j, i)]["pos"])
                    v.station_loc.add(nodes[(j, i)]["pos"])

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    track_for_dir = {
        (1, 0): "=", (-1, 0): "=",
        (0, 1): "|", (0, -1): "|"
    }

    direct_for_tracks = {
        "1": {(1, 0), (0, -1)},
        "2": {(-1, 0), (0, -1)},
        "3": {(-1, 0), (0, 1)},
        "4": {(1, 0), (0, 1)},
        "s": {(1, 0), (-1, 0)}, "p": {(1, 0), (-1, 0)}, "b": {(1, 0), (-1, 0)}, "n": {(1, 0), (-1,0)},
        "5": {(-1, 0), (0, -1), (0, 1)}, "6": {(-1, 0), (0, -1), (1, 0)}, "7": {(1, 0), (0, -1), (0, 1)}, "8": {(-1, 0), (0, -1), (1, 0)}, "a":{(1, 0), (0, -1), (0, 1)},
        "+": {(1, 0), (-1, 0), (0, 1), (0, -1)}
    }

    for node in nodes:
        for dir in directions:
            expected = track_for_dir[dir]
            if  dir in direct_for_tracks[mapa[node[1]][node[0]]]:
                new = node
                while is_in_map(new[1] + dir[1], new[0] + dir[0], mapa) and mapa[new[1] + dir[1]][new[0] + dir[0]] in expected:
                    new = (new[0] + dir[0], new[1] + dir[1])
                if not is_in_map(new[1] + dir[1], new[0] + dir[0], mapa):
                    continue
                new = (new[0] + dir[0], new[1] + dir[1])

                if new != node:
                    segment_switch = None
                    segment_light = None
                    black_hole = True
                    if new in nodes and  (-dir[0], -dir[1]) in direct_for_tracks[mapa[new[1]][new[0]]]:
                        black_hole = False
                        check_light = (1, 1)
                        if new[0] - node[0] > 0 or new[1] - node[1] > 0:
                            check_light = (-1, -1)
                        x = node[1] + check_light[1]
                        y = node[0] + check_light[0]
                        if is_in_map(x, y, mapa) and mapa[x][y] == ":":
                            segment_light = lights[(x, y)]
                    for dir in [(1, -1), (-1, -1), (1, 0), (-1, 0)]:
                        if mapa[node[1]][node[0]] in "5678a" and is_in_map(node[1] + dir[1], node[0] + dir[0], mapa) and mapa[node[1] + dir[1]][node[0] + dir[0]] == "v":
                            segment_switch = switches[(node[1] + dir[1], node[0] + dir[0])]
                            break
                    start_pos = nodes[node]["pos"]
                    end_pos   = (new[0]*64 + 32, new[1]*64 + 32)
                    seg = Segment(start_pos, end_pos, end_pos[0] - start_pos[0], end_pos[1] - start_pos[1], segment_light, segment_switch)
                    if black_hole:
                        seg.black_hole = True
                    if not nodes[node]["pos"] in v.segments:
                        v.segments[nodes[node]["pos"]] = []
                    v.segments[nodes[node]["pos"]].append(seg)

# vykreslení herní plochy
# ovládací panel
def draw_controlpanel(surface):
    global can_press
   
    pg.draw.rect(surface, (220, 215, 200), (896, 0, 384, 896))
    for button in game_buttons:
        button.draw(surface)

    if v.curr_train:    # zobrazení rychlosti
        speed_text = f"{v.curr_train.speed*12}"
        Button("Rychlost vlaku:", 959, 588, 160, 20, (220, 215, 200), "black", 12).draw(surface)
        Button(speed_text + " km/h", 955, 618, 140, 20, (220, 215, 200), "black").draw(surface)
        for button in curr_buttons:
            button.draw(surface)
        can_press.extend(curr_buttons)

# vykreslení mapy
def draw_map(mapa, pozadi, lights, switches, surface):
    surface.blit(pozadi, (0,0))    # pozadí železnice

    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            znak = mapa[i][j]
            if znak in tiles:
                picture = tiles[znak]
                surface.blit(picture, (j * 64, i * 64))

    for light in lights.values():
        light.draw(surface)
    for switch in switches.values():
        switch.draw(surface)


# výběr výchozího směru
def select_direction(surface):
    global can_press
    from objects import direction_buttons

    for button in direction_buttons:
        button.draw(surface)


# výběr výchozícho nádraží
def select_station(surface):
    global can_press
    from objects import station_buttons

    for button in station_buttons:
        button.draw(surface)


# stav hry a vykreslení
def game_mode_draw(surface):
    global can_press

    can_press = list(game_can_click)
    
    can_press.extend([light for light in v.lights.values()])
    can_press.extend([switch for switch in v.switches.values()])

    draw_map(v.mapa, v.povrch, v.lights, v.switches, surface)   # vykreslení mapy
    draw_controlpanel(surface)  # vykreslení ovládacího panelu

    if v.mode == "direction":
        can_press.extend(direction_can_click)
        select_direction(surface)
    elif v.mode == "station":
        can_press.extend(station_buttons)
        select_station(surface)
    elif v.mode == "error":
        Button("Nádraží není", 896, 500, 384, 60,(220, 215, 200), "black", 18).draw(surface)
        Button("dostupné,", 896, 560, 384, 60,(220, 215, 200), "black", 18).draw(surface)
        Button("zvol jiné", 896, 620, 384, 60,(220, 215, 200), "black", 18).draw(surface)
    elif v.mode == "full":
        pg.draw.rect(surface, (220, 215, 200), (896, 500, 384, 896))
        Button("Kolejiště", 896, 500, 384, 60,(220, 215, 200), "black", 18).draw(surface)
        Button("je plné", 896, 560, 384, 60,(220, 215, 200), "black", 18).draw(surface)
    
    # pohyb a vykresleni vlaků
    v.trains.update(surface)
    if v.curr_train:
        pg.draw.circle(surface, "blue", v.curr_train.pos, 24)
    v.trains.draw(surface)
    train_collision(v.train_set, surface)

    return can_press

# nalezení volného indexu v seznam
def find_index(list):
    for j in range(9):
        if j not in v.train_set:
            return j
    return None
        
# nalezení správného segmentu pro start vlaku
def find_segment(pos, dir):
    segments = v.segments.get(pos)
    if segments:
        for i in segments:
            if i.dx < 0 and dir == "left":
                return i
            elif i.dx > 0 and dir == "right":
                return i
            elif i.dy < 0 and dir == "up":
                return i
            elif i.dy > 0 and dir == "down":
                return i
    return None

    
vyhybky = {
    "5": [(0, -1), (0, 1), (1, 0), (-1, 0)],
    "6": [(1, 0), (-1, 0), (0, 1), (0, -1)],
    "7": [(0, -1), (0, 1), (-1, 0), (1, 0)],
    "8": [(-1, 0), (1, 0), (0, 1), (0, -1)],
    "a": [(0, 1), (0, -1), (-1, 0), (1, 0)]
}

# nalezení následujícího segmentu
def find_new_segment(pos, ex, dir):
    from pygame.math import Vector2
    global vyhybky

    if isinstance(pos, Vector2):
        pos = (pos.x, pos.y)
    elif isinstance(pos, list):
        pos = tuple(pos)

    segments = v.segments.get(pos)
    if not segments:
        return None
    for seg in segments:
        directions = {
            "down": (0, 1),
            "up": (0, -1),
            "right": (1, 0),
            "left": (-1, 0)
        }

        if seg.switch:
            smery = vyhybky[v.mapa[(pos[1]-32)//64][(pos[0]-32)//64]]
            if directions[dir] == smery[0] and ((seg.switch.dir == "straight" and seg.vect != smery[0]) or (seg.switch.dir == "turn" and seg.vect != smery[3])):
                continue
            elif (directions[dir] == smery[1] and (seg.switch.dir != "straight" or seg.vect != smery[1])) or (directions[dir] == smery[2] and (seg.switch.dir != "turn" or seg.vect != smery[1])):
                continue
        elif v.mapa[(pos[1]-32)//64][(pos[0]-32)//64] == "+":
            if seg.dx == 0 and (dir == "right" or dir == "left"):
                continue
            elif seg.dy == 0 and (dir == "up" or dir == "down"):
                continue
        if seg.e != ex:
            if not seg.light or seg.light.color == "green":
                return seg
    return None

# kolize vlaků
def train_collision(trains, surface):
    collide = set()
    for train in trains.values():
        for j in trains.values():
            if train.number != j.number and train.rect.colliderect(j.rect):
                for i in {train, j}:
                    collide.add(i)
    for t in collide:
        t.kill_train(surface)