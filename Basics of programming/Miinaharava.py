# Miinaharava
# Made by Aleksi Hytönen

import random
import haravasto as harava
import time
from datetime import datetime

# Kirjasto, joka sisältää pelissä käytettvät muuttujat
tila = {
    "kentta": None,
    "naytto": None,
    "miinat": None,
    "pisteet": None,
    "nimi": None,
    "aika": None,
    "valinnat": None,
    "tulos": None,
    "leveys": None,
    "korkeus": None,
    "paiva": None,
    "kello": None
}

def miinoita(lista, ruudut, miinat):
    """Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin."""
    for i in range(0, miinat):
        koordinaatti = random.choice(ruudut)
        lista[koordinaatti[1]][koordinaatti[0]] = "x"
        ruudut.remove(koordinaatti)
    tila["kentta"] = lista

def pelin_voitto(lista):
    """Funktio tarkistaa, onko pelaaja avannut kaikki mahdolliset ruudut, missä ei ole miinoja.
    Arg.    Lista   = Pelikenttä
    Return  True    = Pelaaja on avannut kaikki ruudut, jossa ei ole miinoja. 
            False   = Pelikentällä on vielä avaamattomia ruutuja, joissa ei ole miinaa."""

    laskuri = 0
    for i in range(0, len(lista[0])):
        for j in range(0, len(lista)):
            if lista[j][i] == " " or lista [j][i] == "f":
                laskuri += 1
    if laskuri == tila["miinat"]:
        return True
    else:
        return False

def kasittele_hiiri(x, y, painike, muokkaus):
    """Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä. 
    Tulostaa hiiren sijainnin sekä painetun napin terminaaliin."""
    loppu = False
    if painike == harava.HIIRI_VASEN:
        tila["valinnat"] += 1
        if tila["kentta"][int(y/40)][int(x/40)] == "x":
            tila["naytto"][int(y/40)][int(x/40)] = "x"
            loppu = True
        else:
            tulvataytto(tila["kentta"], int(x/40), int(y/40))
    elif painike == harava.HIIRI_OIKEA:
        if tila["naytto"][int(y/40)][int(x/40)] == "f":
            tila["naytto"][int(y/40)][int(x/40)] = " "
        elif tila["naytto"][int(y/40)][int(x/40)] == " ":
            tila["naytto"][int(y/40)][int(x/40)] = "f"
    elif painike == harava.HIIRI_KESKI:
        pass
    piirra_kentta()
    if pelin_voitto(tila["naytto"]):
        harava.lopeta()
        tila["aika"] = (time.time() - tila["aika"]) / 60
        tila["tulos"] = "Voitto"
        tallenna()
        print("\nVoitit Pelin! Valinnat: {}, Pisteet: {}, Aika: {:.2f}min\n".format(tila["valinnat"], tila["pisteet"], tila["aika"]))
    if loppu:
        harava.lopeta()
        tila["aika"] = (time.time() - tila["aika"]) / 60
        tila["tulos"] = "Häviö"
        tallenna()
        print("\nHävisit Pelin! Valinnat: {}, Pisteet: {}, Aika: {:.2f}min\n".format(tila["valinnat"], tila["pisteet"], tila["aika"]))

def tallenna():
    """Tallentaa pelin tiedot pelihistoriaan."""

    with open("historia.txt", "a") as kohde:
        kohde.write("Päivämäärä: {pai} Kellonaika: {kel:%H:%M:%S} Pelaaja: {pelaaja} Siirtoja: {siirrot}kpl pisteet: {pis} peliaika: {aik:.2f} tulos: {tul} miinoja: {mii}kpl leveys: {lev} korkeus: {kor}\n".format(pai=tila["paiva"], kel=tila["kello"], pelaaja=tila["nimi"], siirrot=tila["valinnat"], pis=tila["pisteet"], aik=tila["aika"], tul=tila["tulos"], mii=tila["miinat"], lev=tila["leveys"], kor=tila["korkeus"]))
        kohde.close()

