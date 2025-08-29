# Dokumentace - Železniční simulátor

## Zadání problému

Cílem projektu je vytvořit simulátor železničního provozu, ve kterém hráč může spravovat vlaky, návěstidla a výhybky na přednastavených mapách.
Program má umožnit:
- výběr mapy kolejiště
- přidání a ovládání až 9 vlaků na jedné železnici (+ výběr výchozí stanice a směru pro každý z nich, popř. jejich odstranění)
- ruční přepínání výhybek a návěstidel
- vykreslení aktuálního stavu železnice a vlaků
- detekci kolize nebo vykolejení vlaku

## Uživatelská část

### Spuštění programu

Program se spouští souborem main.py.
Po spuštění se zobrazí domovská obrazovka se třemi tlačítky:
- "Výběr mapy" - otevře seznam dostupných map
- "Ovládání" - přesměruje uživatele k nápovědě pro ovládání
- "Ukončit program" - ukončí program

### Výběr mapy

Uživatel zvolí jednu ze dvou přednastavených map kliknutím na obrázek levým tlačítkem myši.
Následně se načte a zobrazí mapa kolejiště se všemi objekty.

### Přidání vlaku

Hráč zvolí kliknutím na ikonu jednoho ze 4 vláčků typ vlaku, který chce do kolejiště umístit.
Následně se rozbalí nabídka nádraží, znichž kliknutím na název vybere hráč výchozí pozici pro nový vlak.
Jednomu nádraží může příslušet více kolejí, potom je vlak umístěn na první volnou.
Poté je vlaku přiřazen počateční směr. Rychlost soupravy je ve chvíli přidání nulová.

### Ovládání vlaků

Ovládaný vlak je označen modrým kruhem. Rychlost tohoto vlaku je možné zvýšit nebo snížit šipkami na ovládacím panelu vpravo.
Označený vlak lze odstranit z kolejiště.

Ostatní vláčky jsou řízeny signalizací návěstidel a výhybkami. Označit je lze kliknutím na jejich ikonu.
Nově přidaný vlak je označen automaticky.

### Návěstidla a výhybky

Hráč ručně přepíná signál návěstidla (zelená - volno, červená - vlak se zastaví).
Vlaky jedoucí zleva nebo shora jsou řízeny návěstidlem vlevo nahoře od křižovatky, vlaky ze zbylých směrů návěstidlem vpravo dole.

Obdobně jsou ručně přepínány výhybky. Ikona výhybky se vždy nachází nahoře, popř. vedle od příslušné koleje.
Pokud výhybka směřije doprava, je nastavěn přímý směr, v opačném případě je aktivní odbočka.
Výhybka má vždy jeden směr hlavní (oběma směry se dá jet), a dva vedlejší (dá se jet jen jedním směrem).

### Nehody

Pokud dojde ke srážce vlaků, případně k vykolejení vlaku, všichni účastníci incidentu jsou odstraněni z mapy.

## Programátorská část

Projekt je rozdělen do několika modulů (main.py, functions.py, classes.py, objects.py, variables.py), z nichž má každý svou funkci:
- main.py - spouštěcí soubor programu (inicializace hlavního okna, nastavení FPS, řídí hlavní smyčku hry)
- functions.py - logika vykreslování, načítání map a pohybu vlaků (úlohy jednotlivých funkcí vysvětleny přímo v souboru)
- classes.py - definuje ojektové třídy (Button a ImageButton)
- objects.py - definuje konkrétní tlačítka pro všechny fáze hry
- variables.p - obsahuje globální proměnné

### Použité datové struktury a algoritmy

Graf mapy
- mapy železnic (kolejiste1.txt, kolejiste2.txt) jsou uloženy jako textové soubory. Při spuštění příslušné mapy se ukládají do matice a následně se převádejí na graf
- uzly representují stanice, výhybky, zatáčky a křižovatky, hrany jsou tvořeny úseky vodorovných či svislých kolejí
- graf slouží jako podklad pro pohyb vlaků

Objektové třídy
- jsou definovány obecné třídy Button a ImageButton (tlačítka textová a obrázková) a další třídy od nich odvozené (dědí jejich metody a  atributy, popř. realizuje další)
- interaktivní prvky železnice a její segmenty jsou implementovány jako samostatné třídy (Switch a Light jsou odvozené z ImageButton):
    Train - vlaky,
    Segment - segment trati,
    Switch - výhybky,
    Light - návěstidla.
- každý objekt si uchovává svůj stav, díky čemuž se uskutečňuje interakce mezi objekty

Soubory objektů 
- vlaky jsou ukládány slovníku a pygame.sprite.Group(), což usnadňnuje jejich pohyb a vykreslování

Parsování mapy
- kolejiště je načítano z externího textového souboru
- na základě použitých znaků se vytvářejí odpovídající objekty
