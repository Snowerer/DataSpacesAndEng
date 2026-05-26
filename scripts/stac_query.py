import requests

url = "https://catalogue.dataspace.copernicus.eu/stac/search"
query = {
    "collections": ["sentinel-2-l2a"],
    "limit": 5
}

try:
    response = requests.post(
        url,
        json=query,
        timeout=20
    )
    response.raise_for_status()
    data = response.json()

    print("Znalezione produkty:\n" + "="*40)
    for item in data.get("features", []):
        product_id = item["id"]
        acq_time = item["properties"]["datetime"]
        
        # Rozdzielanie ID po znaku "_"
        parts = product_id.split('_')
        satellite = parts[0] if len(parts) > 0 else "Unknown"
        tile = parts[5] if len(parts) > 5 else "Unknown"
        
        # Liczenie zasobów
        assets_count = len(item.get("assets", {}))

        print(f"Product ID: {product_id}")
        print(f"Acquisition time: {acq_time}")
        print(f"Satellite: {satellite}")
        print(f"Tile identifier: {tile}")
        print(f"Available assets: {assets_count}")
        print("-" * 40)

except requests.exceptions.RequestException as e:
    print("REQUEST FAILED:", e)
except ValueError:
    print("INVALID JSON RESPONSE")
