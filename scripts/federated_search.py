import requests
import json
import os

url = "https://catalogue.dataspace.copernicus.eu/stac/search"

# Zdefiniowanie 3 niezależnych zapytań z pełnym formatem ISO 8601 dla dat
queries = [
    {
        "name": "Query 1: Optical monitoring of southern Poland",
        "payload": {
            "collections": ["sentinel-2-l2a"],
            "bbox": [19.0, 50.0, 20.0, 51.0],
            "datetime": "2024-01-01T00:00:00Z/2024-01-10T23:59:59Z",
            "limit": 15
        }
    },
    {
        "name": "Query 2: Optical monitoring of Baltic region",
        "payload": {
            "collections": ["sentinel-2-l2a"],
            "bbox": [17.0, 54.0, 19.0, 55.5],
            "datetime": "2024-01-01T00:00:00Z/2024-01-10T23:59:59Z",
            "limit": 15
        }
    },
    {
        "name": "Query 3: Radar monitoring of southern Poland",
        "payload": {
            "collections": ["sentinel-1-grd"],
            "bbox": [19.0, 50.0, 20.0, 51.0],
            "datetime": "2024-01-01T00:00:00Z/2024-01-10T23:59:59Z",
            "limit": 15
        }
    }
]

raw_items = []
normalized_items = []
seen_ids = set()
duplicates_removed = 0
query_counts = {}

print("Uruchamianie silnika federacyjnego...\n")

for q in queries:
    print(f"Wykonuję: {q['name']}...")
    try:
        resp = requests.post(url, json=q['payload'], timeout=30)
        resp.raise_for_status()
        features = resp.json().get("features", [])
        query_counts[q['name']] = len(features)
        
        for f in features:
            raw_items.append(f)
            fid = f.get("id")
            
            # Usuwanie duplikatów
            if fid in seen_ids:
                duplicates_removed += 1
                continue
            seen_ids.add(fid)
            
            # Dodawanie znormalizowanego elementu
            normalized_items.append({
                "id": fid,
                "collection": f.get("collection", "unknown"),
                "bbox": f.get("bbox", []),
                "assets_count": len(f.get("assets", {})),
                "source_provider": "CDSE",
                "source_query": q['name'],
                "_datetime_for_sorting": f.get("properties", {}).get("datetime", "")
            })
    except requests.exceptions.RequestException as e:
        print(f" BŁĄD przy {q['name']}: {e}")
        if e.response is not None:
            print(f" Szczegóły błędu API: {e.response.text}")

# Sortowanie po czasie akwizycji
normalized_items.sort(key=lambda x: x["_datetime_for_sorting"])
for item in normalized_items:
    del item["_datetime_for_sorting"]

# Automatyczne tworzenie folderu results/, by uniknąć FileNotFoundError
os.makedirs("results", exist_ok=True)

with open("results/raw_stac_items.json", "w") as f:
    json.dump(raw_items, f, indent=2)

with open("results/federated_results.json", "w") as f:
    json.dump(normalized_items, f, indent=2)

print("\nSukces! Zapisano raw_stac_items.json oraz federated_results.json w folderze results/.")
for name, count in query_counts.items():
    print(f" - {name} zwróciło produktów: {count}")
print(f" - Usunięto duplikatów: {duplicates_removed}")
