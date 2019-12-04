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

def tyhja(lista):
    for i in lista:
        if i != 0:
            return False
    return True

def etsi_kallein(lista):
    kallein = 0
    solmu = 0
    for index, i in enumerate(lista):
        if i > kallein:
            kallein = i
            solmu = index
    return kallein, solmu
	
def etsi_halvin(lista, halvin):
    umpikuja = True
    solmu = None
    for index, i in enumerate(lista):
        if i <= halvin and i != 0:
            halvin = i
            solmu = index
            umpikuja = False
    if umpikuja:
        return 0, 0
    else:
        return halvin, solmu

def vierailtu(verkko, jono, paikka):
    for i in range(0, len(verkko)):
        verkko[i][paikka] = 0
    for i in range(0, len(jono)):
        jono[i][paikka] = 0
    return verkko, jono

def reitti(verkko, maali):
    maali -= 1
    jono = []
    jono.append(verkko[0])
    kallein, solmu = etsi_kallein(jono[0])
    korkein, paikka = etsi_halvin(jono[-1], kallein)
    kesken = True
    reitti = [1]
    while len(jono) != 0 and kesken:
        solmu = jono[-1]
        halvin, paikka = etsi_halvin(solmu, kallein)
        if paikka == maali and halvin != 0:
            reitti.append(paikka + 1)
            kesken = False
        elif halvin != 0:
            verkko, jono = vierailtu(verkko, jono, paikka)
            if halvin > korkein:
                korkein = halvin
            jono.pop()
            jono.append(solmu)
            jono.append(verkko[paikka])
            reitti.append(paikka + 1)
            print("Kallein: {}".format(kallein))
        elif tyhja(jono[-1]):
            jono.pop()
            reitti.pop()
        else:
            kallein, solmu = etsi_kallein(jono[-1])
            jono[-1][solmu] = 0
        print(jono)
        print(reitti)
        print('---------------------')
    return reitti, korkein
	
def main():
    #with open("./graph_testdata/graph_ADS2018_10_1.txt", "r") as kohde:
    with open("./verkko.txt", "r") as kohde:
      lista = kohde.readlines()
      kohde.close()
    verkko, maali = muodosta_verkko(lista)
    vastaus, kallein = reitti(verkko, int(maali))
    print(vastaus)
    print(kallein)
    
if __name__ == "__main__":
    main()