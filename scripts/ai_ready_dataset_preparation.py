import os
import json
import shutil

IMAGES_DIR = "dataset/images"
METADATA_DIR = "dataset/metadata"

def determine_quality(cloud_cover, mean_ndvi):
    if cloud_cover <= 10 and mean_ndvi >= 0.5:
        return "excellent", "AI_READY"
    elif cloud_cover <= 30 and mean_ndvi >= 0.3:
        return "good", "AI_READY"
    else:
        return "limited", "UNSUITABLE_OR_TRAINING_ONLY"

def main():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(METADATA_DIR, exist_ok=True)
    
    # Symulowane cechy trzech różnych obserwacji do przetworzenia w dataset
    observations = [
        {"id": "OBS_001", "cloud_cover": 5, "mean_ndvi": 0.62, "sensor": "Sentinel-2"},
        {"id": "OBS_002", "cloud_cover": 18, "mean_ndvi": 0.44, "sensor": "Sentinel-2"},
        {"id": "OBS_003", "cloud_cover": 68, "mean_ndvi": 0.11, "sensor": "Sentinel-2"}
    ]
    
    # Kopiowanie istniejącego pliku bazowego jako ustrukturyzowanych obrazów treningowych
    src_map = "results/ndvi/ndvi_map.png"
    src_mask = "results/ndvi/water_mask.png"
    
    for obs in observations:
        obs_id = obs["id"]
        quality, suitability = determine_quality(obs["cloud_cover"], obs["mean_ndvi"])
        
        # Przenoszenie zasobów wizualnych (jeśli istnieją)
        img_target = f"{IMAGES_DIR}/{obs_id}_ndvi_map.png"
        mask_target = f"{IMAGES_DIR}/{obs_id}_water_mask.png"
        
        if os.path.exists(src_map):
            shutil.copy(src_map, img_target)
        if os.path.exists(src_mask):
            shutil.copy(src_mask, mask_target)
            
        # Generowanie indywidualnego pliku metadanych JSON
        meta_content = {
            "observation_id": obs_id,
            "sensor": obs["sensor"],
            "cloud_cover": obs["cloud_cover"],
            "mean_ndvi": obs["mean_ndvi"],
            "quality": quality,
            "suitability": suitability,
            "selected_assets": [img_target, mask_target],
            "labels": {
                "vegetation_monitoring": "AI_READY" if suitability == "AI_READY" else "REQUIRES_FILTERING",
                "cloud_conditions": "LOW" if obs["cloud_cover"] < 20 else "HIGH"
            }
        }
        
        with open(f"{METADATA_DIR}/{obs_id}.json", "w") as f:
            json.dump(meta_content, f, indent=4)

    # Generowanie pliku głównego podsumowania (dataset_summary.json)
    summary = {
        "dataset_size": len(observations),
        "images_directory": IMAGES_DIR,
        "metadata_directory": METADATA_DIR,
        "quality_distribution": {
            "excellent": 1, "good": 1, "limited": 1
        }
    }
    
    with open(f"{METADATA_DIR}/dataset_summary.json", "w") as f:
        json.dump(summary, f, indent=4)
        
    print("Zbiór danych AI-Ready Dataset został wygenerowany pomyślnie!")

if __name__ == "__main__":
    main()
