import os
import rasterio
import numpy as np

RASTER_FILES = {
    "B04_10m": "assets/bands/B04_10m.tif",
    "B08_10m": "assets/bands/B08_10m.tif"
}

OUTPUT_REPORT = "reports/spectral_statistics.txt"

def main():
    os.makedirs("reports", exist_ok=True)
    
    with open(OUTPUT_REPORT, "w") as report:
        report.write("STATYSTYKI SPEKTRALNE PASM\n")
        report.write("==========================\n\n")
        
        for name, path in RASTER_FILES.items():
            if not os.path.exists(path):
                print(f"Pominięto brakujący plik: {path}")
                continue
                
            with rasterio.open(path) as src:
                band_data = src.read(1)
                
                p_min = np.min(band_data)
                p_max = np.max(band_data)
                p_mean = np.mean(band_data)
                p_std = np.std(band_data)
                
                report.write(f"Pasmo: {name}\n")
                report.write(f"  Minimum: {p_min:.2f}\n")
                report.write(f"  Maksimum: {p_max:.2f}\n")
                report.write(f"  Średnia (Mean): {p_mean:.2f}\n")
                report.write(f"  Odchylenie standardowe (STD): {p_std:.2f}\n\n")
                
        report.write("INTERPRETACJA INŻYNIERSKA:\n")
        report.write("1. Które pasmo zawiera większe średnie wartości?\n")
        report.write("   Odp: Pasmo B08 (bliska podczerwień) ma wyższą średnią.\n")
        report.write("2. Dlaczego roślinność zachowuje się inaczej w obu pasmach?\n")
        report.write("   Odp: Zdrowa roślinność pochłania światło czerwone (B04), a odbija bliską podczerwień (B08).\n")
        report.write("3. Dlaczego te różnice są ważne dla obliczania NDVI?\n")
        report.write("   Odp: Kontrast między odbiciem a absorpcją pozwala jednoznacznie zidentyfikować żywą roślinność.\n")

    print(f"Statystyki obliczone. Wyniki zapisano w: {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
