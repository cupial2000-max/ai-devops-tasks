# Zadanie 25: Generowanie prostego Jenkinsfile

## 1. Cel zadania

Celem zadania było przygotowanie deklaratywnego potoku Jenkins dla aplikacji Node.js. Pipeline automatyzuje kolejne etapy procesu CI/CD: pobieranie kodu, instalowanie zależności, testowanie, budowanie aplikacji, tworzenie obrazu Docker oraz publikowanie go w rejestrze Docker Hub.

## 2. Wyjaśnienie poszczególnych etapów Jenkinsfile

### 2.1. Konfiguracja pipeline

`pipeline` określa główną strukturę potoku w składni deklaratywnej Jenkinsa.

`agent any` oznacza, że Jenkins może uruchomić zadanie na dowolnym dostępnym agencie.

Sekcja `environment` pozwala zdefiniować zmienne środowiskowe wykorzystywane w kolejnych etapach. W tym przypadku `DOCKER_IMAGE` określa nazwę obrazu Docker, który będzie budowany i publikowany.

### 2.2. Checkout – pobieranie kodu

Etap `Checkout` odpowiada za pobranie kodu źródłowego z repozytorium.

Polecenie `checkout scm` wykorzystuje konfigurację repozytorium przypisaną do zadania Jenkins i pobiera odpowiednią wersję kodu.

Dzięki temu pipeline pracuje na aktualnej wersji projektu.

### 2.3. Install Dependencies – instalacja zależności

Etap `Install Dependencies` instaluje biblioteki i pakiety wymagane przez aplikację Node.js.

Polecenie `npm install` odczytuje plik `package.json` i instaluje wymagane zależności.

Jest to konieczne, aby aplikacja mogła zostać poprawnie przetestowana i zbudowana.

### 2.4. Run Tests – uruchomienie testów

Etap `Run Tests` uruchamia testy aplikacji za pomocą polecenia `npm test`.

Pozwala to sprawdzić, czy aplikacja działa zgodnie z założeniami i czy wprowadzone zmiany nie powodują błędów.

Jeżeli testy zakończą się niepowodzeniem, Jenkins przerwie wykonywanie kolejnych etapów pipeline.

### 2.5. Build Application – budowanie aplikacji

Etap `Build Application` odpowiada za przygotowanie aplikacji do wdrożenia.

Polecenie `npm run build` uruchamia skrypt budowania zdefiniowany w pliku `package.json`.

W zależności od projektu może to oznaczać kompilację kodu, optymalizację plików lub wygenerowanie wersji produkcyjnej aplikacji.

### 2.6. Build Docker Image – budowanie obrazu Docker

Etap `Build Docker Image` tworzy obraz Docker na podstawie pliku `Dockerfile` znajdującego się w katalogu projektu.

Polecenie:

`docker build -t %DOCKER_IMAGE%:%BUILD_NUMBER% .`

buduje obraz i nadaje mu nazwę oraz tag. Zmienna `BUILD_NUMBER` oznacza numer aktualnego wykonania pipeline.

Dzięki temu poszczególne wersje obrazu można łatwo rozróżnić.

### 2.7. Push Docker Image – publikowanie obrazu

Etap `Push Docker Image` odpowiada za przesłanie przygotowanego obrazu do rejestru Docker Hub.

Do uwierzytelnienia wykorzystywane są dane dostępowe zapisane wcześniej w Jenkins Credentials.

Polecenie `docker login` loguje użytkownika do Docker Hub, a `docker push` publikuje obraz w rejestrze.

Po zakończeniu operacji wykonywane jest `docker logout`, które wylogowuje użytkownika.

Dzięki temu gotowy obraz może zostać pobrany i uruchomiony na innym środowisku.

### 2.8. Post – działania końcowe

Sekcja `post` definiuje działania wykonywane po zakończeniu pipeline.

Zawiera trzy warunki:

- `success` – wyświetla komunikat o pomyślnym zakończeniu wszystkich etapów.
- `failure` – wyświetla komunikat informujący o niepowodzeniu pipeline.
- `always` – wyświetla komunikat niezależnie od wyniku wykonania.

## 3. Najlepsze praktyki przy tworzeniu pipeline'ów Jenkins

Podczas tworzenia potoków Jenkins warto stosować następujące zasady:

1. **Podział na etapy** – każdy etap powinien odpowiadać za konkretną czynność, co ułatwia analizowanie błędów.
2. **Bezpieczne przechowywanie danych** – haseł, tokenów i innych poufnych danych nie należy umieszczać bezpośrednio w kodzie Jenkinsfile. Należy korzystać z Jenkins Credentials.
3. **Automatyczne testowanie** – testy powinny być wykonywane przed budowaniem i publikowaniem aplikacji.
4. **Wersjonowanie obrazów** – warto stosować unikalne tagi, np. numer kompilacji, aby łatwo identyfikować poszczególne wersje aplikacji.
5. **Czytelność kodu** – nazwy etapów i komunikaty powinny jasno określać wykonywane operacje.
6. **Obsługa błędów** – warto stosować sekcję `post`, aby informować o wyniku wykonania pipeline.
7. **Ograniczanie uprawnień** – dane dostępowe powinny mieć tylko takie uprawnienia, jakie są niezbędne do wykonania zadania.
8. **Kontrola zależności** – w projektach produkcyjnych warto rozważyć `npm ci` zamiast `npm install`, ponieważ zapewnia instalację zgodną z plikiem `package-lock.json`.

## 4. Podsumowanie

W ramach zadania przygotowano deklaratywny Jenkinsfile automatyzujący podstawowe etapy procesu CI/CD dla aplikacji Node.js.

Pipeline obejmuje pobieranie kodu, instalację zależności, testowanie, budowanie aplikacji, tworzenie obrazu Docker i publikowanie go w Docker Hub.

Zastosowanie takiego rozwiązania pozwala ograniczyć liczbę czynności wykonywanych ręcznie, usprawnić proces tworzenia oprogramowania oraz zwiększyć powtarzalność procesu wdrażania aplikacji.