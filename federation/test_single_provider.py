import requests

object_id = "OBJ-003"

# 1. Pobieranie wszystkich obserwacji z satellite_A
response_A_all = requests.get("http://127.0.0.1:8001/observations")
data_A_all = response_A_all.json()

# 2. Pobieranie obserwacji dla konkretnego obiektu z satellite_A
response_A_obj = requests.get(f"http://127.0.0.1:8001/observations/{object_id}")
data_A_obj = response_A_obj.json()

# 3. Pobieranie obserwacji dla konkretnego obiektu z satellite_B
response_B_obj = requests.get(f"http://127.0.0.1:8002/observations/{object_id}")
data_B_obj = response_B_obj.json()

# 4. Wyświetlanie wyników zgodnie z instrukcją
print("satellite_A:")
print("NUMBER OF OBSERVATIONS:", len(data_A_all))
print(f"{object_id} RESULTS:", len(data_A_obj))

print("\nsatellite_B:")
print(f"{object_id} RESULTS:", len(data_B_obj))

print("\nCOMPARISON:")
if len(data_A_obj) > 0 and len(data_B_obj) > 0:
    print(f"{object_id} is present in both providers.")
else:
    print(f"{object_id} is not present in both providers.")
