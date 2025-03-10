import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Stałe
c = 3e8  # Prędkość światła w próżni [m/s]

# Dane wejściowe
f = 2.21e9  # Częstotliwość [Hz]
minS = 17  # Wymagana skuteczność ekranowania [dB]
tłumienie = 14  # Wartość tłumienia [dB]
rozmiar_płyty = 0.5  # Wymiar płyty [m] (50 cm)

# 1. Obliczenie długości fali
lam = c / f
print(f"Długość fali: {lam:.4f} m")

# 2. Obliczenie maksymalnego wymiaru liniowego otworu
l = lam / (2 * 10 ** (minS / 20))
print(f"Maksymalny wymiar liniowy otworu: {l:.6f} m")

# 3. Obliczenie minimalnej odległości między otworami
n = 10**((minS - tłumienie) / 20)
minOdl = l / math.sqrt(n)
print(f"Minimalna odległość między otworami: {minOdl:.6f} m")

# 4. Obliczenie maksymalnej liczby otworów na płytce
pole_powierzchni_otworu = l ** 2  # Pole powierzchni jednego otworu
całkowite_pole_powierzchni_płyty = rozmiar_płyty**2  # Całkowite pole powierzchni płyty

# Funkcja do obliczenia skuteczności ekranowania
def oblicz_skuteczność_ekranowania(liczba_otworów):
    return -20 * math.log10(math.sqrt(liczba_otworów))

# Szukanie optymalnej liczby otworów
optymalna_liczba_otworów = 1
while True:
    S = oblicz_skuteczność_ekranowania(optymalna_liczba_otworów + 1)  # Sprawdzamy kolejną liczbę otworów
    if S < minS:
        break  # Jeśli skuteczność spadnie poniżej 17 dB, zatrzymujemy się
    optymalna_liczba_otworów += 1

print(f"Optymalna liczba otworów: {optymalna_liczba_otworów}")
print(f"Skuteczność ekranowania dla {optymalna_liczba_otworów} otworów: {oblicz_skuteczność_ekranowania(optymalna_liczba_otworów):.2f} dB")

# 5. Obliczenie pola powierzchni otworów
pole_powierzchni_wszystkich_otworów = optymalna_liczba_otworów * pole_powierzchni_otworu
print(f"Całkowite pole powierzchni otworów: {pole_powierzchni_wszystkich_otworów:.6f} m²")

# 6. Wizualizacja graficzna rozłożenia otworów na przesłonie
fig, ax = plt.subplots(figsize=(8, 8))

# Ustawienie granic wykresu
ax.set_xlim(0, rozmiar_płyty)
ax.set_ylim(0, rozmiar_płyty)

# Obliczenie liczby otworów wzdłuż jednej osi
liczba_otworów_w_rzędzie = int(math.sqrt(optymalna_liczba_otworów))

# Obliczenie odstępów między otworami
odstepy = (rozmiar_płyty - liczba_otworów_w_rzędzie * l) / (liczba_otworów_w_rzędzie + 1)

# Rysowanie otworów
for i in range(liczba_otworów_w_rzędzie):
    for j in range(liczba_otworów_w_rzędzie):
        x = odstepy + i * (l + odstepy)
        y = odstepy + j * (l + odstepy)
        ax.add_patch(patches.Rectangle((x, y), l, l, edgecolor='blue', facecolor='none'))

# Dodanie tytułu i etykiet osi
ax.set_title(f"Rozłożenie {optymalna_liczba_otworów} otworów na przesłonie")
ax.set_xlabel("Szerokość [m]")
ax.set_ylabel("Wysokość [m]")

# Wyświetlenie wykresu
plt.grid(True)
plt.show()