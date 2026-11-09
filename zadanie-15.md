# Zadanie 15: Refaktoryzacja prostej funkcji

## Prompt

Zrefaktoryzuj tę funkcję, aby była bardziej czytelna i łatwiejsza w utrzymaniu.

Oryginał jest w `config.js`. Wersja po zmianie jest w `config-refactored.js`.

## Co się zmieniło

Łańcuch `if` / `else if` / `else` został zastąpiony obiektem `environmentConfigs`. Klucz to nazwa środowiska (`development`, `testing`, `staging`, `production`), wartość to jego ustawienia.

Funkcja robi teraz dwie rzeczy: bierze wpis dla podanego `env`, a gdy takiego klucza nie ma, bierze `development`. `{ ...config }` zwraca kopię obiektu. Dzięki temu wywołujący nie nadpisze wspólnej konfiguracji, tak jak w oryginale, gdzie każde wywołanie tworzyło nowy obiekt.

Gałąź `else` z oryginału zwracała te same wartości co `development`. W nowej wersji ten sam efekt daje `|| environmentConfigs.development`.

## Korzyści

- Nowy wariant, na przykład `qa`, to jeden wpis w obiekcie, bez dokładania kolejnego `else if`.
- Wartości stoją obok siebie, więc różnice między środowiskami widać bez czytania warunków.
- Funkcja nie powtarza pięciu prawie takich samych `return`.
- Wynik dla czterech nazwanych środowisk i dla nieznanej nazwy zostaje taki sam jak wcześniej.
