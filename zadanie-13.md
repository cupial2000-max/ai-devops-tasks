# Zadanie 13: Generowanie komentarzy dokumentacyjnych

## Prompt

Dodaj do tej funkcji komentarze dokumentacyjne w formacie JSDoc.

Oryginalna funkcja, bez komentarzy, jest w `fetch-user.js`. Ta sama funkcja z blokiem JSDoc jest w `fetch-user-documented.js`. Działanie kodu się nie zmienia.

## Czym jest JSDoc

JSDoc to komentarz zaczynający się od `/**` i kończący się `*/`, stawiany bezpośrednio nad funkcją. Edytor czyta go przy podpowiedziach, a narzędzia mogą z niego złożyć dokumentację.

W tym komentarzu są trzy części:

- pierwsze zdania opisują, co funkcja robi i co zwraca przy błędzie,
- `@param {number|string} userId` podaje typ i znaczenie argumentu,
- `@returns {Promise<...|null>}` podaje typ wyniku: obietnicę obiektu z polami `name`, `email` i `lastLogin` albo `null`.

Typ w nawiasach klamrowych jest informacją dla człowieka i edytora. Sam JavaScript go nie sprawdza.
