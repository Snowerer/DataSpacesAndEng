import requests
import json
import datetime
import os

BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"

def generate_report():
    response = requests.get(BROKER_EVENTS_URL)
    events = response.json()
    
    with open("contracts/event_schema.json", "r") as f:
         required_fields = json.load(f)["required_fields"]
         
    with open("contracts/providers_registry.json", "r") as f:
         expected_providers = [p["name"] for p in json.load(f)]
         
    valid_events = [e for e in events if not [f for f in required_fields if f not in e]]
    invalid_events = len(events) - len(valid_events)
    
    active_providers = sorted(set(e.get("provider") for e in valid_events))
    missing_providers = sorted(set(expected_providers) - set(active_providers))
    
    per_provider = {p: sum(1 for e in valid_events if e.get("provider") == p) for p in active_providers}
    distinct_objects = len(set(e.get("object_id") for e in valid_events))
    obj_003_count = sum(1 for e in valid_events if e.get("object_id") == "OBJ-003")
    
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"reports/stream_report_{now_str}.txt"
    
    with open(report_path, "w") as f:
        f.write("REAL-TIME FEDERATION REPORT\n")
        f.write(f"Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("[STREAM STATUS]\n")
        f.write(f"Total events: {len(events)}\n")
        f.write(f"Valid events: {len(valid_events)}\n")
        f.write(f"Invalid events: {invalid_events}\n\n")
        f.write("[PROVIDERS]\n")
        f.write(f"Active providers: {', '.join(active_providers) if active_providers else 'none'}\n")
        f.write(f"Missing providers: {', '.join(missing_providers) if missing_providers else 'none'}\n\n")
        f.write("[PER-PROVIDER COUNTS]\n")
        for p, count in per_provider.items():
            f.write(f"{p}: {count}\n")
        f.write("\n[OBJECT STATISTICS]\n")
        f.write(f"Distinct objects: {distinct_objects}\n")
        f.write(f"OBJ-003 observations: {obj_003_count}\n\n")
        f.write("[FEDERATION STATUS]\n")
        f.write(f"COMPLETE: {'NO' if missing_providers else 'YES'}\n")
        
    print(f"Report generated successfully: {report_path}")

if __name__ == "__main__":
    generate_report()
