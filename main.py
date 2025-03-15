import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

najlepsze = {
    "odstep": 0,
    "odstep_wartosc": 0,
    "przekatna": 0,
    "otwory_w_rzedzie": 0,
    "otwory_wszystkie": 0,
    "pp_otworow": 0,
    "tlumienie": 0,
}

c = 3e8  # Predkosc swiatla [m/s]
f = 2.21e9  # Czestotliwosc [Hz]
min_tlumienie = 14  # Wymagane tlumienie [dB]
rozmiar_plyty = 0.5  # Wymiar plyty [m]
min_margines = 0.003  # Minimalna odleglosc od krawedzi [m]

lam = round(c / f, 4)  # Dlugosc fali [m]

i = 10
while i >= 2:
    odstep = lam / i  # Minimalny odstep miedzy otworami [m]
    przekatna = round(lam / 2, 4)

    while przekatna > 0:
        bok = round(przekatna / math.sqrt(2), 3)
        otwory_w_rzedzie = (rozmiar_plyty - 2 * min_margines) // (bok + odstep)
        otwory_wszystkie = otwory_w_rzedzie ** 2
        margines = (rozmiar_plyty - otwory_w_rzedzie * (bok + odstep) + odstep) / 2

        if margines < min_margines:
            przekatna -= 0.001
            continue

        s_jednego = round(20 * math.log10(lam / (2 * przekatna)), 4)
        otwory_w_lambda_przez_2 = (lam / 2 - odstep) // (bok + odstep)

        if otwory_w_lambda_przez_2 == 0:
            przekatna -= 0.001
            continue
        s_lambda_przez_2 = round(-20 * math.log10(math.sqrt(otwory_w_lambda_przez_2)), 4)
        pp_otworow = round(bok ** 2 * otwory_wszystkie, 4)
        tlumienie = round(s_jednego + s_lambda_przez_2)
        if tlumienie < 14:
            przekatna -= 0.001
            continue

        if najlepsze["pp_otworow"] < pp_otworow:
            najlepsze["odstep"] = i
            najlepsze["odstep_wartosc"] = odstep
            najlepsze["przekatna"] = przekatna
            najlepsze["otwory_w_rzedzie"] = int(otwory_w_rzedzie)
            najlepsze["otwory_wszystkie"] = int(otwory_wszystkie)
            najlepsze["pp_otworow"] = pp_otworow
            najlepsze["tlumienie"] = tlumienie

        przekatna -= 0.001

    i -= 0.5

# Wypisanie wynikow
print("Najlepsze parametry:")
print(f"Odstep miedzy otworami: {najlepsze['odstep_wartosc']} m")
print(f"Przekatna otworu: {najlepsze['przekatna']} m")
print(f"Liczba otworow w rzedzie: {najlepsze['otwory_w_rzedzie']}")
print(f"Laczna liczba otworow: {najlepsze['otwory_wszystkie']}")
print(f"Pole powierzchni otworow: {najlepsze['pp_otworow']} m2")
print(f"Tlumienie: {najlepsze['tlumienie']} dB")

# Wizualizacja rozmieszczenia otworow na przeslonie
fig, ax = plt.subplots(figsize=(8, 8))

# Ustawienie granic wykresu
ax.set_xlim(0, rozmiar_plyty)
ax.set_ylim(0, rozmiar_plyty)

# Obliczenie pozycji otworow z uwzglednieniem marginesow
start_x = min_margines
start_y = min_margines

# Rysowanie otworow
for i in range(najlepsze["otwory_w_rzedzie"]):
    for j in range(najlepsze["otwory_w_rzedzie"]):
        x = start_x + i * (najlepsze["przekatna"] + najlepsze["odstep_wartosc"])
        y = start_y + j * (najlepsze["przekatna"] + najlepsze["odstep_wartosc"])
        ax.add_patch(patches.Rectangle((x, y), najlepsze["przekatna"], najlepsze["przekatna"], edgecolor='blue', facecolor='none'))

# Dodanie tytulu i etykiet osi
ax.set_title(f"Rozmieszczenie {najlepsze['otwory_wszystkie']} otworow na przeslonie")
ax.set_xlabel("Szerokosc [m]")
ax.set_ylabel("Wysokosc [m]")

# Wyswietlenie wykresu
plt.grid(True)
plt.show()