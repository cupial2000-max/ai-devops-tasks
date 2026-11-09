# Zadanie 23: Analiza złożoności algorytmu

## Pytanie

Jaka jest złożoność czasowa i pamięciowa tego algorytmu? Czy można go zoptymalizować?

Oryginał jest w `find-pairs.js`. Wersja z jedną pętlą jest w `find-pairs-optimized.js`.

## Złożoność oryginału

Dla tablicy o długości `n` zewnętrzna pętla wykonuje się `n` razy, a wewnętrzna dla indeksu `i` przegląda jeszcze `n - i - 1` elementów. Liczba sprawdzeń sumy to `n * (n - 1) / 2`.

Złożoność czasowa jest więc **O(n²)**. Każda para indeksów jest oglądana nawet wtedy, gdy pasujących par jest mało.

Pamięć poza wynikiem jest stała: kilka zmiennych pętli. Lista `pairs` rośnie z liczbą znalezionych par `p`. Złożoność pamięciowa wyniku to **O(p)**, a dodatkowa pamięć algorytmu to **O(1)**. W najgorszym razie prawie każde dwa elementy tworzą parę i `p` jest rzędu n².

## Optymalizacja

Zamiast drugiej pętli wystarczy pamiętać, ile razy każda wartość już wystąpiła. Dla elementu `arr[j]` dopełnienie to `targetSum - arr[j]`. Jeśli ta liczba jest w mapie, każda jej wcześniejsza kopia tworzy parę z bieżącym elementem. Dopiero potem bieżąca liczba trafia do mapy, więc para nie łączy elementu z samym sobą i zachowuje kolejność z oryginału: najpierw wcześniejszy element, potem późniejszy.

Dla `[1, 4, 2, 3]` i sumy `5` obie funkcje zwracają `[[1, 4], [2, 3]]`.

Mapa ma co najwyżej `n` kluczy, więc dodatkowa pamięć to **O(n)** plus **O(p)** na wynik. Czas to **O(n + p)**: jedno przejście tablicy i dopisanie każdej znalezionej pary. Gdy par jest mało, jest to liniowe względem `n`. Gdy par jest rzędu n², wypisanie ich i tak zajmuje czas kwadratowy. Żaden algorytm nie zwróci kwadratowej liczby par szybciej niż w czasie zależnym od ich liczby.

Mapa zakłada, że elementy da się użyć jako klucze. Dla liczb, tak jak w tej funkcji, ten warunek jest spełniony.
