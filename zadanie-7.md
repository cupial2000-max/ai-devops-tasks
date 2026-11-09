# Zadanie 7: Wygenerowanie prostego skryptu Bash

## Prompt 1

Napisz prosty skrypt bash, który sprawdza, czy usługa Docker działa, a jeśli nie - próbuje ją uruchomić.

Skrypt jest w pliku `check_docker.sh`.

## Prompt 2

Wyjaśnij działanie tego skryptu linia po linii, tak jakbyś tłumaczył osobie początkującej.

## Wyjaśnienie linia po linii

```bash
#!/usr/bin/env bash
```

Pierwsza linia to shebang. Mówi systemowi, że plik ma uruchomić program `bash`. Dzięki temu po nadaniu prawa do wykonania (`chmod +x check_docker.sh`) można wołać skrypt jako `./check_docker.sh`, a nie tylko przez `bash check_docker.sh`.

```bash
if systemctl is-active --quiet docker; then
```

`if` zaczyna warunek. `systemctl` to narzędzie do usług w systemie (systemd). `is-active docker` pyta, czy usługa o nazwie `docker` jest w tej chwili uruchomiona. `--quiet` chowa tekst odpowiedzi: skrypt interesuje tylko wynik, czyli „tak” albo „nie”. Jeśli usługa działa, wykonywane są polecenia do najbliższego `else`.

```bash
  echo "Usługa Docker działa."
```

`echo` wypisuje tekst na ekran. Ta linia jest wcięta tylko dla czytelności. Bash ignoruje takie spacje na początku linii.

```bash
else
```

`else` oznacza „w przeciwnym razie”. Tu trafiamy, gdy Docker nie działa.

```bash
  echo "Usługa Docker nie działa. Próba uruchomienia..."
```

Informacja dla osoby uruchamiającej skrypt, zanim cokolwiek zostanie zmienione w systemie.

```bash
  sudo systemctl start docker
```

`start docker` prosi system o uruchomienie usługi. `sudo` wykonuje to polecenie z uprawnieniami administratora, bo zwykły użytkownik zwykle nie może włączać usług. System może poprosić o hasło.

```bash
  if systemctl is-active --quiet docker; then
```

Drugi, wewnętrzny warunek. Po próbie startu skrypt sprawdza jeszcze raz, czy usługa naprawdę działa. Samo wywołanie `start` nie gwarantuje sukcesu: usługa może nie istnieć albo paść od razu po starcie.

```bash
    echo "Usługa Docker została uruchomiona."
```

Ten tekst pojawia się tylko wtedy, gdy drugie sprawdzenie wypadło pozytywnie.

```bash
  else
    echo "Nie udało się uruchomić usługi Docker."
    exit 1
```

Gdy po próbie startu Docker nadal nie działa, skrypt wypisuje błąd. `exit 1` kończy skrypt i zwraca kod 1. Kod inny niż 0 oznacza dla systemu i dla innych skryptów, że coś się nie udało. Kod 0 (domyślny, gdy skrypt dojdzie do końca bez `exit`) oznacza sukces.

```bash
  fi
fi
```

Każde `if` musi mieć swoje `fi` (słowo `if` czytane od tyłu). Pierwsze `fi` zamyka wewnętrzne sprawdzenie po starcie, drugie zamyka główne sprawdzenie z początku pliku.
