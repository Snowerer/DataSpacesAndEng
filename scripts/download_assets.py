import os
import requests

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"
QUERY = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [19.0, 50.0, 20.0, 51.0],
    "datetime": "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z",
    "query": {
        "eo:cloud_cover": {
            "lt": 20
        }
    },
    "limit": 1
}

OUTPUT_PATHS = {
    "thumbnail": "assets/thumbnails/thumbnail.jpg",
    "TCI_10m": "assets/visual/visual.jp2",
    "B04_10m": "assets/bands/B04.jp2",
    "B08_10m": "assets/bands/B08.jp2"
}

def is_http_url(url):
    return url.startswith("http://") or url.startswith("https://")

def download_file(url, output_path):
    if not is_http_url(url):
        print(f"SKIPPED NON-HTTP ASSET: {url}")
        return False
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"FAILED TO DOWNLOAD {url}: {e}")
        return False

def main():
    print("Querying STAC API...")
    response = requests.post(STAC_URL, json=QUERY)
    response.raise_for_status()
    data = response.json()
    
    if not data.get("features"):
        print("No features found matching query.")
        return

    item = data["features"][0]
    assets = item["assets"]
    
    print("\nAVAILABLE ASSETS IN METADATA:")
    for asset_name in assets:
        print(f" - {asset_name}")
        
    downloaded_count = 0
    skipped_count = 0
    
    print("\nStarting asset processing...")
    for target_asset, target_path in OUTPUT_PATHS.items():
        if target_asset in assets:
            asset_url = assets[target_asset].get("href")
            print(f"Processing target asset '{target_asset}': {asset_url}")
            if download_file(asset_url, target_path):
                downloaded_count += 1
            else:
                skipped_count += 1
        else:
            print(f"Target asset '{target_asset}' not found in item metadata.")
            skipped_count += 1

    # Generowanie krótkiego raportu z pobierania
    report_path = "reports/download_report.txt"
    with open(report_path, "w") as rep:
        rep.write("DOWNLOAD REPORT\n===============\n")
        rep.write(f"Product ID: {item.get('id')}\n")
        rep.write(f"Total downloaded assets: {downloaded_count}\n")
        rep.write(f"Total skipped/unsupported assets: {skipped_count}\n")
    print(f"\nDownload processing completed. Summary saved to {report_path}")

if __name__ == "__main__":
    main()
