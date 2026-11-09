# Zadanie 9: Weryfikacja prostego YAML

## Pytanie

Czy ten plik YAML jest poprawny? Jeśli nie, popraw błędy.

## Oryginalny plik

```yaml
services:
  web:
    image: nginx
    ports:
      - "80:80"
  app:
    build: .
    ports
      - "3000:3000"
    depends_on:
      - db
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD=password
```

## Znalezione błędy

Plik nie jest poprawnym YAML-em. Usługa `web` jest zapisana dobrze. Dwa błędy są w `app` i `db`.

1. **Brak dwukropka po `ports` w usłudze `app`.** W YAML klucz mapy musi kończyć się dwukropkiem. Linia `ports` jest zwykłym tekstem, a pod nią zaczyna się lista `- "3000:3000"`. Parser zatrzymuje się w tym miejscu, więc reszta pliku nie zostanie wczytana. W usłudze `web` ta sama lista jest zapisana poprawnie: `ports:`.

2. **`POSTGRES_PASSWORD=password` nie jest wpisem mapy.** Pod `environment:` oczekiwany jest klucz i wartość rozdzielone dwukropkiem albo lista napisów. Zapis ze znakiem `=` nie ustawia zmiennej `POSTGRES_PASSWORD`. Docker Compose przyjmuje tu jedną z dwóch form: `POSTGRES_PASSWORD: password` albo `- POSTGRES_PASSWORD=password`.

## Poprawiona wersja

```yaml
services:
  web:
    image: nginx
    ports:
      - "80:80"
  app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: password
```

Zmiany: po `ports` w usłudze `app` jest dwukropek, a hasło Postgresa jest zapisane jako `POSTGRES_PASSWORD: password`.
