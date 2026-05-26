import os
import numpy as np
import rasterio
from rasterio.transform import from_origin

def main():
    os.makedirs("assets/bands", exist_ok=True)
    width = 300
    height = 300
    
    # Definicja transformacji przestrzennej (Kraków/Polska)
    transform = from_origin(19.0, 51.0, 0.0001, 0.0001)
    
    # Generowanie sztucznych danych symulujących pasma optyczne
    # Red (B04) zazwyczaj ma niższe wartości dla zdrowej roślinności
    red = np.random.normal(1200, 250, (height, width)).astype(np.float32)
    # NIR (B08) ma znacznie wyższe wartości dla roślinności
    nir = np.random.normal(2500, 500, (height, width)).astype(np.float32)
    
    # Dodajmy sztuczny obszar "wody" (bardzo niskie odbicie w podczerwieni NIR)
    red[10:50, 10:50] = 800
    nir[10:50, 10:50] = 200

    profile = {
        "driver": "GTiff",
        "height": height,
        "width": width,
        "count": 1,
        "dtype": "float32",
        "crs": "EPSG:4326",
        "transform": transform
    }
    
    # Zapisywanie pasma Red
    with rasterio.open("assets/bands/B04_10m.tif", "w", **profile) as dst:
        dst.write(red, 1)
        
    # Zapisywanie pasma NIR
    with rasterio.open("assets/bands/B08_10m.tif", "w", **profile) as dst:
        dst.write(nir, 1)
        
    print("Sample bands created:")
    print(" - assets/bands/B04_10m.tif")
    print(" - assets/bands/B08_10m.tif")

if __name__ == "__main__":
    main()
