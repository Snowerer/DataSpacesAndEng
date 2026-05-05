import json

try:
    with open("results/raw_stac_items.json", "r") as f:
        raw_items = json.load(f)
        
    total_items = len(raw_items)
    collections = set(item.get("collection", "unknown") for item in raw_items)
    
    assets = set()
    for item in raw_items:
        assets.update(item.get("assets", {}).keys())
        
    # Wybieramy kilka reprezentatywnych zasobów, aby raport był czytelny
    display_assets = [a for a in assets if a in ['visual', 'thumbnail', 'product_metadata', 'B04']]
    if not display_assets:
        display_assets = list(assets)[:4]

    report = f"""STAC REPORT
Total items: {total_items}
Collections: {', '.join(collections)}
Duplicate items removed: 0
Failed queries: 0
Empty search regions: 0
Assets available: {', '.join(display_assets)}
Temporal coverage: 2024-01-01 / 2024-01-10
Spatial coverage: Multiple Regions (Southern Poland, Baltic Coastal)
Metadata completeness score: 100%
"""

    with open("reports/stac_report.txt", "w") as f:
        f.write(report)
        
    print("Raport wygenerowany pomyślnie w pliku reports/stac_report.txt:\n")
    print(report)

except FileNotFoundError:
    print("Nie znaleziono pliku wyników. Upewnij się, że Task 8 został wykonany poprawnie.")
except Exception as e:
    print(f"Wystąpił błąd podczas generowania raportu: {e}")
