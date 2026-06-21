-- 1. Upewniamy się, że moduł sieciowy jest załadowany
INSTALL httpfs;
LOAD httpfs;

-- 2. Tworzymy główny "widok" (wirtualną tabelę), która skleja 3 serwery
CREATE OR REPLACE VIEW federated_observations AS
SELECT 'satellite_A' AS provider, * FROM 'http://127.0.0.1:8001/observations.csv'
UNION ALL
SELECT 'satellite_B' AS provider, * FROM 'http://127.0.0.1:8002/observations.csv'
UNION ALL
SELECT 'ground_station' AS provider, * FROM 'http://127.0.0.1:8003/observations.csv';

-- 3. Obliczamy całkowitą liczbę obserwacji
SELECT 'TOTAL OBSERVATIONS' AS metric, count(*) AS value FROM federated_observations;

-- 4. Szukamy wyłącznie obserwacji dla obiektu OBJ-003
SELECT 'OBJ-003 OBSERVATIONS' AS metric, count(*) AS value FROM federated_observations WHERE object_id = 'OBJ-003';

-- 5. Liczymy rekordy z podziałem na dostawcę (największy będzie na samej górze)
SELECT provider, count(*) AS count 
FROM federated_observations 
GROUP BY provider 
ORDER BY count DESC;
