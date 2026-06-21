import os

REPORT_FILE = "reports/federated_observation_selection.txt"

def compute_sensor_score(sensor_name, scenario):
    score = 50 # Bazowe punkty za dostępność kolekcji
    if sensor_name == "Sentinel-2 Optical":
        if scenario == "normal":
            score += 70 # Optymalne warunki dla pasm widzialnych
        elif scenario == "cloudy":
            score -= 30 # Chmury blokują widoczność optyczną
        elif scenario == "night":
            score -= 50 # Brak światła słonecznego uniemożliwia rejestrację pasm RGB/NIR
    elif sensor_name == "Sentinel-1 SAR (Radar)":
        if scenario == "normal":
            score += 40 # Dobry odczyt struktury terenu
        elif scenario == "cloudy":
            score += 80 # Radar przenika chmury - najwyższy priorytet
        elif scenario == "night":
            score += 80 # Brak słońca nie wpływa na aktywny sensor radarowy
    return score

def main():
    os.makedirs("reports", exist_ok=True)
    scenarios = ["normal", "cloudy", "night"]
    sensors = ["Sentinel-2 Optical", "Sentinel-1 SAR (Radar)"]
    
    with open(REPORT_FILE, "w") as f:
        f.write("RAPORT Z DECYZJI FEDEROWANEGO WYBORU SENSORÓW\n")
        f.write("============================================\n\n")
        
        for sc in scenarios:
            f.write(f"Scenariusz operacyjny: {sc.upper()}\n")
            f.write("-" * 35 + "\n")
            scores = {}
            for sensor in sensors:
                score = compute_sensor_score(sensor, sc)
                scores[sensor] = score
                f.write(f" - {sensor}: {score} pkt\n")
                
            best_sensor = max(scores, key=scores.get)
            f.write(f"Rekomendacja systemu: [ {best_sensor} ]\n\n")

    print(f"Zadanie P4 zakończone. Decyzje federacyjne zapisano w: {REPORT_FILE}")

if __name__ == "__main__":
    main()
