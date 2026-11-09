# Zadanie 20: Generowanie wyrażeń regularnych

## Problem

Potrzebne jest wyrażenie regularne, które sprawdza format adresu IPv4, na przykład `192.168.1.1`.

Funkcja `isValidIPv4` w pliku `ipv4-validator.js` zwraca `true` albo `false` na podstawie tego wzorca:

```text
^(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$
```

## Jak działa wyrażenie

`^` i `$` oznaczają początek i koniec tekstu. Adres nie może mieć nic przed sobą ani za sobą.

Jeden oktet (liczba między kropkami) to alternatywa, od najbardziej szczegółowej:

| Fragment | Jakie liczby łapie |
| --- | --- |
| `25[0-5]` | 250–255 |
| `2[0-4]\d` | 200–249 |
| `1\d{2}` | 100–199 |
| `[1-9]?\d` | 0–99, bez zera na początku przy liczbach dwucyfrowych |

`\d` to jedna cyfra. `[1-9]?` to opcjonalna cyfra od 1 do 9, więc `0` przechodzi, a `01` już nie: po pierwszej cyfrze zostaje druga, której wzorzec nie pochłania.

`(?:oktet\.){3}` powtarza „liczba i kropka” dokładnie trzy razy. Na końcu jest czwarty oktet, już bez kropki. Razem są cztery liczby rozdzielone trzema kropkami, każda z zakresu 0–255.

## Przykłady

Poprawne:

| Adres | Wynik | Dlaczego |
| --- | --- | --- |
| `192.168.1.1` | poprawny | cztery oktety, każdy w zakresie |
| `0.0.0.0` | poprawny | zero jest dozwolone |
| `255.255.255.255` | poprawny | górna granica oktetu |
| `10.0.0.1` | poprawny | zwykły adres prywatny |

Niepoprawne:

| Adres | Wynik | Dlaczego |
| --- | --- | --- |
| `256.1.1.1` | niepoprawny | 256 jest większe niż 255 |
| `192.168.1` | niepoprawny | tylko trzy oktety |
| `192.168.1.1.5` | niepoprawny | pięć oktetów |
| `192.168.01.1` | niepoprawny | zero wiodące w `01` |
| `192.168.1.` | niepoprawny | pusta końcówka po kropce |
| `abc.def.ghi.jkl` | niepoprawny | to nie są liczby |

Ten sam wzorzec sprawdzony w PowerShellu daje wyniki z tabeli. Funkcja `isValidIPv4` nie była uruchamiana przez Node, bo `node` nie jest dostępny w ścieżce.
