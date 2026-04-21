import json
import requests

# 1. Wczytanie rejestru dostawców
with open("contracts/providers_registry.json", "r") as f:
    providers = json.load(f)

object_id = "OBJ-003"
results = []
providers_with_object = []

# Lista wszystkich zarejestrowanych nazw dostawców
all_provider_names = [p["name"] for p in providers]

# 2. Odpytywanie każdego dostawcy o konkretny obiekt
for provider in providers:
    provider_name = provider["name"]
    provider_url = provider["url"]
    
    try:
        response = requests.get(f"{provider_url}/observations/{object_id}")
        data = response.json()
        
        if data:  # Jeśli odpowiedź nie jest pusta
            providers_with_object.append(provider_name)
            for row in data:
                row["provider"] = provider_name
                results.append(row)
    except Exception as e:
        print(f"Błąd połączenia z {provider_name}: {e}")

# 3. Analiza kompletności (kto nie zwrócił danych o tym obiekcie?)
missing_providers = [name for name in all_provider_names if name not in providers_with_object]

# 4. Wyświetlanie wyników zgodnie z instrukcją
print("OBJECT:", object_id)
print("TOTAL OBSERVATIONS:", len(results))

print("PROVIDERS CONTAINING OBJECT:")
for name in providers_with_object:
    print(f"  {name}")

print("MISSING PROVIDERS:")
if missing_providers:
    for name in missing_providers:
        print(f"  {name}")
else:
    print("  none")

if not missing_providers:
    print("COMPLETENESS: YES")
else:
    print("COMPLETENESS: NO")
