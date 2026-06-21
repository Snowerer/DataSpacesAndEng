import os
import requests
from datetime import datetime

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"
QUERY = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [19.0, 50.0, 20.0, 51.0],
    "datetime": "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z",
    "limit": 10
}
REPORT_FILE = "reports/observation_ranking.txt"

def parse_datetime(value):
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)

def compute_cloud_score(cloud_cover):
    if cloud_cover is None:
        return 0
    return max(0, 100 - cloud_cover)

def compute_completeness_score(assets_count):
    if assets_count >= 30:
        return 30
    elif assets_count >= 20:
        return 20
    elif assets_count >= 10:
        return 10
    else:
        return 0

def compute_recency_score(acquisition_time, newest_time):
    if acquisition_time is None or newest_time is None:
        return 0
    total_days = 30
    age_days = (newest_time - acquisition_time).total_seconds() / 86400
    score = max(0, 20 - (age_days / total_days) * 20)
    return score

def main():
    os.makedirs("reports", exist_ok=True)
    
    print("Querying STAC for multiple observations...")
    response = requests.post(STAC_URL, json=QUERY, timeout=30)
    response.raise_for_status()
    features = response.json().get("features", [])
    
    if not features:
        print("No observations found to rank.")
        return
        
    # Znalezienie najświeższej daty w pobranym zestawie do obliczenia recency
    parsed_times = []
    for item in features:
        dt_str = item.get("properties", {}).get("datetime")
        if dt_str:
            parsed_times.append(parse_datetime(dt_str))
    newest_time = max(parsed_times) if parsed_times else None

    ranked_observations = []

    for item in features:
        properties = item.get("properties", {})
        assets = item.get("assets", {})
        
        product_id = item.get("id")
        acq_time_str = properties.get("datetime")
        acq_time = parse_datetime(acq_time_str) if acq_time_str else None
        cloud_cover = properties.get("eo:cloud_cover")
        assets_count = len(assets)
        
        c_score = compute_cloud_score(cloud_cover)
        comp_score = compute_completeness_score(assets_count)
        r_score = compute_recency_score(acq_time, newest_time)
        final_score = c_score + comp_score + r_score
        
        ranked_observations.append({
            "id": product_id,
            "datetime": acq_time_str,
            "cloud_cover": cloud_cover,
            "assets_count": assets_count,
            "cloud_score": c_score,
            "completeness_score": comp_score,
            "recency_score": r_score,
            "final_score": final_score
        })

    # Sortowanie od najlepszego wyniku do najgorszego
    ranked_observations = sorted(ranked_observations, key=lambda x: x["final_score"], reverse=True)

    with open(REPORT_FILE, "w") as f:
        f.write("OBSERVATION RANKING REPORT\n")
        f.write("==========================\n\n")
        for i, obs in enumerate(ranked_observations, 1):
            f.write(f"{i}. ID: {obs['id']}\n")
            f.write(f"   Time: {obs['datetime']}\n")
            f.write(f"   Cloud cover: {obs['cloud_cover']}\n")
            f.write(f"   Assets count: {obs['assets_count']}\n")
            f.write(f"   Cloud score: {obs['cloud_score']:.2f}\n")
            f.write(f"   Completeness score: {obs['completeness_score']:.2f}\n")
            f.write(f"   Recency score: {obs['recency_score']:.2f}\n")
            f.write(f"   Final score: {obs['final_score']:.2f}\n\n")

    print(f"Ranking zakończony sukcesem. Wyniki zapisano w: {REPORT_FILE}")

if __name__ == "__main__":
    main()
