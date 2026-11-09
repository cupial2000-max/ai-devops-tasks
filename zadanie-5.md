# Zadanie 5: Wizualizacja ASCII Art

## 1. Pierwszy diagram – podstawowa architektura systemu

### Prompt:
```text
Stwórz prosty diagram ASCII Art przedstawiający połączenie klienta, serwera aplikacji i bazy danych.
```

### Wygenerowany diagram:

```text
+----------+        +-------------------+        +----------------+
|          |        |                   |        |                |
|  KLIENT  | <----> | SERWER APLIKACJI  | <----> | BAZA DANYCH    |
|          |        |                   |        |                |
+----------+        +-------------------+        +----------------+
```

## 2. Drugi diagram – architektura z opisami i przepływem danych

### Prompt:
```text
Dodaj do diagramu opisy elementów i kierunki przepływu danych.
```

### Ulepszony diagram:

```text
       ŻĄDANIE HTTP                    ZAPYTANIE SQL
+------------------+   ------------>  +---------------------+
|                  |                  |                     |
|     KLIENT       |                  |  SERWER APLIKACJI   |
|  (przeglądarka)  |   <------------  |  (logika biznesowa) |
|                  |   ODPOWIEDŹ HTTP |                     |
+------------------+                  +----------+----------+
                                                  |
                                                  |
                                            ZAPYTANIE SQL
                                                  |
                                                  v
                                       +---------------------+
                                       |                     |
                                       |     BAZA DANYCH     |
                                       |   (przechowywanie   |
                                       |       danych)       |
                                       |                     |
                                       +----------+----------+
                                                  |
                                                  |
                                           WYNIKI ZAPYTANIA
                                                  |
                                                  v
                                       +---------------------+
                                       |  SERWER APLIKACJI   |
                                       +---------------------+
```

## 3. Opis działania systemu

1. **Klient** – użytkownik korzysta z aplikacji za pomocą przeglądarki internetowej.
2. **Serwer aplikacji** – odbiera żądania klienta, przetwarza je i realizuje logikę biznesową.
3. **Baza danych** – przechowuje informacje i odpowiada na zapytania serwera.
4. **Przepływ danych** – klient wysyła żądanie do serwera, serwer komunikuje się z bazą danych, a następnie zwraca klientowi odpowiedź.

## 4. Podsumowanie

Diagramy przedstawiają podstawową architekturę systemu składającego się z trzech elementów: klienta, serwera aplikacji oraz bazy danych. Drugi diagram dodatkowo obrazuje kierunki komunikacji i przepływ informacji między poszczególnymi elementami.