import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

c = 3e8  # Prędkość światła w próżni [m/s]
f = 2.21e9  # Częstotliwość [Hz]
minS = 17  # Wymagana skuteczność ekranowania [dB]
tłumienie = 14  # Wartość tłumienia [dB]
rozmiar_płyty = 0.5  # Wymiar płyty [m] (50 cm)

# 1. Obliczenie długości fali
lam = c / f
print(f"Długość fali: {lam:.4f} m")

# 2. Obliczenie maksymalnego wymiaru liniowego otworu
# Skuteczność ekranowania dla pojedynczego otworu: S = 20 * log(lambda / (2 * l))
# Przekształcamy wzór, aby obliczyć l:
l = lam / (2 * 10 ** (minS / 20))
print(f"Maksymalny wymiar liniowy otworu: {l:.6f} m")

# 3. Obliczenie minimalnej odległości między otworami
# Dla liniowego rzędu otworów, skuteczność ekranowania spada o 20 * log(sqrt(n))
# Chcemy, aby skuteczność ekranowania nie była gorsza niż 17 dB, więc:
# 17 dB = 20 * log(sqrt(n)) + tłumienie
# Przekształcamy wzór, aby obliczyć n:
n = 10**((minS - tłumienie) / 20)
minOdl = l / math.sqrt(n)
print(f"Minimalna odległość między otworami: {minOdl:.6f} m")

# 4. Obliczenie maksymalnej liczby otworów na płytce
# Zakładamy, że otwory są kwadratowe i rozmieszczone w równych odstępach
pole_powierzchni_otworu = l ** 2  # Pole powierzchni jednego otworu
całkowite_pole_powierzchni_płyty = rozmiar_płyty**2  # Całkowite pole powierzchni płyty

# Maksymalna liczba otworów:
maksymalna_liczba_otworów = int(całkowite_pole_powierzchni_płyty / (pole_powierzchni_otworu + minOdl ** 2))
print(f"Maksymalna liczba otworów: {maksymalna_liczba_otworów}")

# 5. Obliczenie skuteczności ekranowania dla zadanej liczby otworów
# Skuteczność ekranowania dla wielu otworów: S = -20 * log(sqrt(n))
S = -20 * math.log10(math.sqrt(maksymalna_liczba_otworów))
print(f"Skuteczność ekranowania dla {maksymalna_liczba_otworów} otworów: {S:.2f} dB")

# 6. Wizualizacja graficzna rozłożenia otworów na przesłonie
fig, ax = plt.subplots(figsize=(8, 8))

# Ustawienie granic wykresu
ax.set_xlim(0, rozmiar_płyty)
ax.set_ylim(0, rozmiar_płyty)

# Obliczenie liczby otworów wzdłuż jednej osi
liczba_otworów_w_rzędzie = int(math.sqrt(maksymalna_liczba_otworów))

# Obliczenie odstępów między otworami
odstepy = (rozmiar_płyty - liczba_otworów_w_rzędzie * l) / (liczba_otworów_w_rzędzie + 1)

# Rysowanie otworów
for i in range(liczba_otworów_w_rzędzie):
    for j in range(liczba_otworów_w_rzędzie):
        x = odstepy + i * (l + odstepy)
        y = odstepy + j * (l + odstepy)
        ax.add_patch(patches.Rectangle((x, y), l, l, edgecolor='blue', facecolor='none'))

# Dodanie tytułu i etykiet osi
ax.set_title(f"Rozłożenie {maksymalna_liczba_otworów} otworów na przesłonie")
ax.set_xlabel("Szerokość [m]")
ax.set_ylabel("Wysokość [m]")

# Wyświetlenie wykresu
plt.grid(True)
plt.show()