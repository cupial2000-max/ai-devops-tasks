# Zadanie 22: Generowanie README dla projektu

## Polecenie

Stwórz prosty plik README.md dla tego projektu, zawierający sekcje: opis, instalacja, użycie, endpointy API.

Wygenerowany tekst jest w `project-readme.md`. Nie zastępuje on `README.md` tego repozytorium, bo to repozytorium jest zbiorem zadań, a nie aplikacją Simple Task API.

## Uwagi o jakości

Sekcje są zgodne z poleceniem: opis, instalacja, użycie i tabela endpointów. Opis oddaje trzy podane funkcje, czyli CRUD zadań, filtr statusu i priorytetu oraz prostą autoryzację. Przykłady `curl` pokazują, w jakiej kolejności z tego API skorzystać.

Reszta jest dopowiedziana, bo w opisie projektu nie było ścieżek, pól zadania ani sposobu logowania. Nazwy `/api/tasks` i `/api/auth/login`, pola `title`, `status`, `priority` oraz nagłówek `Bearer` są propozycją czytelną dla takiego API, a nie odczytem z kodu. Kroki `npm install` i plik `.env` też wynikają z typowego projektu Node.js, a nie z istniejącego `package.json`.

Dokumentacja wygląda kompletnie, ale da się nią wprowadzić w błąd: czytelnik może uznać, że te polecenia działają w tym katalogu. Przed użyciem jej przy prawdziwej aplikacji trzeba zestawić ścieżki, zmienne środowiskowe i kody odpowiedzi z kodem serwera.