def historia():
    """Tulostaa pelihistorian."""

    with open("historia.txt") as luku:
        his = luku.read().splitlines()
        luku.close()
    for i in range(0, len(his)):
        print(his[i])
		
def piirra_kentta():
    """Käsittelijäfunktio, 
    joka piirtää kaksiulotteisena listana kuvatun miinakentän ruudut näkyviin peli-ikkunaan. 
    Funktiota kutsutaan aina kun pelimoottori pyytää ruudun näkymän päivitystä."""
    lista = tila["naytto"]
    harava.tyhjaa_ikkuna()
    harava.piirra_tausta()
    harava.aloita_ruutujen_piirto()
    for i in range(0, len(lista)):
        for j in range(0, len(lista[0])):
            harava.lisaa_piirrettava_ruutu(lista[i][j], j * 40, i * 40)
    harava.piirra_ruudut()
	
def main(tama):
    """Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän."""

    harava.lataa_kuvat("spritet")
    harava.luo_ikkuna(len(tama[0]) * 40, len(tama) * 40)
    harava.aseta_hiiri_kasittelija(kasittele_hiiri)
    harava.aseta_piirto_kasittelija(piirra_kentta)
    tila["aika"] = time.time()
    harava.aloita()
	
def tulvataytto(lista, x, y):
    """Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, 
    että täyttö aloitetaan annetusta x, y -pisteestä."""
    if lista[y][x] == "x":
        pass
    else:
        aloitus = [(x, y)]
        leveys = len(lista)
        korkeus = len(lista[0])
        while not len(aloitus) == 0:
            x, y = aloitus.pop()
            x = int(x)
            y = int(y)
            miinat = laske_ninjat(x, y, lista)
            if miinat > 0:
                tila["naytto"][y][x] = miinat
                tila["pisteet"] += miinat
            else:
                lista[y][x] = "0"
                tila["naytto"][y][x] = "0"
                paikka = sijainti(x, y, leveys, korkeus)
                try:
                    if paikka == "nurkka":
                        if x == 0 and y == 0:
                            if lista[0][1] == " ":
                                aloitus.append((1, 0))
                            for i in range(y, y + 2):
                                if lista[1][i] == " ":
                                    aloitus.append((i, 1))
                        if x == korkeus and y == 0:
                            if lista[0][x - 1] == " ":
                                aloitus.append((x - 1, 0))
                            for i in range(x - 1, x):
                                if lista[1][i] == " ":
                                    aloitus.append((i, 1))
                        if x == 0 and y == leveys:
                            if lista[y][0] == " ":
                                aloitus.append((0, y))
                            for i in range(0, 1):
                                if lista[y][i] == " ":
                                    aloitus.append((i, y))
                        if x == korkeus and y == leveys:
                            if lista[y][x - 1] == " ":
                                aloitus.append((x - 1, y))
                            for i in range(x - 1, x + 1):
                                if lista[y - 1][i] == " ":
                                    aloitus.append((i, y - 1))
                    elif paikka == "laita":
                        if y == 0:
                            if lista[y][x - 1] == " ":
                                aloitus.append((x - 1, y))
                            if lista[y][x + 1] == " ":
                                aloitus.append((x + 1, y))
                            for i in range(x - 1, x + 2):
                                if lista[1][i] == " ":
                                    aloitus.append((i, 1))
                        if x == korkeus:
                            for i in range(x - 1, x + 1):
                                if lista[y - 1][i] == " ":
                                    aloitus.append((i, y - 1))
                            if lista[y][x - 1] == " ":
                                aloitus.append((x - 1, y))
                            for i in range(x - 1, x + 1):
                                if lista[y + 1][i] == " ":
                                    aloitus.append((i, y + 1))
                        if y == leveys:
                            for i in range(x - 1, x + 1):
                                if lista[y - 1][i] == " ":
                                    aloitus.append((i, y - 1))
                            if lista[y][x - 1] == " ":
                                aloitus.append((x - 1, y))
                            if lista[y][x + 1] == " ":
                                aloitus.append((x + 1, y))
                        if x == 0:
                            for i in range(y - 1, y + 2):
                                if lista[i][x + 1] == " ":
                                    aloitus.append((x + 1, i))
                            if lista[y + 1][x] == " ":
                                aloitus.append((x, y + 1))
                            if lista[y - 1][x] == " ":
                                aloitus.append((x, y - 1))
                    elif paikka == "keski":
                        for i in range(x - 1, x + 2):
                            if lista[y - 1][i] == " ":
                                aloitus.append((i, y - 1))
                        if lista[y][x - 1] == " ":
                            aloitus.append((x - 1, y))
                        if lista[y][x + 1] == " ":
                            aloitus.append((x + 1, y))
                        for i in range(x - 1, x + 2):
                            if lista[y + 1][i] == " ":
                                aloitus.append((i, y + 1))
                except IndexError:
                    pass
    tila["kentta"] = lista
		
