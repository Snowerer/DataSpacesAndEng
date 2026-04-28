import requests
import time
import json

BROKER_EVENTS_URL = "http://127.0.0.1:7000/events"

# Ładowanie wymagań kontraktu i rejestru dostawców
with open("contracts/event_schema.json", "r") as f:
    contract = json.load(f)
    required_fields = contract["required_fields"]

with open("contracts/providers_registry.json", "r") as f:
    expected_providers = [p["name"] for p in json.load(f)]

while True:
    response = requests.get(BROKER_EVENTS_URL)
    events = response.json()
    
    print("\n" + "="*50)
    print("CURRENT NUMBER OF EVENTS:", len(events))
    
    # Zadanie 10: Walidacja
    valid_count = 0
    invalid_count = 0
    for event in events:
        missing = [field for field in required_fields if field not in event]
        if missing:
            print("INVALID EVENT DETECTED:", event)
            print("MISSING FIELDS:", missing)
            invalid_count += 1
        else:
            valid_count += 1
            
            # ZADANIE PRAKTYCZNE P5: Threshold Alert
            if float(event.get("temperature", 0)) > 28.0:
                print(f"WARNING: Provider: {event['provider']} | Object: {event['object_id']} | Temperature: {event['temperature']}")
                
    print(f"VALID EVENTS: {valid_count} | INVALID EVENTS: {invalid_count}")
    
    if events:
        # Zadania 7 & 8: Agregacja w czasie rzeczywistym
        active = sorted(set(event.get("provider") for event in events if "provider" in event))
        objects = sorted(set(event.get("object_id") for event in events if "object_id" in event))
        
        per_provider = {}
        for event in events:
            if "provider" in event:
                prov = event["provider"]
                per_provider[prov] = per_provider.get(prov, 0) + 1
        
        selected_object = "OBJ-003"
        selected_count = sum(1 for event in events if event.get("object_id") == selected_object)
        
        print("ACTIVE PROVIDERS:", active)
        print("PER PROVIDER:", per_provider)
        print("DISTINCT OBJECTS:", len(objects))
        print(f"{selected_object} OBSERVATIONS:", selected_count)
        
        # Zadanie 9: Wykrywanie brakujących dostawców
        missing_providers = sorted(set(expected_providers) - set(active))
        print("EXPECTED PROVIDERS:", expected_providers)
        print("MISSING PROVIDERS:", missing_providers if missing_providers else "none")
        print("COMPLETE:", "NO" if missing_providers else "YES")
        
    print("="*50)
    time.sleep(3)
