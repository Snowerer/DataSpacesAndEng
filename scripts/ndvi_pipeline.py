import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

def main():
    os.makedirs("results/ndvi", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    red_path = "assets/bands/B04_10m.tif"
    nir_path = "assets/bands/B08_10m.tif"
    
    with rasterio.open(red_path) as red_src:
        red = red_src.read(1).astype(float)
    with rasterio.open(nir_path) as nir_src:
        nir = nir_src.read(1).astype(float)
        
    # Wyznaczenie indeksu NDVI
    ndvi = (nir - red) / (nir + red + 1e-6)
    
    np.save("results/ndvi/ndvi.npy", ndvi)
    
    n_min = float(ndvi.min())
    n_max = float(ndvi.max())
    n_mean = float(np.mean(ndvi))
    
    high_veg_pixels = int(np.sum(ndvi > 0.5))
    low_ndvi_pixels = int(np.sum(ndvi < 0))
    total_pixels = int(ndvi.size)
    
    plt.figure(figsize=(8, 8))
    plt.imshow(ndvi, cmap="YlGn")
    plt.colorbar(label="Wskaźnik NDVI")
    plt.title("Mapa NDVI (Dane Syntetyczne)")
    plt.savefig("results/ndvi/ndvi_map.png")
    plt.close()
    
    report_path = "reports/ndvi_analysis.txt"
    with open(report_path, "w") as f:
        f.write("ANALIZA WSKAŹNIKA NDVI\n")
        f.write("======================\n\n")
        f.write(f"Plik wejściowy macierzy: results/ndvi/ndvi.npy\n")
        f.write(f"Wygenerowana wizualizacja: results/ndvi/ndvi_map.png\n\n")
        f.write(f"Minimalne NDVI: {n_min:.4f}\n")
        f.write(f"Maksymalne NDVI: {n_max:.4f}\n")
        f.write(f"Średnie NDVI: {n_mean:.4f}\n\n")
        f.write(f"Liczba pikseli gęstej roślinności (NDVI > 0.5): {high_veg_pixels}\n")
        f.write(f"Liczba pikseli o ujemnym wskaźniku (NDVI < 0): {low_ndvi_pixels}\n\n")
        f.write("INTERPRETACJA INŻYNIERSKA:\n")
        f.write("- Piksele NDVI > 0.5 wskazują na zdrową pokrywę roślinną.\n")
        f.write("- Piksele ujemne odzwierciedlają sztuczny zbiornik wodny absorpcyjny dla podczerwieni.\n")

    print(f"Potok NDVI wykonany! Sprawdź raport w: {report_path}")

if __name__ == "__main__":
    main()
