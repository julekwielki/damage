import numpy as np
import matplotlib.pyplot as plt
import random
from kom import Cell


def death(a):
    return 0 #  1/(1 + np.exp(-0.2*(organizm[a].passage-60)))


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


nn = 1000  # bok tablicy
k = 70  # liczba kroków obecnie każdy krok to ok doby - cykl komórkowy

p3 = 0.95  # próba naprawy jednego uszkodzenia
p4 = 0.999  # udana naprawa
p0 = 0.05
p_on = 0.05
uszk = 5

organizm = np.ndarray(nn, dtype=object)
dam = np.ones(nn, dtype=float)  # sumaryczne uszkodzenia normalne
dam2 = np.ones(nn, dtype=float)  # sumaryczne uszkodzenia onko

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
    organizm[x] = Cell()

for x in range(nn):
    organizm[x].status = 1
    n_dam = np.random.poisson(uszk)
    onco = 0
    for i in range(n_dam):
        rand = random.random()
        if rand < p_on:
            onco += 1

    organizm[x].onco_damage = onco
    organizm[x].damage = n_dam - onco
    dam[x] = organizm[x].damage
    dam2[x] = organizm[x].onco_damage

"""
print("początkowe uszkodzenia\t" + str(np.average(dam)))
print("początkowe onko uszkodzenia\t" + str(np.average(dam2)))
plt.hist(dam)
plt.show()
# """
# """
zapis = [[], [], [], [], [], [], []]
for s in range(k):
    dn, dm, don, dom, da, doa, x7, x8 = 0, 0, 0, 0, 0, 0, 0, 0
    s0, s1, s2, s3 = 0, 0, 0, 0
    if s == 20 or s == 60:
        uszk = 50
    if s == 21 or s == 61:
        uszk = 5
    for x in range(nn):
        if organizm[x].status == 1:  # normalna komórka
            s1 += 1
            organizm[x].passage += 1

            p1 = death(x)  # śmierć
            rand = random.random()
            if rand < p1:
                organizm[x].die()

            else:  # uszkodzenia nie zależą od innych procesów i zawsze się zdarzają
                rep, non_rep = repair(organizm[x].damage)
                organizm[x].damage = organizm[x].damage - (rep + non_rep)
                organizm[x].perm_damage += non_rep
                if non_rep:
                    organizm[x].status = 2

                dam[x] = organizm[x].damage + organizm[x].perm_damage  # pomocnicze
                dn += rep  # pomocnicze
                dm += non_rep  # pomocnicze

                rep, non_rep = repair(organizm[x].onco_damage)
                organizm[x].onco_damage = organizm[x].onco_damage - rep - non_rep
                organizm[x].onco_mut += non_rep

                if non_rep:
                    organizm[x].status = 3

                dam2[x] = organizm[x].onco_damage + organizm[x].onco_mut  # pomocnicze
                don += rep  # pomocnicze
                dom += non_rep  # pomocnicze

                n_dam, onco = damage()
                organizm[x].onco_damage += onco
                organizm[x].damage += n_dam

                dam[x] += n_dam  # pomocnicze
                dam2[x] += onco  # pomocnicze
                da += n_dam  # pomocnicze
                doa += onco  # pomocnicze

        elif organizm[x].status == 2:  # normalna komórka
            s2 += 1
            organizm[x].passage += 1

            p1 = death(x)  # śmierć
            rand = random.random()
            if rand < p1:
                organizm[x].die()

            else:  # uszkodzenia nie zależą od innych procesów i zawsze się zdarzają
                rep, non_rep = repair(organizm[x].damage)
                organizm[x].damage = organizm[x].damage - (rep + non_rep)
                organizm[x].perm_damage += non_rep

                dam[x] = organizm[x].damage + organizm[x].perm_damage  # pomocnicze
                dn += rep  # pomocnicze
                dm += non_rep  # pomocnicze

                rep, non_rep = repair(organizm[x].onco_damage)
                organizm[x].onco_damage = organizm[x].onco_damage - rep - non_rep
                organizm[x].onco_mut += non_rep

                if non_rep:
                    organizm[x].status = 3

                dam2[x] = organizm[x].onco_damage + organizm[x].onco_mut  # pomocnicze
                don += rep  # pomocnicze
                dom += non_rep  # pomocnicze

                n_dam, onco = damage()
                organizm[x].onco_damage += onco
                organizm[x].damage += n_dam

                dam[x] += n_dam  # pomocnicze
                dam2[x] += onco  # pomocnicze
                da += n_dam  # pomocnicze
                doa += onco  # pomocnicze

        elif organizm[x].status == 3:  # normalna komórka
            s3 += 1
            organizm[x].passage += 1

            p1 = death(x)  # śmierć
            rand = random.random()
            if rand < p1:
                organizm[x].die()

            else:  # uszkodzenia nie zależą od innych procesów i zawsze się zdarzają
                rep, non_rep = repair(organizm[x].damage)
                organizm[x].damage = organizm[x].damage - (rep + non_rep)
                organizm[x].perm_damage += non_rep

                dam[x] = organizm[x].damage + organizm[x].perm_damage  # pomocnicze
                dn += rep  # pomocnicze
                dm += non_rep  # pomocnicze

                rep, non_rep = repair(organizm[x].onco_damage)
                organizm[x].onco_damage = organizm[x].onco_damage - rep - non_rep
                organizm[x].onco_mut += non_rep

                dam2[x] = organizm[x].onco_damage + organizm[x].onco_mut  # pomocnicze
                don += rep  # pomocnicze
                dom += non_rep  # pomocnicze

                n_dam, onco = damage()
                organizm[x].onco_damage += onco
                organizm[x].damage += n_dam

                dam[x] += n_dam  # pomocnicze
                dam2[x] += onco  # pomocnicze
                da += n_dam  # pomocnicze
                doa += onco  # pomocnicze

        elif organizm[x].status == -1:
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
        uhu.append(organizm[x].passage)

plt.hist(uhu)
# plt.show()
# """

"""
print("końcowe uszkodzenia\t" + str(np.average(dam)))
print("końcowe onko uszkodzenia\t" + str(np.average(dam2)))
plt.hist(dam)
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

"""
plt.figure(1)
plt.hist(dam2)
plt.figure(2)
plt.hist(dam)
plt.show()

dammm = []
for x in dam2:
    if x > 0:
        dammm.append(x)

plt.hist(dam2)  # , bins=[0,1,2,3,4,5,6,7,8,9,10])
plt.show()

dammm = []
for x in range(len(dam2)):
    if dam2[x] > 0:
        dammm.append(dam2[x]/(dam[x]+dam2[x]))

plt.hist(dammm)
plt.show()
"""
