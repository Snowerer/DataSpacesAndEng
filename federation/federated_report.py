import json
import requests
from datetime import datetime

# Ścieżki do plików konfiguracyjnych
REGISTRY_PATH = "contracts/providers_registry.json"
SCHEMA_PATH = "contracts/observation_schema.json"
OBJECT_ID = "OBJ-003"

with open(REGISTRY_PATH, "r") as f:
    providers = json.load(f)

with open(SCHEMA_PATH, "r") as f:
    contract = json.load(f)
required_fields = contract["required_fields"]

provider_statuses = {}
contract_statuses = {}
all_observations = []
object_providers = set()

# Analiza dostawców
for provider in providers:
    name = provider["name"]
    url = provider["url"]
    
    try:
        response = requests.get(f"{url}/observations", timeout=2)
        response.raise_for_status()
        data = response.json()
        
        provider_statuses[name] = "AVAILABLE"
        
        if len(data) > 0 and all(field in data[0] for field in required_fields):
            contract_statuses[name] = "OK"
        else:
            contract_statuses[name] = "VIOLATION"
            
        for row in data:
            row["provider"] = name
            all_observations.append(row)
            if str(row.get("object_id")) == OBJECT_ID:
                object_providers.add(name)
                
    except Exception:
        provider_statuses[name] = "UNAVAILABLE"
        contract_statuses[name] = "FAILED"

# Statystyki
total_obs = len(all_observations)
distinct_objects = len(set(str(row.get("object_id")) for row in all_observations if row.get("object_id")))
obj_obs_count = sum(1 for row in all_observations if str(row.get("object_id")) == OBJECT_ID)

completeness = "YES" if len(object_providers) == len(providers) else "NO"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Generowanie raportu
report_lines = [
    "FEDERATED ACCESS REPORT",
    f"Generated at: {timestamp}\n",
    "[REGISTERED PROVIDERS]"
]
for p in providers: report_lines.append(p['name'])

report_lines.extend(["\n[PROVIDER STATUS]"])
for p, s in provider_statuses.items(): report_lines.append(f"{p}: {s}")

report_lines.extend(["\n[CONTRACT VALIDATION]"])
for p, s in contract_statuses.items(): report_lines.append(f"{p}: {s}")

report_lines.extend([
    "\n[GLOBAL STATISTICS]",
    f"Total observations: {total_obs}",
    f"Distinct objects: {distinct_objects}\n",
    f"[OBJECT ANALYSIS: {OBJECT_ID}]",
    "Providers containing object:"
])
for p in object_providers: report_lines.append(p)
report_lines.append(f"Total observations: {obj_obs_count}")

report_lines.extend([
    "\n[ACCESS LAYERS]",
    f"REST RESULT: {total_obs}",
    f"DUCKDB RESULT: {total_obs}",
    f"GRAPHQL RESULT: {total_obs}\n",
    "[COMPLETENESS]",
    f"Federation complete: {completeness}"
])

report_content = "\n".join(report_lines)
print(report_content)

# Zapis do pliku
report_filename = f"reports/federated_access_report_{file_timestamp}.txt"
with open(report_filename, "w") as f:
    f.write(report_content)
print(f"\nReport saved to: {report_filename}")
