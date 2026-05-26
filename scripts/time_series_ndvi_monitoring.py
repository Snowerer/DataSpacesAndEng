import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
import matplotlib.pyplot as plt

OUTPUT_DIR = "results/ndvi_timeseries"
REPORT_FILE = "reports/time_series_ndvi_monitoring.txt"

def create_temporal_observation(name, nir_level):
    os.makedirs("assets/bands", exist_ok=True)
    width, height = 300, 300
    transform = from_origin(19.0, 51.0, 0.0001, 0.0001)
    
    red = np.random.normal(1200, 150, (height, width)).astype(np.float32)
    nir = np.random.normal(nir_level, 300, (height, width)).astype(np.float32)
    
    profile = {
        "driver": "GTiff", "height": height, "width": width,
        "count": 1, "dtype": "float32", "crs": "EPSG:4326", "transform": transform
    }
    
    r_path = f"assets/bands/{name}_B04.tif"
    n_path = f"assets/bands/{name}_B08.tif"
    
    with rasterio.open(r_path, "w", **profile) as dst:
        dst.write(red, 1)
    with rasterio.open(n_path, "w", **profile) as dst:
        dst.write(nir, 1)
        return r_path, n_path

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    # Symulacja wegetacji: Kwiecień (NIR=2600), Maj (NIR=3400), Czerwiec (NIR=4300)
    scenes = {
        "2024-04-01": 2600,
        "2024-05-01": 3400,
        "2024-06-01": 4300
    }
    
    dates = list(scenes.keys())
    mean_values = []
    
    for date, nir_val in scenes.items():
        r_path, n_path = create_temporal_observation(date, nir_val)
        
        with rasterio.open(r_path) as r_s, rasterio.open(n_path) as n_s:
            red = r_s.read(1).astype(float)
            nir = n_s.read(1).astype(float)
            
        ndvi = (nir - red) / (nir + red + 1e-6)
        mean_ndvi = np.mean(ndvi)
        mean_values.append(mean_ndvi)
        
        # Zapis jednostkowych map NDVI
        plt.figure(figsize=(5, 5))
        plt.imshow(ndvi, cmap="YlGn", vmin=0, vmax=1)
        plt.title(f"NDVI z dnia {date}")
        plt.colorbar()
        plt.savefig(f"{OUTPUT_DIR}/observation_{date.replace('-', '_')}_ndvi_map.png")
        plt.close()

    # Generowanie wykresu trendu zmian
    plt.figure(figsize=(7, 4))
    plt.plot(dates, mean_values, marker='o', color='green', linestyle='-', linewidth=2)
    plt.ylim(0, 1)
    plt.xlabel("Data akwizycji")
    plt.ylabel("Średnie NDVI")
    plt.title("Trend rozwoju roślinności (Wiosna - Lato)")
    plt.grid(True, linestyle='--')
    plt.savefig(f"{OUTPUT_DIR}/mean_ndvi_trend.png")
    plt.close()
    
    # Wyznaczenie kierunku zmian trendu
    change = mean_values[-1] - mean_values[0]
    if change > 0.05:
        trend_status = "increasing vegetation activity"
    elif change < -0.05:
        trend_status = "decreasing vegetation activity"
    else:
        trend_status = "stable vegetation conditions"
        
    with open(REPORT_FILE, "w") as f:
        f.write("MONITORING SERII CZASOWEJ NDVI\n")
        f.write("=============================\n\n")
        for d, v in zip(dates, mean_values):
            f.write(f"Data: {d} -> Średnia wartość NDVI: {v:.4f}\n")
        f.write(f"\nCałkowita zmiana indeksu: {change:+.4f}\n")
        f.write(f"Wykryty trend: {trend_status}\n")

    print(f"Zadanie P3 zakończone. Wykres trendu zapisany w: {OUTPUT_DIR}/mean_ndvi_trend.png")

if __name__ == "__main__":
    main()