def sijainti(x, y, korkeus, leveys):
    """Etsii pisteen paikan kentällä.
    Arg.    x       =   Pisteen x-koordinaatti
            y       =   Pisteen y-koordinaatti
            korkeus =   Kentän korkeus
            leveys  =   Kentän leveys
    Return  paikka  =   Pisteen paikka kentällä"""

    if leveys > 0 and korkeus > 0:
        if x == 0 and y == 0:
            paikka = "nurkka"
        elif x == leveys and y == 0:
            paikka = "nurkka"
        elif x == 0 and y == korkeus:
            paikka = "nurkka"
        elif x == leveys and y == korkeus:
            paikka = "nurkka"
        elif x > 0 and x < leveys and y == 0:
            paikka = "laita"
        elif x == 0 and y > 0 and y < korkeus:
            paikka = "laita"
        elif x > 0 and x < leveys and y == korkeus:
            paikka = "laita"
        elif x == leveys and y > 0 and y < korkeus:
            paikka = "laita"
        else:
            paikka = "keski"
    return paikka

def pyyda_syote(jono, virhe):
    """Kysyy käyttäjältä kokonaislukua käyttäen 
    kysymyksenä parametrina annettua merkkijonoa. Virheellisen syötteen 
    kohdalla käyttäjälle näytetään toisena parametrina annettu virheilmoitus. 
    Käyttäjän antama kelvollinen syöte palautetaan kokonaislukuna."""
    while True:
        try:
            arvo = int(input(jono))
        except ValueError:
            print(virhe)
        else:
            break
    return arvo

def muodosta_kentta(leveys, korkeus):
    lista1 = []
    lista2 = []
    for i in range(0, korkeus):
        for j in range(0, leveys):
            lista1.append(" ")
        lista2.append(lista1)
        lista1 = []
    return lista2

def peli():
    """Uuden pelin aloittaminen."""

    lista = []
    tila["pisteet"] = 0
    tila["valinnat"] = 0
    tila["nimi"] = input("Kerro nimesi: ")
    tila["leveys"] = pyyda_syote("Anna kentän leveys kokonaislukuna (Max 20): ", "Virheellinen syöte")
    tila["korkeus"] = pyyda_syote("Anna kentän korkeus kokonaislukuna (Max 20): ", "Virheellinen syöte")
    while True:
        if tila["leveys"] > 20:
            tila["leveys"] = pyyda_syote("Liian leveä kenttä!\nAnna kentän leveys kokonaislukuna (Max 20): ", "Virheellinen syöte")
        elif tila["korkeus"] > 20:
            tila["korkeus"] = pyyda_syote("Liian korkea kenttä!\nAnna kentän korkeus kokonaislukuna (Max 20): ", "Virheellinen syöte")
        else:
            break
    tila["kentta"] = muodosta_kentta(tila["leveys"], tila["korkeus"])
    tila["naytto"] = muodosta_kentta(tila["leveys"], tila["korkeus"])
    tila["paiva"] = time.strftime("%x")
    tila["kello"] = datetime.now()
    maksimi = tila["leveys"] * tila["korkeus"]
    miinat = pyyda_syote("Montako miinaa haluat kentälle?\nVoit maksimissaan sijoittaa {} miinaa kentälle: ".format(maksimi), "Virheellinen syöte")
    while miinat > maksimi or miinat < 0:
        miinat = pyyda_syote("Sijoitit virheellisen määrän miinoja!\nSyötä miinojen määrä uudelleen:  ", "Virheellinen syöte")
    for i in range(0, tila["korkeus"]):
        for j in range(0, tila["leveys"]):
            lista.append((j, i))
    tila["miinat"] = miinat
    miinoita(tila["kentta"], lista, miinat)
    main(tila["naytto"])

