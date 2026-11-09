# Zadanie 29 – Generowanie szablonu konfiguracji Jenkins

## 1. Cel zadania

Celem zadania jest przygotowanie szablonu Jenkins Configuration as Code (JCasC) w formacie YAML. Rozwiązanie umożliwia automatyczne konfigurowanie serwera Jenkins bez konieczności ręcznego ustawiania wszystkich parametrów przez interfejs przeglądarkowy.

## 2. Czym jest Jenkins Configuration as Code?

Jenkins Configuration as Code (JCasC) to mechanizm pozwalający definiować konfigurację Jenkinsa w pliku YAML.

Dzięki temu można:
- automatycznie ustawiać podstawowe parametry serwera,
- konfigurować narzędzia wykorzystywane podczas budowania aplikacji,
- definiować ustawienia wtyczek,
- automatycznie tworzyć przykładowe zadania,
- łatwo przenosić konfigurację pomiędzy różnymi środowiskami.

## 3. Wykorzystane elementy konfiguracji

### 3.1. Podstawowe ustawienia Jenkins

W sekcji `jenkins` zdefiniowano podstawowe parametry serwera:
- `numExecutors` – liczba równoległych wykonawców zadań,
- `mode` – sposób wykorzystania wykonawców,
- `quietPeriod` – czas oczekiwania przed rozpoczęciem buildu,
- `systemMessage` – komunikat wyświetlany na stronie głównej Jenkins.

Dodatkowo skonfigurowano lokalne konto administratora i podstawowy sposób autoryzacji.

### 3.2. Globalne narzędzia

Sekcja `tool` umożliwia zdefiniowanie narzędzi wykorzystywanych przez zadania Jenkins.

W przygotowanym szablonie uwzględniono:
- Maven – narzędzie do budowania projektów Java,
- Node.js – środowisko uruchomieniowe dla aplikacji JavaScript.

Docker wymaga dodatkowo zainstalowanego silnika Docker oraz dostępnego klienta Docker na odpowiednim agencie Jenkins. Sama deklaracja narzędzia w YAML nie instaluje silnika.

### 3.3. Wtyczki

Do wykorzystania pełnej konfiguracji potrzebne są odpowiednie wtyczki, między innymi:
- Configuration as Code,
- Pipeline,
- Job DSL,
- Git,
- NodeJS,
- Timestamper,
- Docker Pipeline.

Wtyczki należy zainstalować przed zastosowaniem konfiguracji JCasC.

### 3.4. Przykładowe zadanie Pipeline

W sekcji `jobs` zdefiniowano przykładowe zadanie o nazwie `przykladowa-aplikacja`.

Zadanie składa się z następujących etapów:
1. Checkout – pobranie kodu.
2. Build – budowanie aplikacji.
3. Test – uruchomienie testów.
4. Deploy – przykładowy etap wdrożenia.

Zadanie jest tworzone automatycznie przez wtyczkę Job DSL.

## 4. Jak uruchomić konfigurację JCasC?

### Krok 1. Instalacja Jenkins

Należy zainstalować Jenkins i uruchomić serwer. Można wykorzystać instalator dla systemu Windows lub obraz Docker.

### Krok 2. Instalacja wymaganych wtyczek

Po zalogowaniu do Jenkins należy przejść do:

Manage Jenkins → Plugins → Available plugins.

Następnie wyszukać i zainstalować wymagane wtyczki:
- Configuration as Code,
- Pipeline,
- Job DSL,
- Git,
- NodeJS,
- Timestamper,
- Docker Pipeline.

Po instalacji warto zrestartować Jenkins.

### Krok 3. Umieszczenie pliku konfiguracyjnego

Plik `.idea/jenkins-casc.yaml` należy umieścić w katalogu dostępnym dla serwera Jenkins.

Domyślnie JCasC szuka pliku `jenkins.yaml` w katalogu JENKINS_HOME.

Można również wskazać własną lokalizację za pomocą zmiennej środowiskowej `CASC_JENKINS_CONFIG`.

### Krok 4. Konfiguracja zmiennych środowiskowych

Przykładowa konfiguracja w PowerShell:

```powershell
$env:CASC_JENKINS_CONFIG = "C:\jenkins\jenkins-casc.yaml"
$env:JENKINS_ADMIN_ID = "admin"
$env:JENKINS_ADMIN_PASSWORD = "silne_haslo"
```

Hasło powinno być przechowywane bezpiecznie i nie może być umieszczane w publicznym repozytorium.

Zmienne muszą być dostępne dla procesu Jenkins przed uruchomieniem lub ponownym uruchomieniem serwera.

### Krok 5. Uruchomienie i zastosowanie konfiguracji

Po uruchomieniu Jenkins z odpowiednio ustawioną zmienną `CASC_JENKINS_CONFIG` plugin JCasC odczyta plik YAML i zastosuje zdefiniowane ustawienia.

Konfigurację można również przeładować z poziomu interfejsu:

Manage Jenkins → Configuration as Code → Reload existing configuration.

### Krok 6. Weryfikacja konfiguracji

Po załadowaniu pliku należy sprawdzić:
- czy ustawiona została liczba wykonawców,
- czy narzędzia Maven i Node.js są widoczne w konfiguracji globalnej,
- czy konto administratora działa,
- czy utworzyło się zadanie `przykladowa-aplikacja`,
- czy zadanie można uruchomić.

W przypadku błędów należy sprawdzić logi Jenkins oraz poprawność składni YAML.

## 5. Podsumowanie

Jenkins Configuration as Code pozwala automatyzować konfigurację środowiska Jenkins za pomocą plików YAML. Ułatwia to odtwarzanie ustawień, zarządzanie środowiskami i przechowywanie konfiguracji w systemie kontroli wersji.

Przygotowany szablon obejmuje podstawowe ustawienia serwera, narzędzia programistyczne, wymagane wtyczki oraz przykładowe zadanie Pipeline.