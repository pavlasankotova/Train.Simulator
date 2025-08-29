from classes import *

# domovská obrazovka:
select_map = SelectMap("Výběr mapy", 240, 380, 570, 110, (220, 215, 200), "black", 36)
tutorial = Turotial("Ovládání", 240, 494, 570, 110, (220, 215, 200),"black", 36)
exit_homescreen = Exit("Ukončit program", 240, 608, 570, 110, (220, 215, 200), "black", 36)

homescreen_buttons = [select_map, tutorial, exit_homescreen]

# nápověda:
title_tutorial = Button("Ovládání:", 355, 16.5, 570, 110, (220, 215, 200), "black")
line1 = Button("Hráč si nejprve zvolí libovolnou mapu. Kliknutím na ikonu vláčku přidá", 355, 144, 570, 40, (220, 215, 200), "black",15)
line2 = Button("zvolený vlak, pro nějž vybere výchozí nádraží a směr.", 355, 184, 570, 40, (220, 215, 200), "black", 15)
line3 = Button("Na trati může být najednou až 9 vláčků. Hráč označenému vlaku může", 355, 224, 570, 40, (220, 215, 200), "black", 15)
line4 = Button("libovolně měnit rychlost nebo ho odstranit. K označení vlaku dojde", 355, 264, 570, 40, (220, 215, 200), "black", 15)
line5 = Button("přidáním nového vlaku na železnici, nebo kliknutím na jiný vlak v kolejišti.", 355, 304, 570, 40, (220, 215, 200), "black", 15)
line6 = Button("Označený vlak je ovládán hráčem, ostatní se řídí signalizací na trati.", 355, 344, 570, 40, (220, 215, 200), "black", 15)
line7 = Button("Tu ale spravuje uživatel, musí mít tedy železnici pod neustálou kontrolou.", 355, 384, 570, 40, (220, 215, 200), "black", 15)
line8 = Button("Signalizaci změní kliknutím na ikonu návěstidla, podobně přehodí výhybku.", 355, 424, 570, 40, (220, 215, 200), "black", 15)
line9 = Button("Výhybky se nachází vždy nahoře (vpravo či vlevo), popř. vedle od příslušné", 355, 464, 570, 40, (220, 215, 200), "black", 15)
line10 = Button("koleje. Semafory pro vlaky jedoucí zleva či shora se nacházejí vlevo nahoře", 355, 504, 570, 40, (220, 215, 200), "black", 15)
line11 = Button("od křižovatky, pro zbylé směry vpravo dole.", 355, 544, 570, 40, (220, 215, 200), "black", 15)
line12 = Button("Při kolizi vlaků nebo vykolejení jsou všichni účastníci nehody odstraněni.", 355, 584, 570, 40, (220, 215, 200), "black", 15)
back_tutorial = ToHomescreen("Zpět na hlavní menu", 50, 641.5, 570, 110, (220, 215, 200), "black")
exit_tutorial = Exit("Ukončit program", 660, 641.5, 570, 110, (220, 215, 200), "black")

tutorial_buttons = [title_tutorial, line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12, back_tutorial, exit_tutorial]
tut_can_click = [back_tutorial, exit_tutorial]

# výběr mapy:
title_selection = Button("Výběr mapy:", 355, 16.5, 570, 110, (220, 215, 200), "black")
map1 = Mapa("images/mapa1.png", 85, 128, 1)
map2 = Mapa("images/mapa2.png", 683, 128, 2)
back_selection = ToHomescreen("Zpět na hlavní menu", 50, 641.5, 570, 110, (220, 215, 200), "black")
exit_selection = Exit("Ukončit program", 660, 641.5, 570, 110, (220, 215, 200), "black")

selection_buttons = [title_selection, map1, map2, back_selection, exit_selection]
sel_can_click = [map1, map2, back_selection, exit_selection]

# ovládací panel:
homepage = ToHomescreen("Menu", 896, 10, 384, 40, (220, 215, 200), "black", 12)
selection = SelectMap("Výběr mapy", 896, 50, 384, 40, (220, 215, 200), "black", 12)
exit = Exit("Ukončit", 896, 90, 384, 40, (220, 215, 200), "black", 12)
select_train = Button("Nový vláček:", 896, 130, 384, 60, (220, 215, 200), "black", 18)
train1 = SelectTrain("images/vlaky/nakladni1.png", 943.2, 190, 1)
train2 = SelectTrain("images/vlaky/rychlik1.png", 1027.4, 190, 2)
train3 = SelectTrain("images/vlaky/parni1.png", 1111.6, 190, 3)
train4 = SelectTrain("images/vlaky/elektricka1.png", 1195.8, 190, 4)


game_buttons = [homepage, selection, exit, select_train, train1, train2, train3, train4]
game_can_click = [homepage, selection, exit, train1, train2, train3, train4]

# výběr směru
left = SelectDirection("<-", 896, 260, 192, 60, (220, 215, 200), "black", 18)
right = SelectDirection("->", 1088, 260, 192, 60, (220, 215, 200), "black", 18)
vyber = Button("Zvol počáteční směr", 896, 320, 384, 20, (220, 215, 200), "black", 12)

direction_buttons = [left, right, vyber]
direction_can_click = [right, left]

# výběr výchozího nádraží:
plzen = SelectStation("Plzeň", 896, 260, 384, 60, (220, 215, 200), "black", 18)
nepomuk = SelectStation("Nepomuk", 896, 320, 384, 60, (220, 215, 200), "black", 18)
blovice = SelectStation("Blovice", 896, 380, 384, 60, (220, 215, 200), "black", 18)
stahlavy = SelectStation("Šťáhlavy", 896, 440, 384, 60,(220, 215, 200), "black", 18)

station_buttons = [plzen, nepomuk, blovice, stahlavy]

# zvýšení a snížení rychlosti:
but1 = Remove("Odstranit vlak", 922, 513, 300, 20, (220, 215, 200), "black", 18)
but4 = Speed("images/sipky/up.png", 1168.8, 565, 1)
but5 = Speed("images/sipky/down.png",1168.8, 634, 2)

curr_buttons = [but1, but4, but5]