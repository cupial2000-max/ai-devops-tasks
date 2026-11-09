# Zadanie 8: Analiza krótkiego błędu

## Komunikat błędu

```text
ERROR: for app  Cannot start service app: driver failed programming external connectivity on endpoint app (172.18.0.2): Error starting userland proxy: listen tcp4 0.0.0.0:3000: bind: address already in use
```

## Pytanie

Co oznacza ten błąd i jak mogę go rozwiązać?

## Co oznacza ten błąd

Docker nie uruchomił usługi `app`, bo nie mógł otworzyć portu **3000** na hoście.

Fragment `listen tcp4 0.0.0.0:3000: bind: address already in use` mówi wprost: adres `0.0.0.0:3000` jest już zajęty. `0.0.0.0` oznacza „wszystkie interfejsy tej maszyny”, a `bind` to próba zarezerwowania portu. Ktoś inny już nasłuchuje na 3000: inny kontener, poprzedni proces aplikacji albo lokalny serwer deweloperski.

`driver failed programming external connectivity` i `Error starting userland proxy` to skutek, nie przyczyna. Docker tworzy przekierowanie z portu hosta do kontenera (adres kontenera w komunikacie to `172.18.0.2`). Ta operacja pada, bo port na hoście jest zajęty, więc cały start usługi `app` się zatrzymuje.

Sam kontener i obraz są w tym błędzie drugorzędne. Konflikt jest na porcie hosta.

## Jak to rozwiązać

**1. Zobacz, co trzyma port 3000.**

Linux:

```bash
sudo ss -tlnp | grep 3000
```

Albo:

```bash
sudo lsof -i :3000
```

Docker:

```bash
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

W kolumnie `PORTS` szukaj `0.0.0.0:3000` albo `:::3000`.

**2. Zwolnij port albo zmień mapowanie.**

Jeśli to stary kontener tej samej aplikacji:

```bash
docker stop <nazwa>
docker rm <nazwa>
```

Przy Compose, z katalogu projektu:

```bash
docker compose down
docker compose up
```

Jeśli portu potrzebuje inny program (na przykład `npm start` na hoście), zatrzymaj ten program albo w Compose wystaw aplikację na inny port hosta. Po lewej jest port maszyny, po prawej port w kontenerze:

```yaml
services:
  app:
    ports:
      - "3001:3000"
```

Aplikacja w kontenerze dalej słucha na 3000, a z hosta wchodzisz na `http://localhost:3001`.

**3. Uruchom usługę ponownie** i sprawdź, że port należy do nowego kontenera:

```bash
docker compose up
docker ps
```
