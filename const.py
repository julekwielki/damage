import numpy as np
import matplotlib.pyplot as plt
import random
from kom import Cell


def death(a, b):
    return 1/(1 + np.exp(-0.2*(organizm[a][b].passage-60)))


def repair(cell_damages):
    repaired = 0  # naprawione
    non_repaired = 0  # nienaprawione
    for i in range(cell_damages):
        ran = random.random()
        if ran < p3:  # próba naprawy
            ran = random.random()
            if ran < p4:
                repaired += 1  # skuteczna naprawa
            else:
                non_repaired += 1  # błędna naprawa
    return repaired, non_repaired


def damage():
    n_dam = np.random.poisson(uszk)
    onco = 0
    for i in range(n_dam):
        rand = random.random()
        if rand < p_on:
            onco += 1
    return n_dam - onco, onco


nn = 100  # bok tablicy
k = 70  # liczba kroków obecnie każdy krok to ok doby - cykl komórkowy

p3 = 0.95  # próba naprawy jednego uszkodzenia
p4 = 0.9999  # udana naprawa
p0 = 0.05
p_on = 0.01
uszk = 50

organizm = np.ndarray((nn, nn), dtype=object)
dam = np.ones((nn, nn), dtype=float)  # sumaryczne uszkodzenia normalne
dam2 = np.ones((nn, nn), dtype=float)  # sumaryczne uszkodzenia onko

dn, dm, don, dom, da, doa, x7, x8 = 0, 0, 0, 0, 0, 0, 0, 0
norm_dam = []  # średnia liczba uszkodzeń - nie nowych - to znam z poissona
onco_dam = []  # średnia liczba onko uszkodzeń
perm_dam = []  # nowa liczba stałych uszkodzeń
onco_mut = []  # nowa liczba onko mutacji
fixed_dam = []  # średnia liczba naprawionych w danym kroku
fixed_onco = []
new_dam = []
new_onco = []

for x in range(nn):  # wypełnienie tablicy komórkami
    for y in range(nn):
        organizm[x][y] = Cell()

for x in range(nn):
    for y in range(nn):
        organizm[x][y].status = 1
        n_dam = np.random.poisson(uszk)
        onco = 0
        for i in range(n_dam):
            rand = random.random()
            if rand < p_on:
                onco += 1

        organizm[x][y].onco_damage = onco
        organizm[x][y].damage = n_dam - onco
        dam[x][y] = organizm[x][y].damage
        dam2[x][y] = organizm[x][y].onco_damage

"""
result = dam.flatten()
result2 = dam2.flatten()
print("początkowe uszkodzenia\t" + str(np.average(result)))
print("początkowe onko uszkodzenia\t" + str(np.average(result2)))
plt.hist(result)
plt.show()
# """

