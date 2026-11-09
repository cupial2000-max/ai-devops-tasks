
# Zadanie 27 – Wyjaśnienie zależności między etapami pipeline'u Jenkins

## 1. Checkout kodu
Pierwszym etapem jest pobranie kodu źródłowego aplikacji z repozytorium Git, np. GitHub. Jenkins uzyskuje w ten sposób aktualną wersję projektu, która będzie poddawana dalszym procesom.

## 2. Budowanie aplikacji
Jenkins kompiluje kod i przygotowuje aplikację do testowania. Na tym etapie wykrywane są podstawowe błędy związane z budowaniem projektu.

## 3. Testy jednostkowe
Sprawdzane jest działanie poszczególnych funkcji i modułów aplikacji. Pozwala to wykryć błędy na wczesnym etapie.

## 4. Analiza statyczna kodu
Kod jest analizowany bez uruchamiania aplikacji. Weryfikowana jest jego jakość, poprawność oraz zgodność z przyjętymi standardami programowania.

## 5. Skanowanie bezpieczeństwa
Przeprowadzana jest kontrola kodu i zależności pod kątem znanych luk bezpieczeństwa. W przypadku wykrycia poważnych zagrożeń pipeline może zostać zatrzymany.

## 6. Budowanie obrazu Docker
Po pomyślnym przejściu wcześniejszych etapów tworzony jest obraz Docker zawierający aplikację i jej wymagane środowisko uruchomieniowe.

## 7. Testy integracyjne
Sprawdzana jest współpraca poszczególnych modułów aplikacji oraz komunikacja z zewnętrznymi usługami i bazami danych. Testy pozwalają upewnić się, że komponenty działają poprawnie razem.

## 8. Wdrożenie na środowisko staging
Aplikacja zostaje wdrożona na środowisko testowe, które odwzorowuje środowisko produkcyjne. Umożliwia to sprawdzenie działania całego systemu w warunkach zbliżonych do rzeczywistych.

## 9. Testy akceptacyjne
Na środowisku staging przeprowadzana jest końcowa weryfikacja aplikacji. Sprawdzane jest, czy spełnia ona wymagania funkcjonalne i jest gotowa do udostępnienia użytkownikom.

## 10. Wdrożenie na produkcję
Jeżeli wszystkie wcześniejsze etapy zakończą się powodzeniem, aplikacja zostaje wdrożona na środowisko produkcyjne, gdzie mogą korzystać z niej użytkownicy.

## 11. Zatrzymanie pipeline i poprawa błędów
Jeżeli testy akceptacyjne nie zostaną zaliczone, proces wdrożenia zostaje zatrzymany. Programiści analizują błędy, wprowadzają poprawki i ponownie uruchamiają pipeline.

## Podsumowanie

Pipeline CI/CD w Jenkinsie automatyzuje proces dostarczania oprogramowania. Każdy etap zależy od poprawnego zakończenia poprzedniego. Dzięki temu błędy i zagrożenia są wykrywane przed wdrożeniem aplikacji na produkcję.

Podział procesu na kolejne etapy zwiększa jakość, bezpieczeństwo i niezawodność aplikacji oraz ogranicza ryzyko nieudanego wdrożenia.
