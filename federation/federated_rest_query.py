import json
import requests
from collections import Counter

# 1. Wczytanie rejestru dostawców z pliku
with open("contracts/providers_registry.json", "r") as f:
    providers = json.load(f)

all_results = []
provider_counts = Counter()

# 2. Pętla odpytująca każdego dostawcę
for provider in providers:
    provider_name = provider["name"]
    provider_url = provider["url"]
    
    try:
        # Pobieramy dane
        response = requests.get(f"{provider_url}/observations")
        data = response.json()
        
        # 3. Znakujemy każdy rekord nazwą dostawcy i dodajemy do głównej listy
        for row in data:
            row["provider"] = provider_name
            all_results.append(row)
            
        # Zliczamy, ile rekordów dostarczył dany provider
        provider_counts[provider_name] += len(data)
    except Exception as e:
        print(f"Błąd połączenia z {provider_name}: {e}")

# 4. Wyświetlanie podsumowania (zgodnie z oczekiwanym wyjściem)
print("TOTAL RECORDS:", len(all_results))

print("PER-PROVIDER COUNTS:")
for name, count in provider_counts.items():
    print(f"  {name}: {count}")

if provider_counts:
    # Pobieramy nazwę dostawcy z największą liczbą wyników
    largest_provider = provider_counts.most_common(1)[0][0]
    print("LARGEST PROVIDER:")
    print(f"  {largest_provider}")
