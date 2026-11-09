# Zadanie 12: Optymalizacja prostego skryptu

## Pytanie

Czy ten kod można zoptymalizować? Jeśli tak, zaproponuj bardziej wydajną wersję.

## Oryginalna wersja

```python
def find_duplicates(list_of_items):
    duplicates = []
    for i in range(len(list_of_items)):
        for j in range(i+1, len(list_of_items)):
            if list_of_items[i] == list_of_items[j] and list_of_items[i] not in duplicates:
                duplicates.append(list_of_items[i])
    return duplicates
```

Funkcja zwraca wartości, które występują na liście co najmniej dwa razy. Każda taka wartość jest na liście wyniku tylko raz, w kolejności pierwszego znalezienia pary.

## Zoptymalizowana wersja

```python
def find_duplicates(list_of_items):
    seen = set()
    duplicates = []

    for item in list_of_items:
        if item in seen:
            if item not in duplicates:
                duplicates.append(item)
        else:
            seen.add(item)

    return duplicates
```

Dla samych porównań „czy już widziałem” drugi zbiór jest szybszy niż `item not in duplicates` na liście:

```python
def find_duplicates(list_of_items):
    seen = set()
    already_reported = set()
    duplicates = []

    for item in list_of_items:
        if item in seen:
            if item not in already_reported:
                already_reported.add(item)
                duplicates.append(item)
        else:
            seen.add(item)

    return duplicates
```

## Co się zmienia

Oryginał dla każdego elementu o indeksie `i` przegląda całą resztę listy (`j` od `i + 1`). To jest około `n * n / 2` porównań. Dodatkowo `list_of_items[i] not in duplicates` przy każdym porównaniu przechodzi listę wyników. Przy `n` elementach czas rośnie jak kwadrat liczby elementów.

Nowa wersja przechodzi listę raz. Zbiór `seen` pamięta wartości już spotkane, a sprawdzenie `item in seen` jest szybkie, niezależne od długości listy. Wartość trafia do wyniku przy drugim wystąpieniu i dzięki `already_reported` nie trafia tam ponownie.

Kolejność wyniku zostaje taka jak w oryginale: duplikat pojawia się w momencie drugiego napotkania, nie na końcu po posortowaniu.

Zbiór w Pythonie przyjmuje tylko elementy, które da się haszować (liczby, napisy, krotki). Oryginał używa `==`, więc działa też dla list i słowników w środku listy. Jeśli elementy nie są haszowalne, zostaje wersja z pętlami.

Przykład: `find_duplicates([1, 2, 1, 3, 2, 1])` w obu wersjach zwraca `[1, 2]`.