def laske_ninjat(x, y, kentta):
    """Laskee annetussa huoneessa yhden ruudun ympärillä olevat ninjat 
    ja palauttaa niiden lukumäärän. 
    Funktio toimii sillä oletuksella, 
    että valitussa ruudussa ei ole ninjaa - jos on, 
    sekin lasketaan mukaan."""
    ninjat = 0
    leveys = len(kentta[0]) - 1
    korkeus = len(kentta) - 1
    paikka = sijainti(x, y, leveys, korkeus)
    if paikka == "nurkka":
        if x == 0 and y == 0:
            if kentta[0][1] == "x":
                ninjat += 1
            for i in range(y, y + 2):
                if kentta[1][i] == "x":
                    ninjat += 1
        if x == leveys and y == 0:
            if kentta[0][x - 1] == "x":
                ninjat += 1
            for i in range(x - 1, x):
                if kentta[1][i] == "x":
                    ninjat += 1
        if x == 0 and y == korkeus:
            if kentta[y][0] == "x":
                ninjat += 1
            for i in range(0, 1):
                if kentta[y][i] == "x":
                    ninjat += 1
        if x == leveys and y == korkeus:
            if kentta[y][x - 1] == "x":
                ninjat += 1
            for i in range(x - 1, x + 1):
                if kentta[y - 1][i] == "x":
                    ninjat += 1
    if paikka == "laita":
        if y == 0:
            if kentta[y][x - 1] == "x":
                ninjat += 1
            if kentta[y][x + 1] == "x":
                ninjat += 1
            for i in range(x - 1, x + 2):
                if kentta[1][i] == "x":
                    ninjat += 1
        if x == leveys:
            for i in range(x - 1, x + 1):
                if kentta[y - 1][i] == "x":
                    ninjat += 1
            if kentta[y][x - 1] == "x":
                ninjat += 1
            for i in range(x - 1, x + 1):
                if kentta[y + 1][i] == "x":
                    ninjat += 1
        if y == korkeus:
            for i in range(x - 1, x + 1):
                if kentta[y - 1][i] == "x":
                    ninjat += 1
            if kentta[y][x - 1] == "x":
                ninjat += 1
            if kentta[y][x + 1] == "x":
                ninjat += 1
        if x == 0:
            for i in range(0, 2):
                if kentta[y - 1][i] == "x":
                    ninjat += 1
            if kentta[y][1] == "x":
                ninjat += 1
            for i in range(0, 2):
                if kentta[y + 1][i] == "x":
                    ninjat += 1
    if paikka == "keski":
        for i in range(x - 1, x + 2):
            if kentta[y - 1][i] == "x":
                ninjat += 1
        if kentta[y][x - 1] == "x":
            ninjat += 1
        if kentta[y][x + 1] == "x":
            ninjat += 1
        for i in range(x - 1, x + 2):
            if kentta[y + 1][i] == "x":
                ninjat += 1
    return ninjat

def aloitus():
    #main

    print("Tervetuloa pelaamaan miinaharavaa!")
    while True:
        print("valitse toiminto:")
        print("1. Aloita peli")
        print("2. Tarkastele tuloksia")
        print("3. Lopeta")
        valinta = pyyda_syote("Syötä valinta ja paina enter: ", "Virheellinen syöte")
        if valinta == 1:
            print("Aloitetaan peli")
            peli()
        elif valinta == 2:
            historia()
        elif valinta == 3:
            print("Kiitos pelaamisesta! Ohjelma suljetaan!")
            break
        else:
            print("Virheellinen syöte!")

if __name__ == "__main__":
    aloitus()