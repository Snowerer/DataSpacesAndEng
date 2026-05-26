import os
import numpy as np
import rasterio

REPORT_FILE = "reports/eo_processing_report.txt"
ASSET_PATHS = {
    "B04": "assets/bands/B04_10m.tif",
    "B08": "assets/bands/B08_10m.tif",
    "NDVI": "results/ndvi/ndvi.npy",
    "NDVI map": "results/ndvi/ndvi_map.png"
}

def check_file_status(path):
    return "dostępny" if os.path.exists(path) else "brakujący"

def get_raster_metadata(path):
    if not os.path.exists(path):
        return "Brak pliku do odczytu metadanych."
    with rasterio.open(path) as src:
        return f"Rozmiar: {src.width}x{src.height} px, Pasma: {src.count}, CRS: {src.crs}"

def get_band_statistics(path):
    if not os.path.exists(path):
        return "Brak danych."
    with rasterio.open(path) as src:
        data = src.read(1)
        return f"Min: {np.min(data):.2f}, Max: {np.max(data):.2f}, Średnia: {np.mean(data):.2f}"

def read_ranking_summary(path):
    if not os.path.exists(path):
        return "Brak wygenerowanego raportu rankingu."
    with open(path, "r") as f:
        lines = f.readlines()
    # Pobieramy nagłówek i dane o pierwszej (najlepszej) rekomendowanej obserwacji
    summary = "".join(lines[:11])
    return summary

def main():
    os.makedirs("reports", exist_ok=True)
    
    # Wczytanie statystyk NDVI, jeśli plik istnieje
    ndvi_stats = "Brak pliku macierzy NDVI."
    veg_assessment = "Brak oceny wegetacji - uruchom najpierw ndvi_pipeline.py"
    
    if os.path.exists(ASSET_PATHS["NDVI"]):
        ndvi_data = np.load(ASSET_PATHS["NDVI"])
        n_min = np.min(ndvi_data)
        n_max = np.max(ndvi_data)
        n_mean = np.mean(ndvi_data)
        high_veg_ratio = np.sum(ndvi_data > 0.5) / ndvi_data.size
        
        ndvi_stats = f"Min: {n_min:.4f}, Max: {n_max:.4f}, Średnia: {n_mean:.4f}"
        if high_veg_ratio > 0.15:
            veg_assessment = "Wykryto wysokie zagęszczenie zielonej roślinności na badanym obszarze."
        else:
            veg_assessment = "Niskie zagęszczenie roślinności, dominacja powierzchni nieożywionych lub wody."

    with open(REPORT_FILE, "w") as f:
        f.write("ZBIORCZY RAPORT PRZETWARZANIA EO (EARTH OBSERVATION)\n")
        f.write("====================================================\n\n")
        
        f.write("1. STATUS GENEROWANIA ZASOBÓW:\n")
        for name, path in ASSET_PATHS.items():
            f.write(f"   - {name}: {check_file_status(path)} ({path})\n")
        f.write("\n")
        
        f.write("2. METADANE TECHNICZNE RASTRÓW:\n")
        f.write(f"   - Pasmo B04: {get_raster_metadata(ASSET_PATHS['B04'])}\n")
        f.write(f"   - Pasmo B08: {get_raster_metadata(ASSET_PATHS['B08'])}\n")
        f.write("\n")
        
        f.write("3. STATYSTYKI RADIOMETRYCZNE PASM SPEKTRALNYCH:\n")
        f.write(f"   - Czerwień (B04): {get_band_statistics(ASSET_PATHS['B04'])}\n")
        f.write(f"   - Bliska Podczerwień (B08): {get_band_statistics(ASSET_PATHS['B08'])}\n")
        f.write("\n")
        
        f.write("4. WYNIKI ANALIZY INDEKSU ROŚLINNOŚCI (NDVI):\n")
        f.write(f"   - Statystyki NDVI: {ndvi_stats}\n")
        f.write(f"   - Ocena Środowiskowa: {veg_assessment}\n")
        f.write("\n")
        
        f.write("5. REKOMENDACJA Z SILNIKA RANKINGOWEGO:\n")
        f.write(read_ranking_summary("reports/observation_ranking.txt"))
        
    print(f"Zbiorczy raport wygenerowany pomyślnie i zapisany w: {REPORT_FILE}")

if __name__ == "__main__":
    main()