zapis = [[], [], [], [], [], [], []]
for s in range(k):
    dn, dm, don, dom, da, doa, x7, x8 = 0, 0, 0, 0, 0, 0, 0, 0
    s0, s1, s2, s3 = 0, 0, 0, 0

    for x in range(nn):
        for y in range(nn):
            if organizm[x][y].status == 1:  # normalna komórka
                s1 += 1
                organizm[x][y].passage += 1

                p1 = death(x, y)  # śmierć
                rand = random.random()
                if rand < p1:
                    organizm[x][y].die()

                else:  # uszkodzenia nie zależą od innych procesów i zawsze się zdarzają
                    rep, non_rep = repair(organizm[x][y].damage)
                    organizm[x][y].damage = organizm[x][y].damage - (rep + non_rep)
                    organizm[x][y].perm_damage += non_rep
                    if non_rep:
                        organizm[x][y].status = 2

                    dam[x][y] = organizm[x][y].damage + organizm[x][y].perm_damage  # pomocnicze
                    dn += rep  # pomocnicze
                    dm += non_rep  # pomocnicze

                    rep, non_rep = repair(organizm[x][y].onco_damage)
                    organizm[x][y].onco_damage = organizm[x][y].onco_damage - rep - non_rep
                    organizm[x][y].onco_mut += non_rep

                    if non_rep:
                        organizm[x][y].status = 3

                    dam2[x][y] = organizm[x][y].onco_damage + organizm[x][y].onco_mut  # pomocnicze
                    don += rep  # pomocnicze
                    dom += non_rep  # pomocnicze

                    n_dam, onco = damage()
                    organizm[x][y].onco_damage += onco
                    organizm[x][y].damage += n_dam

                    dam[x][y] += n_dam  # pomocnicze
                    dam2[x][y] += onco  # pomocnicze
                    da += n_dam  # pomocnicze
                    doa += onco  # pomocnicze

            elif organizm[x][y].status == 2:  # normalna komórka
                s2 += 1
                organizm[x][y].passage += 1

                p1 = death(x, y)  # śmierć
                rand = random.random()
                if rand < p1:
                    organizm[x][y].die()

                else:  # uszkodzenia nie zależą od innych procesów i zawsze się zdarzają
                    rep, non_rep = repair(organizm[x][y].damage)
                    organizm[x][y].damage = organizm[x][y].damage - (rep + non_rep)
                    organizm[x][y].perm_damage += non_rep

                    dam[x][y] = organizm[x][y].damage + organizm[x][y].perm_damage  # pomocnicze
                    dn += rep  # pomocnicze
                    dm += non_rep  # pomocnicze

                    rep, non_rep = repair(organizm[x][y].onco_damage)
                    organizm[x][y].onco_damage = organizm[x][y].onco_damage - rep - non_rep
                    organizm[x][y].onco_mut += non_rep

                    if non_rep:
                        organizm[x][y].status = 3

                    dam2[x][y] = organizm[x][y].onco_damage + organizm[x][y].onco_mut  # pomocnicze
                    don += rep  # pomocnicze
                    dom += non_rep  # pomocnicze

                    n_dam, onco = damage()
                    organizm[x][y].onco_damage += onco
                    organizm[x][y].damage += n_dam

                    dam[x][y] += n_dam  # pomocnicze
                    dam2[x][y] += onco  # pomocnicze
                    da += n_dam  # pomocnicze
                    doa += onco  # pomocnicze

            elif organizm[x][y].status == 3:  # normalna komórka
                s3 += 1
                organizm[x][y].passage += 1

                p1 = death(x, y)  # śmierć
                rand = random.random()
                if rand < p1:
                    organizm[x][y].die()

                else:  # uszkodzenia nie zależą od innych procesów i zawsze się zdarzają
                    rep, non_rep = repair(organizm[x][y].damage)
                    organizm[x][y].damage = organizm[x][y].damage - (rep + non_rep)
                    organizm[x][y].perm_damage += non_rep

                    dam[x][y] = organizm[x][y].damage + organizm[x][y].perm_damage  # pomocnicze
                    dn += rep  # pomocnicze
                    dm += non_rep  # pomocnicze

                    rep, non_rep = repair(organizm[x][y].onco_damage)
                    organizm[x][y].onco_damage = organizm[x][y].onco_damage - rep - non_rep
                    organizm[x][y].onco_mut += non_rep

                    dam2[x][y] = organizm[x][y].onco_damage + organizm[x][y].onco_mut  # pomocnicze
                    don += rep  # pomocnicze
                    dom += non_rep  # pomocnicze

                    n_dam, onco = damage()
                    organizm[x][y].onco_damage += onco
                    organizm[x][y].damage += n_dam

                    dam[x][y] += n_dam  # pomocnicze
                    dam2[x][y] += onco  # pomocnicze
                    da += n_dam  # pomocnicze
                    doa += onco  # pomocnicze

            elif organizm[x][y].status == -1:
                s0 += 1
    zapis[0].append(s0)
    zapis[1].append(s1)
    zapis[2].append(s2)
    zapis[3].append(s3)
    zapis[4].append(s1+s2+s3)
    zapis[5].append(s2+s3)
    norm_dam.append(sum(dam.flatten()) / len(dam.flatten()))
    onco_dam.append(sum(dam2.flatten()) / len(dam2.flatten()))

    fixed_dam.append(dn)
    perm_dam.append(dm)
    fixed_onco.append(don)
    onco_mut.append(dom)
    new_dam.append(da / nn**2)
    new_onco.append(doa)

plt.plot(zapis[0], label="martwe")
plt.plot(zapis[1], label="normalne")
plt.plot(zapis[2], label="zmutowane_norm")
plt.plot(zapis[3], label="zmutowane_onk")
plt.plot(zapis[4], label="żywe")
plt.plot(zapis[5], label="zmutowane")
plt.legend()
plt.show()

uhu = []
for x in range(nn):
    for y in range(nn):
        uhu.append(organizm[x][y].passage)

plt.hist(uhu)
plt.show()
"""
result = dam.flatten()
result2 = dam2.flatten()
print("końcowe uszkodzenia\t" + str(np.average(result)))
print("końcowe onko uszkodzenia\t" + str(np.average(result2)))
plt.hist(result)
plt.show()
#"""

"""
plt.plot(norm_dam)
plt.show()
# """
"""
plt.plot(perm_dam, label="perm_dam")
plt.plot(onco_mut, label="onco_mut")
# plt.plot(fixed_dam, label="fixed_dam")
plt.plot(fixed_onco, label="fixed_onco")
plt.plot(new_dam, label="new_dam")
plt.plot(new_onco, label="new_onco")
plt.legend()
plt.show()
# """

# plt.hist(result2)
# plt.show()
