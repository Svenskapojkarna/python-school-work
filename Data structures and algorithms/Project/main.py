def muodosta_verkko(lista):
    rivi = lista[0].rstrip().split()
    kaupungit = int(rivi[0])
    tiet = int(rivi[1])
    valit = nollaverkko(kaupungit)
    verkko = []
    for i in range(1, kaupungit):
      for j in range(1, tiet + 1):
        solmu = lista[j].rstrip().split()
        if int(solmu[0]) == i:
          valit[int(solmu[1]) - 1] = int(solmu[2])
      verkko.append(valit)
      valit = nollaverkko(kaupungit)
    maali = lista[len(lista) - 1]
    return verkko, maali

def nollaverkko(pituus):
    nolla = []
    for i in range(0, pituus):
        nolla.append(0)
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
    edellinen = []
    lista = []
    while solmu != maali:
        print(solmu + 1)
        lista = verkko[solmu]
        while naapurit(lista):
            solmu = edellinen.pop()
            lista = verkko[solmu]
        edellinen.append(solmu)
        print(lista)
        seuraava, halvin = etsi_halvin(halvin, lista)
        if seuraava == None:
            solmu = edellinen.pop()
        else:
            verkko[solmu][seuraava] = 0
            solmu = seuraava
    return "Found it!"
	
def main():
    with open("verkko.txt", "r") as kohde:
      lista = kohde.readlines()
      kohde.close()
    verkko, maali = muodosta_verkko(lista)
    print(reitti(verkko, int(maali)))
    

if __name__ == "__main__":
    main()