# Federated EO Data Space - National Flood Monitoring

## O projekcie
Wykonałem ten projekt w celu wsparcia National Flood Monitoring Agency. Zaprojektowałem i zaimplementowałem sfederowaną przestrzeń danych ułatwiającą odkrywanie i używanie zasobów Earth Observation (EO).

## Etap 1: Eksploracja i selekcja zasobów
Zbadałem dostępne ekosystemy i wybrałem następujące zasoby operacyjne:

* **Sentinel-1 (SAR):** Wybrałem ten satelitę jako główne narzędzie, ponieważ pozwala na ocenę zasięgu powodzi niezależnie od warunków pogodowych (chmury) oraz w nocy.
* **Sentinel-2 (Optyczny):** Zaimplementowałem go do precyzyjnego mapowania terenów zalanych w warunkach bezchmurnych.
* **Copernicus EMS:** Wykorzystałem tę usługę jako kluczowe wsparcie dla działań reagowania kryzysowego (Emergency Response).
* **EUMETSAT:** Dodałem to źródło, ponieważ wczesne ostrzeganie opiera się na ciągłym monitorowaniu warunków meteorologicznych.

Wykonałem selekcję tak, aby każdy zasób odpowiadał na konkretne wymaganie operacyjne systemu wczesnego ostrzegania.

## Etap 2: Uruchomienie katalogu
Zaimplementowałem katalog w formie lekkiej aplikacji webowej wspierającej filtrowanie i wyszukiwanie zasobów pochodzących od wielu dostawców.

**Jak uruchomić:**
1. Sklonuj repozytorium.
2. Otwórz plik `index.html` w dowolnej przeglądarce internetowej.
3. Użyj paska wyszukiwania, aby filtrować zasoby po tagach (np. "night", "radar").
