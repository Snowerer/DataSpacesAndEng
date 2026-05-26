import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
import matplotlib.pyplot as plt

OUTPUT_DIR = "results/ndvi_comparison"
REPORT_FILE = "reports/multi_observation_ndvi_comparison.txt"

def create_sample_observation(name, cloud_level):
    os.makedirs("assets/bands", exist_ok=True)
    width, height = 300, 300
    transform = from_origin(19.0, 51.0, 0.0001, 0.0001)
    
    red = np.random.normal(1200, 200, (height, width)).astype(np.float32)
    nir = np.random.normal(2600, 400, (height, width)).astype(np.float32)
    
    if cloud_level == "high":
        # Chmury silnie odbijają zarówno światło widzialne, jak i podczerwień
        red[100:250, 100:250] = 8000
        nir[100:250, 100:250] = 8500

    profile = {
        "driver": "GTiff", "height": height, "width": width,
        "count": 1, "dtype": "float32", "crs": "EPSG:4326", "transform": transform
    }
    
    red_path = f"assets/bands/{name}_B04.tif"
    nir_path = f"assets/bands/{name}_B08.tif"
    
    with rasterio.open(red_path, "w", **profile) as dst:
        dst.write(red, 1)
    with rasterio.open(nir_path, "w", **profile) as dst:
        dst.write(nir, 1)
        
    return red_path, nir_path

def compute_ndvi(red_path, nir_path):
    with rasterio.open(red_path) as r_src:
        red = r_src.read(1).astype(float)
    with rasterio.open(nir_path) as n_src:
        nir = n_src.read(1).astype(float)
    return (nir - red) / (nir + red + 1e-6)

def save_ndvi_map(ndvi, output_path, title):
    plt.figure(figsize=(6, 6))
    plt.imshow(ndvi, cmap="YlGn", vmin=-1, vmax=1)
    plt.colorbar(label="NDVI")
    plt.title(title)
    plt.savefig(output_path)
    plt.close()

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    r_low, n_low = create_sample_observation("low_cloud", "low")
    r_high, n_high = create_sample_observation("high_cloud", "high")
    
    ndvi_low = compute_ndvi(r_low, n_low)
    ndvi_high = compute_ndvi(r_high, n_high)
    
    save_ndvi_map(ndvi_low, f"{OUTPUT_DIR}/low_cloud_observation_ndvi_map.png", "Czysta scena (Niskie zachmurzenie)")
    save_ndvi_map(ndvi_high, f"{OUTPUT_DIR}/high_cloud_observation_ndvi_map.png", "Skażona scena (Wysokie zachmurzenie)")
    
    with open(REPORT_FILE, "w") as f:
        f.write("MULTI-OBSERVATION NDVI COMPARISON REPORT\n")
        f.write("========================================\n\n")
        f.write(f"Scena 1 (Niskie zachmurzenie):\n")
        f.write(f"  Średnie NDVI: {np.mean(ndvi_low):.4f}\n")
        f.write(f"  Piksele wysokiej roślinności (NDVI > 0.5): {np.sum(ndvi_low > 0.5)}\n\n")
        f.write(f"Scena 2 (Wysokie zachmurzenie):\n")
        f.write(f"  Średnie NDVI: {np.mean(ndvi_high):.4f}\n")
        f.write(f"  Piksele wysokiej roślinności (NDVI > 0.5): {np.sum(ndvi_high > 0.5)}\n\n")
        f.write("WNIOSKI INŻYNIERSKIE:\n")
        f.write("- Chmury drastycznie spłaszczają wartości NDVI w okolice zera (tutaj ~0.03 w rejonie chmury).\n")
        f.write("- Wysokie zachmurzenie fałszuje statystyki, ukrywając realną roślinność pod spodem.\n")
        f.write("- Przed podaniem danych do modeli klasyfikacji AI niezbędne jest filtrowanie jakościowe.\n")

    print(f"Zadanie P1 zakończone. Raport: {REPORT_FILE}")

if __name__ == "__main__":
    main()
