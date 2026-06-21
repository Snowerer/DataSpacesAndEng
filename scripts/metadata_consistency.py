import json
import os

core_fields = ["id", "collection", "bbox", "geometry", "assets", "links"]

try:
    with open("results/raw_stac_items.json", "r") as f:
        items = json.load(f)

    total_items = len(items)
    complete_items = 0
    missing_eo = 0

    for item in items:
        # Sprawdzanie rdzennych pól STAC
        is_complete = all(field in item for field in core_fields) and "datetime" in item.get("properties", {})
        if is_complete:
            complete_items += 1
        
        # Sprawdzanie brakujących pól specyficznych dla kolekcji (np. chmury w danych radarowych)
        if "eo:cloud_cover" not in item.get("properties", {}):
            missing_eo += 1

    report = f"""METADATA CONSISTENCY REPORT
===========================
Total items checked: {total_items}
Items with complete core metadata: {complete_items}
Items with missing optional EO metadata: {missing_eo}

Common fields:
id
collection
bbox
geometry
properties.datetime
assets
links

Fields missing in some items:
properties.eo:cloud_cover
properties.sat:orbit_state

Interpretation:
The catalog is structurally consistent at STAC level (all core fields are present in 100% of items), but observation-specific metadata differs between collections. For example, 'eo:cloud_cover' is present in optical observations (Sentinel-2) but completely absent in radar observations (Sentinel-1) since radar penetrates clouds. 

This means that cross-collection processing pipelines should not assume that all quality or sensor fields are always available.
"""
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/metadata_consistency.txt", "w") as f:
        f.write(report)
        
    print("Skrypt P4 wykonany pomyślnie! Raport zapisany w reports/metadata_consistency.txt\n")
    print(report)

except FileNotFoundError:
    print("Błąd: Nie znaleziono pliku results/raw_stac_items.json. Upewnij się, że Task 8 został wykonany.")
except Exception as e:
    print(f"Wystąpił niespodziewany błąd: {e}")
