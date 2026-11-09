# Zadanie 19: Generowanie prostej dokumentacji

## Prompt

Stwórz dokumentację tego endpointu w formacie Markdown, zawierającą opis, parametry, przykładowe żądanie i odpowiedź.

Opis wejściowy podawał tylko ścieżkę `GET /api/users`, fakt zwracania listy użytkowników oraz trzy parametry: `page`, `limit` i `role`. Wygenerowany tekst jest w `api-docs.md`.

## Refleksja

Dokumentacja dobrze pokrywa to, co było w opisie. Tabela parametrów ma domyślne wartości i maksimum `limit`, a przykładowe żądanie pokazuje wszystkie trzy parametry naraz. Tyle da się oprzeć wprost na poleceniu.

Reszta jest dopowiedziana. Prompt nie podawał kształtu użytkownika, więc pola `id`, `name`, `email` i `role` oraz opakowanie `page`, `limit` i `users` są propozycją, nie kontraktem API. To samo dotyczy kodu `400` i treści błędu: w wymaganiach nie było ani statusów, ani uwierzytelniania, ani tego, co się dzieje przy pustej liście.

Taka dokumentacja nadaje się jako szkic do uzupełnienia. Przed wstawieniem jej do repozytorium projektu trzeba sprawdzić prawdziwą odpowiedź serwera i dopisać to, czego model nie mógł wiedzieć: wymagane nagłówki, kody błędów i dokładne nazwy pól.
