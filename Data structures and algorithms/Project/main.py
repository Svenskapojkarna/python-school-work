def muodosta_verkko(lista):
    rivi = lista[0].rstrip().split()
    kaupungit = int(rivi[0])
    verkko = nollaverkko(kaupungit)
    maali = lista[len(lista) - 1]
    for i in range(1, len(lista) - 1):
        rivi = lista[i].rstrip().split()
        verkko[int(rivi[0]) - 1][int(rivi[1]) - 1] = int(rivi[2])
    verkko.pop()
    return verkko, maali

def nollaverkko(pituus):
    nolla = []
    rivi = []
    for i in range(0, pituus):
        for j in range(0, pituus):
            rivi.append(0)
        nolla.append(rivi)
        rivi = []
    return nolla

def etsi_halvin(halvin, lista):
    solmu = 0
    for j, i in enumerate(lista):
        if i == 0:
            pass
        elif i < halvin:
            halvin = i
            solmu = j
    if solmu > 0:
        return solmu, halvin
    else:
        return None, 1000
	
def naapurit(lista):
    for i in lista:
        if i != 0:
            return False
    return True

def reitti(verkko, maali):
    maali -= 1
    halvin = 1000
    solmu = 0
    korkein = 0
    reitti = [1]
    edellinen = []
    lista = []
    while solmu != maali:
        if reitti[-1] != solmu + 1:
            reitti.append(solmu + 1)
        lista = verkko[solmu]
        while naapurit(lista) and len(edellinen) > 0:
            solmu = edellinen.pop()
            lista = verkko[solmu]
        seuraava, halvin = etsi_halvin(halvin, lista)
        if halvin == 1000:
            if len(edellinen) > 0:
                solmu = edellinen.pop()
            reitti.pop()
        else:
            if halvin > korkein:
                korkein = halvin
            verkko[solmu][seuraava] = 0
            edellinen.append(solmu)
            solmu = seuraava
    reitti.append(maali + 1)
    return reitti, korkein
	
def main():
    with open("./verkko.txt", "r") as kohde:
      lista = kohde.readlines()
      kohde.close()
    verkko, maali = muodosta_verkko(lista)
    vastaus, korkein = reitti(verkko, int(maali))
    print(vastaus)
    print(korkein)
    

if __name__ == "__main__":
    main()