# Zadanie 21: Transformacja danych

## Polecenie

Przekształć te dane JSON do formatu CSV z kolumnami: id, name, email, roles.

Oryginał jest w `users.json`. Wynik jest w `users.csv`.

## Jak przebiegła konwersja

JSON ma jeden obiekt z tablicą `users`. CSV nie ma zagnieżdżenia, więc każdy element tej tablicy stał się jednym wierszem. Klucze obiektu stały się kolumnami w kolejności z polecenia: `id`, `name`, `email`, `roles`.

Pole `roles` w JSON-ie jest tablicą napisów. W CSV komórka jest jednym tekstem, więc role są sklejone średnikiem: `admin;user` i `user`. Średnik nie jest tu separatorem kolumn. Kolumny rozdziela przecinek.

## Wyzwania

**Tablica w płaskim pliku.** CSV nie ma typu „lista”. Trzeba umówić się, jak ją zapisać. Średnik jest czytelny przy krótkich rolach. Inne możliwości to osobny wiersz na każdą rolę albo wstawienie do komórki fragmentu JSON, na przykład `["admin","user"]`. Osobne wiersze powielają `id`, `name` i `email`. Fragment JSON trzeba potem parsować drugi raz.

**Znak w wartości.** Gdyby rola sama zawierała średnik, sklejenie przestałoby być jednoznaczne. To samo dotyczy przecinka w nazwisku: takie pole trzeba objąć cudzysłowem, a cudzysłów wewnątrz pola podwoić. W tych dwóch rekordach nie było przecinka ani cudzysłowu, więc pola nie są dodatkowo cytowane.

**Kształt danych.** Ta konwersja działa, bo każdy użytkownik ma te same cztery pola, a `roles` zawiera tylko napisy. Głębszy obiekt, brakujące pole albo liczba pomieszana z tekstem wymaga osobnej reguły: puste pole, wartość domyślna albo rezygnacja z jednego arkusza.
