# Zadanie 11: Generowanie prostego testu jednostkowego

## Funkcja

```javascript
function sum(a, b) {
  return a + b;
}
```

Kod funkcji jest w pliku `sum.js`. Na końcu pliku jest `module.exports = sum`, żeby test mógł ją wczytać przez `require`.

## Prompt

Napisz prosty test jednostkowy dla tej funkcji używając Jest. Wyjaśnij, czym jest Jest, jak go zainstalować w projekcie i jak uruchomić ten test. Podaj również strukturę plików projektu.

## Czym jest Jest

Jest to narzędzie do testów w JavaScript. Uruchamia pliki z testami, wywołuje funkcję z różnymi argumentami i sprawdza, czy wynik jest taki, jakiego oczekujesz. Gdy wynik się nie zgadza, wypisuje, co dostał i czego się spodziewał.

W teście `describe` grupuje przypadki jednej funkcji, `test` to jeden przypadek, a `expect(...).toBe(...)` porównuje wynik z oczekiwaną wartością.

## Struktura plików

```text
.
├── sum.js           # funkcja sum
├── sum.test.js      # testy tej funkcji
├── package.json     # powstaje po npm init, tu Jest zapisuje się jako zależność deweloperska
└── node_modules/    # pobrane pakiety, w tym Jest; katalog jest w .gitignore
```

Jest sam znajduje pliki o nazwie kończącej się na `.test.js`, więc `sum.test.js` leżące obok `sum.js` nie wymaga dodatkowej konfiguracji.

## Instalacja

W katalogu projektu:

```bash
npm init -y
npm install --save-dev jest
```

`npm init -y` tworzy `package.json`. `npm install --save-dev jest` dopisuje Jest do `devDependencies` i pobiera go do `node_modules/`.

## Uruchomienie

```bash
npx jest
```

Albo sam ten plik:

```bash
npx jest sum.test.js
```

Zielony wynik i napis o trzech zdanych testach oznaczają, że `sum(2, 3)` zwróciło `5`, `sum(-1, -4)` zwróciło `-5`, a `sum(7, 0)` zwróciło `7`.

## Kod testu

Test jest w pliku `sum.test.js`:

```javascript
const sum = require("./sum");

describe("sum", () => {
  test("dodaje dwie liczby", () => {
    expect(sum(2, 3)).toBe(5);
  });

  test("dodaje liczby ujemne", () => {
    expect(sum(-1, -4)).toBe(-5);
  });

  test("dodaje zero", () => {
    expect(sum(7, 0)).toBe(7);
  });
});
```
