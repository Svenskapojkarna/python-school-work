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
	
def etsi_halvin(lista, halvin):
    umpikuja = True
    solmu = None
    for index, i in enumerate(lista):
        if i < halvin and i != 0:
            halvin = i
            solmu = index
            umpikuja = False
    if umpikuja:
        return 0, 0
    else:
        return halvin, solmu

def reitti(verkko, maali):
    maali -= 1
    jono = []
    jono.append(verkko.pop(0))
    kallein = etsi_kallein(jono[0])
    kesken = True
    while len(jono) != 0 and kesken:
        solmu = jono[-1]
        halvin, paikka = etsi_halvin(solmu, kallein)
        if paikka == maali and halvin != 0:
            kesken = False
        elif halvin != 0:
            solmu[paikka] = 0
            kallein = halvin
            jono.pop()
            jono.append(solmu)
            jono.append(verkko[paikka])
        else:
            # Tänne taaksepäin meneminen
    return solmu
	
def main():
    with open("./verkko.txt", "r") as kohde:
      lista = kohde.readlines()
      kohde.close()
    verkko, maali = muodosta_verkko(lista)
    vastaus = reitti(verkko, int(maali))
    print(vastaus)
    
if __name__ == "__main__":
    main()