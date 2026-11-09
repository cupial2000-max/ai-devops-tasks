# Zadanie 17: Generowanie kodu na podstawie opisu

## Wymagania

Funkcja JavaScript ma:

- przyjąć tablicę obiektów z polami `id`, `title` i `status`,
- zostawić tylko zadania o statusie `"completed"`,
- posortować je według `id` rosnąco,
- zwrócić tablicę samych tytułów.

Implementacja jest w `task-filter.js`, w funkcji `getCompletedTaskTitles`.

## Jak to jest zrobione

Łańcuch ma cztery kroki:

1. `filter` zostawia obiekty, których `status` jest dokładnie `"completed"`.
2. `slice` kopiuje tę tablicę, żeby `sort` nie zmieniał listy przekazanej do funkcji.
3. `sort((a, b) => a.id - b.id)` układa zadania od najmniejszego `id`.
4. `map` bierze z każdego obiektu tylko `title`.

## Przykład

```javascript
const getCompletedTaskTitles = require("./task-filter");

const tasks = [
  { id: 3, title: "Napisać testy", status: "completed" },
  { id: 1, title: "Postawić bazę", status: "completed" },
  { id: 2, title: "Zrobić review", status: "open" },
  { id: 4, title: "Wdrożyć aplikację", status: "completed" }
];

getCompletedTaskTitles(tasks);
// ["Postawić bazę", "Napisać testy", "Wdrożyć aplikację"]
```

Zadanie o `id` 2 odpada, bo ma status `"open"`. Zostają trzy tytuły w kolejności identyfikatorów 1, 3, 4.
