import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

najlepsze = {
    "odstep": 0,
    "odstepLiczba": 0,
    "przekatna": 0,
    "otworyRzad": 0,
    "otworyWszystkie": 0,
    "ppOtworow": 0,
    "tlumienie": 0,
}

c = 3e8  # Predkosc swiatla [m/s]
f = 2.21e9  # Czestotliwosc [Hz]
minTlumienie = 14  # Przypisana wartosc tlumienia [dB]
rozmiarPlyty = 0.5  # Wymiar plyty [m]
minMargines = 0.003  # Minimalna odleglosc od marginesow [m]

lam = round(c / f, 4)  # Obliczenie dlugosci fali [m]

i = 10
while i >= 2:
    odstep = lam / i  # Minimalny odstep miedzy otworami [m]
    przekatna = round(lam / 2, 3)

    while przekatna > 0:
        bok = round(przekatna / math.sqrt(2), 3)
        otworyRzad = (rozmiarPlyty - minMargines * 2 + odstep) // (bok + odstep)
        otworyWszystkie = otworyRzad ** 2
        margines = rozmiarPlyty - otworyRzad * (bok + odstep) - odstep

        if margines < minMargines:
            przekatna -= 0.001
            continue

        sJednego = round(20 * math.log10(lam / (2 * przekatna)), 4)
        otworyWLambdaPrzez2 = (lam / 2 - odstep) // (bok + odstep)

        if otworyWLambdaPrzez2 == 0:
            przekatna -= 0.001
            continue
        sLambdaPrzez2 = round(-20 * math.log10(math.sqrt(otworyWLambdaPrzez2)), 4)
        ppOtworow = round(bok ** 2 * otworyWszystkie, 4)
        tlumienie = round(sJednego + sLambdaPrzez2)
        if tlumienie < 14:
            przekatna -= 0.001
            continue

        if najlepsze["ppOtworow"] < ppOtworow:
            najlepsze["odstep"] = i
            najlepsze["odstepLiczba"] = odstep
            najlepsze["przekatna"] = przekatna
            najlepsze["otworyRzad"] = otworyRzad
            najlepsze["otworyWszystkie"] = otworyWszystkie
            najlepsze["ppOtworow"] = ppOtworow
            najlepsze["tlumienie"] = tlumienie

        przekatna -= 0.001

    i -= 0.5

# 6. Wizualizacja graficzna rozłożenia otworów na przesłonie
fig, ax = plt.subplots(figsize=(8, 8))

# Ustawienie granic wykresu
ax.set_xlim(0, rozmiarPlyty)
ax.set_ylim(0, rozmiarPlyty)

# Rysowanie otworów
for i in range(najlepsze["otworyRzad"]):
    for j in range(najlepsze["otworyRzad"]):
        x = najlepsze["odstep"] + i * (najlepsze["przekatna"] + najlepsze["odstep"])
        y = najlepsze["odstep"] + j * (najlepsze["przekatna"] + najlepsze["odstep"])
        ax.add_patch(patches.Rectangle((x, y), najlepsze["przekatna"], najlepsze["przekatna"], edgecolor='blue', facecolor='none'))

# Dodanie tytułu i etykiet osi
ax.set_title(f"Rozłożenie otworów na przesłonie")
ax.set_xlabel("Szerokość [m]")
ax.set_ylabel("Wysokość [m]")

# Wyświetlenie wykresu
plt.grid(True)
plt.show()
