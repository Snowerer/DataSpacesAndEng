import os
import numpy as np
import matplotlib.pyplot as plt

NDVI_PATH = "results/ndvi/ndvi.npy"
MASK_OUTPUT = "results/ndvi/water_mask.png"
REPORT_FILE = "reports/water_detection.txt"

def main():
    if not os.path.exists(NDVI_PATH):
        print(f"Błąd: Brak pliku {NDVI_PATH}. Uruchom najpierw ndvi_pipeline.py.")
        return
        
    ndvi = np.load(NDVI_PATH)
    
    # Tworzenie maski binarnej: True dla NDVI < 0
    water_mask = ndvi < 0
    
    water_pixels = np.sum(water_mask)
    non_water_pixels = ndvi.size - water_pixels
    water_percentage = (water_pixels / ndvi.size) * 100
    
    # Zapis binarnej macierzy do pliku npy
    np.save("results/ndvi/water_mask.npy", water_mask)
    
    # Wizualizacja maski (zwykła binarna mapa czarno-biała lub niebieska)
    plt.figure(figsize=(8, 6))
    plt.imshow(water_mask, cmap="Blues")
    plt.title("Binarna Maska Detekcji Wody (NDVI < 0)")
    plt.colorbar(label="Woda (1 = Tak, 0 = Nie)")
    plt.savefig(MASK_OUTPUT)
    plt.close()
    
    with open(REPORT_FILE, "w") as f:
        f.write("RAPORT DETEKCJI OBSZARÓW WODNYCH\n")
        f.write("================================\n\n")
        f.write(f"Reguła detekcji: NDVI < 0.0\n")
        f.write(f"Liczba pikseli sklasyfikowanych jako woda: {water_pixels}\n")
        f.write(f"Liczba pikseli lądu/roślinności: {non_water_pixels}\n")
        f.write(f"Procentowy udział zbiorników wodnych: {water_percentage:.2f}%\n\n")
        f.write("INTERPRETACJA INŻYNIERSKA:\n")
        f.write("- Ujemne wartości NDVI skutecznie wskazują otwartą wodę, lecz mogą też reagować na głębokie cienie.\n")
        f.write("- Maska ta stanowi świetny produkt wejściowy (labeling) do dalszego uczenia maszynowego (AI).\n")

    print(f"Zadanie P2 zakończone. Maska zapisana w: {MASK_OUTPUT}")

if __name__ == "__main__":
    main()
