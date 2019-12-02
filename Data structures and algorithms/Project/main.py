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

def etsi_kallein(lista):
    kallein = 0
    for i in lista:
        if i > kallein:
            kallein = i
    return kallein
	
def etsi_halvin(lista):
    halvin = etsi_kallein(lista)
    solmu = None
    for index, i in enumerate(lista):
        if i < halvin and i != 0:
            halvin = i
            solmu = index
    return halvin, solmu

def reitti(verkko, maali):
    maali -= 1
    jono = []
    jono.append(verkko.pop(0))
    halvin, solmu = etsi_halvin(jono[0])
    return halvin, solmu
	
def main():
    with open("./verkko.txt", "r") as kohde:
      lista = kohde.readlines()
      kohde.close()
    verkko, maali = muodosta_verkko(lista)
    vastaus, solmu = reitti(verkko, int(maali))
    print(vastaus)
    print(solmu)
    
if __name__ == "__main__":
    main()