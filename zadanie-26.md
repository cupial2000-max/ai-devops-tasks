
# Zadanie 26: Analiza i poprawa istniejącego Jenkinsfile

## 1. Cel zadania

Celem zadania była analiza przykładowego pliku Jenkinsfile,
identyfikacja błędów w jego konfiguracji oraz przygotowanie
poprawionej wersji potoku CI/CD.

## 2. Znalezione błędy

### Błąd 1 – Literówka w nazwie sekcji

Oryginalny zapis:
`stesp`

Poprawiony zapis:
`steps`

Wyjaśnienie:
W konfiguracji Jenkins Declarative Pipeline prawidłowa nazwa
sekcji zawierającej polecenia do wykonania to `steps`.
Literówka powodowała błąd składniowy.

### Błąd 2 – Nieprawidłowe polecenie budowania aplikacji

Oryginalny zapis:
`npm build`

Poprawiony zapis:
`npm run build`

Wyjaśnienie:
Polecenie `npm run build` uruchamia skrypt build zdefiniowany
w pliku package.json. Oryginalny zapis nie jest standardowym
sposobem uruchamiania takiego skryptu.

### Błąd 3 – Nieodpowiedni typ polecenia powłoki

Oryginalny zapis:
`sh`

Poprawiony zapis:
`bat`

Wyjaśnienie:
Polecenie sh jest przeznaczone dla środowisk Unix/Linux.
W przypadku agenta Jenkins działającego w systemie Windows
należy używać polecenia bat do wykonywania poleceń systemowych.

### Błąd 4 – Umiejscowienie warunku when

Oryginalny zapis:
Warunek when znajdował się za sekcją steps.

Poprawiony zapis:
Warunek when został umieszczony przed sekcją steps.

Wyjaśnienie:
Warunek when określa, czy dany etap potoku ma zostać wykonany.
Przeniesiono go przed steps, aby zachować standardową strukturę
Declarative Pipeline i poprawić czytelność konfiguracji.

### Błąd 5 – Jawne określenie tagu obrazu Docker

Oryginalny zapis:
`docker build -t myapp .`

Poprawiony zapis:
`docker build -t myapp:latest .`

Wyjaśnienie:
Dodano jawne określenie tagu latest, aby nazwa obrazu
była zgodna z poleceniem docker push.

## 3. Dodatkowe uwagi

Warunek branch 'master' ogranicza wykonanie etapu Deploy
do gałęzi master. Działa on w przypadku Multibranch Pipeline.

W rzeczywistym środowisku wdrożeniowym konieczne jest również
skonfigurowanie uwierzytelnienia do rejestru Docker oraz
odpowiedniego adresu rejestru.

## 4. Rezultat

Przygotowano trzy pliki:

- Jenkinsfile-with-errors – oryginalna konfiguracja zawierająca błędy.
- Jenkinsfile-fixed – poprawiona konfiguracja potoku CI/CD.
- zadanie-26.md – dokumentacja znalezionych błędów i zastosowanych poprawek.

Poprawiona konfiguracja uwzględnia środowisko Windows
i standardową strukturę Jenkins Declarative Pipeline.
