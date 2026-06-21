import json
import requests
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# 1. Wczytanie rejestru dostawców (ścieżka względna dla folderu gateway)
with open("../contracts/providers_registry.json", "r") as f:
    PROVIDERS = json.load(f)

# 2. Definicja struktury obiektu GraphQL
@strawberry.type
class Observation:
    provider: str
    timestamp: str
    object_id: str
    temperature: float
    velocity: float

# 3. Logika pobierania wszystkich obserwacji (pod spodem używa REST)
def fetch_all():
    results = []
    for provider in PROVIDERS:
        provider_name = provider["name"]
        provider_url = provider["url"]
        try:
            response = requests.get(f"{provider_url}/observations", timeout=2)
            data = response.json()
            for row in data:
                results.append(Observation(
                    provider=provider_name,
                    timestamp=str(row.get("timestamp", "")),
                    object_id=str(row.get("object_id", "")),
                    temperature=float(row.get("temperature", 0.0)),
                    velocity=float(row.get("velocity", 0.0))
                ))
        except Exception as e:
            print(f"Błąd: {provider_name} - {e}")
    return results

# 4. Logika pobierania konkretnego obiektu
def fetch_object(object_id: str):
    results = []
    for provider in PROVIDERS:
        provider_name = provider["name"]
        provider_url = provider["url"]
        try:
            response = requests.get(f"{provider_url}/observations/{object_id}", timeout=2)
            data = response.json()
            for row in data:
                results.append(Observation(
                    provider=provider_name,
                    timestamp=str(row.get("timestamp", "")),
                    object_id=str(row.get("object_id", "")),
                    temperature=float(row.get("temperature", 0.0)),
                    velocity=float(row.get("velocity", 0.0))
                ))
        except Exception as e:
            print(f"Błąd: {provider_name} - {e}")
    return results

# 5. Definicja zapytań (Queries)
@strawberry.type
class Query:
    @strawberry.field
    def observations(self) -> list[Observation]:
        return fetch_all()

    @strawberry.field
    def observations_by_object(self, object_id: str) -> list[Observation]:
        return fetch_object(object_id)

# 6. Uruchomienie aplikacji FastAPI z modułem GraphQL
schema = strawberry.Schema(query=Query)
app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
