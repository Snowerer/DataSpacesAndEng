import json
import requests

# 1. Wczytanie rejestru i kontraktu
with open("contracts/providers_registry.json", "r") as f:
    providers = json.load(f)

with open("contracts/observation_schema.json", "r") as f:
    contract = json.load(f)

required_fields = contract["required_fields"]

# Zmienne do podsumowania
status_counts = {"OK": 0, "VIOLATION": 0, "UNAVAILABLE": 0, "EMPTY DATASET": 0}
problematic_providers = []

# 2. Sprawdzanie każdego dostawcy
for provider in providers:
    provider_name = provider["name"]
    provider_url = provider["url"]
    
    try:
        # Ustawiamy timeout na 2 sekundy!
        response = requests.get(f"{provider_url}/observations", timeout=2)
        response.raise_for_status() # Wyłapuje błędy HTTP (np. 404, 500)
        
        data = response.json()
        
        if len(data) == 0:
            print(f"{provider_name}: EMPTY DATASET")
            status_counts["EMPTY DATASET"] += 1
            problematic_providers.append(provider_name)
            continue
            
        # Sprawdzamy czy pierwszy rekord ma wszystkie wymagane pola z kontraktu
        missing = [field for field in required_fields if field not in data[0]]
        
        if missing:
            print(f"{provider_name}: VIOLATION (Missing fields: {missing})")
            status_counts["VIOLATION"] += 1
            problematic_providers.append(provider_name)
        else:
            print(f"{provider_name}: OK")
            status_counts["OK"] += 1
            
    except Exception:
        # Jeśli serwer nie odpowie w 2 sekundy lub odrzuci połączenie
        print(f"{provider_name}: UNAVAILABLE")
        status_counts["UNAVAILABLE"] += 1
        problematic_providers.append(provider_name)

# 3. Podsumowanie i ocena stanu federacji
print("\nSUMMARY:")
for status, count in status_counts.items():
    print(f"{status}: {count}")

print("\nPROBLEMATIC PROVIDERS:")
if problematic_providers:
    for name in problematic_providers:
        print(f"  {name}")
else:
    print("  none")

# 4. Ocena końcowa
if status_counts["OK"] == len(providers):
    print("\nFEDERATION STATE: RELIABLE")
else:
    print("\nFEDERATION STATE: DEGRADED")
