import os
import rasterio

RASTER_FILES = [
    "assets/bands/B04_10m.tif",
    "assets/bands/B08_10m.tif"
]

OUTPUT_REPORT = "reports/raster_inspection.txt"

def main():
    os.makedirs("reports", exist_ok=True)
    
    with open(OUTPUT_REPORT, "w") as report:
        report.write("RAPORT INSPEKCJI RASTRÓW\n")
        report.write("========================\n\n")
        
        for path in RASTER_FILES:
            if not os.path.exists(path):
                report.write(f"Plik {path} nie istnieje. Pomijanie.\n\n")
                continue
                
            with rasterio.open(path) as src:
                report.write(f"Ścieżka pliku: {path}\n")
                report.write(f"Szerokość (Width): {src.width} px\n")
                report.write(f"Wysokość (Height): {src.height} px\n")
                report.write(f"Liczba pasm (Bands): {src.count}\n")
                report.write(f"Układ współrzędnych (CRS): {src.crs}\n")
                report.write(f"Zasięg przestrzenny (Bounds): {src.bounds}\n")
                report.write("-" * 40 + "\n\n")
                
    print(f"Inspekcja zakończona. Raport zapisany w: {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
