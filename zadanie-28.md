# Zadanie 28 – Skrypt do zarządzania zadaniami Jenkins

## 1. Cel skryptu

Celem skryptu `jenkins-manager.py` jest automatyzacja podstawowych operacji związanych z zarządzaniem zadaniami (jobs) w Jenkinsie. Skrypt komunikuje się z Jenkins za pomocą REST API, dzięki czemu można wykonywać wybrane operacje bez konieczności korzystania z interfejsu przeglądarkowego.

Skrypt umożliwia:
- wyświetlanie listy wszystkich zadań Jenkins,
- sprawdzanie statusu ostatniego buildu wybranego zadania,
- uruchamianie wskazanego zadania.

## 2. Wykorzystane biblioteki

W skrypcie wykorzystano następujące biblioteki Pythona:

- **requests** – biblioteka umożliwiająca wysyłanie zapytań HTTP do Jenkins REST API. Pozwala pobierać informacje o zadaniach oraz uruchamiać buildy.
- **os** – umożliwia odczytywanie zmiennych środowiskowych, w których przechowywane są dane konfiguracyjne i dostępowe do Jenkins.
- **argparse** – odpowiada za obsługę argumentów przekazywanych podczas uruchamiania skryptu z poziomu terminala.
- **requests.auth.HTTPBasicAuth** – zapewnia autoryzację HTTP za pomocą loginu i API Token.

## 3. Sposób działania skryptu

### 3.1. Konfiguracja i autoryzacja

Na początku skrypt pobiera adres serwera Jenkins, nazwę użytkownika oraz API Token ze zmiennych środowiskowych. Następnie tworzy sesję HTTP, która wykorzystuje dane logowania do autoryzacji zapytań.

Dzięki temu dane dostępowe nie muszą być umieszczane bezpośrednio w kodzie programu.

### 3.2. Wysyłanie zapytań do API

Funkcja `make_request()` odpowiada za komunikację z Jenkins. Wykonuje zapytania HTTP i obsługuje ewentualne błędy, takie jak:
- brak połączenia z serwerem,
- przekroczenie czasu oczekiwania,
- błędy HTTP,
- inne problemy związane z zapytaniami.

### 3.3. Listowanie zadań

Funkcja `list_jobs()` wysyła zapytanie do endpointu `/api/json`. Pobiera nazwy wszystkich dostępnych zadań oraz informacje o ich statusie.

Wyniki są wyświetlane w terminalu.

### 3.4. Sprawdzanie statusu buildów

Funkcja `check_status()` pobiera informacje o ostatnim buildzie wskazanego zadania.

Wyświetla numer buildu oraz jego status. Możliwe wyniki to między innymi:
- `SUCCESS` – build zakończył się powodzeniem,
- `FAILURE` – build zakończył się błędem,
- `UNSTABLE` – build zakończył się niestabilnie,
- `BUILD W TRAKCIE` – build jest aktualnie wykonywany.

Jeśli zadanie nie było jeszcze uruchamiane, skrypt wyświetla odpowiedni komunikat.

### 3.5. Uruchamianie zadania

Funkcja `run_job()` wysyła zapytanie HTTP POST do endpointu `/job/nazwa_zadania/build`. Powoduje to zlecenie Jenkinsowi uruchomienia wskazanego zadania.

Skrypt informuje użytkownika o wysłaniu żądania oraz wyświetla kod odpowiedzi HTTP.

### 3.6. Obsługa argumentów

Biblioteka `argparse` pozwala wybrać operację bez modyfikowania kodu programu. Użytkownik może wywołać skrypt z jednym z trzech poleceń: `list`, `status` lub `run`.

## 4. Przykładowe użycie skryptu

Przed uruchomieniem należy zainstalować bibliotekę requests:

```bash
py -m pip install requests
```

Następnie należy skonfigurować zmienne środowiskowe zawierające adres Jenkins, login i API Token.

**Wyświetlenie wszystkich zadań:**

```bash
py jenkins-manager.py list
```

**Sprawdzenie statusu ostatniego buildu:**

```bash
py jenkins-manager.py status nazwa_zadania
```

**Uruchomienie wybranego zadania:**

```bash
py jenkins-manager.py run nazwa_zadania
```

## 5. Podsumowanie

Przygotowany skrypt umożliwia podstawową automatyzację zarządzania zadaniami Jenkins za pomocą Pythona i REST API.

Wykorzystanie biblioteki requests pozwala na łatwą komunikację z serwerem, a argparse umożliwia wygodne wybieranie operacji z poziomu terminala. Dodatkowo zastosowanie API Token oraz obsługi błędów zwiększa bezpieczeństwo i niezawodność rozwiązania.

Skrypt może być w przyszłości rozbudowany o dodatkowe funkcje, takie jak zatrzymywanie buildów, sprawdzanie historii wykonań czy usuwanie zadań.