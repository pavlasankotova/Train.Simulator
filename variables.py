from pygame.sprite import Group

# aktuální stav hry
mode = None

# mapa
mapa = None
lights = {}
switches = {}
povrch = None
game = False

# uvedení nového vláčku do mapy
chosen_train = None
pos = None

# vláčky a skupiny vláčku
curr_train = None
trains = Group()
train_set = {}
number_of_trains = 0

# koleje u nádraží
stations = {
        "p": [],
        "n": [],
        "b": [],
        "s": []
    }

station_loc = set()

# úseky trati
segments = {}