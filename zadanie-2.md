# Zadanie 2: Porównanie odpowiedzi różnych modeli

**Pytanie:** Wymień 5 korzyści z używania kontenerów Docker w środowisku programistycznym.

## Odpowiedź ChatGPT

Oto 5 najważniejszych korzyści z używania kontenerów Docker w środowisku programistycznym:

1. Izolacja środowiska – każdy kontener działa niezależnie od pozostałych, dzięki czemu aplikacje mogą korzystać z różnych wersji bibliotek i zależności bez wzajemnych konfliktów.

2. Przenośność – kontenery można uruchamiać na różnych systemach i komputerach, np. Windows, Linux czy macOS, zachowując takie samo środowisko działania aplikacji.

3. Powtarzalność środowiska – Docker pozwala zapewnić wszystkim członkom zespołu takie same warunki pracy, co ogranicza problemy wynikające z różnic w konfiguracji komputerów.

4. Szybkie uruchamianie aplikacji – kontenery uruchamiają się znacznie szybciej niż tradycyjne maszyny wirtualne, ponieważ współdzielą jądro systemu operacyjnego.

5. Łatwiejsze wdrażanie i skalowanie – Docker upraszcza przenoszenie aplikacji między środowiskami programistycznymi, testowymi i produkcyjnymi oraz umożliwia łatwe uruchamianie wielu instancji aplikacji.

Podsumowanie: Docker ułatwia pracę programistom, zapewnia spójność środowiska, ogranicza problemy z zależnościami i przyspiesza proces tworzenia, testowania oraz wdrażania oprogramowania.

## Odpowiedź Cursora (Grok)

Pięć korzyści z Dockera w codziennej pracy programisty:

1. **Jedno środowisko dla całego zespołu.** Zamiast instrukcji „zainstaluj Node 20, Pythona 3.12 i Postgresa 16” w repozytorium leży `Dockerfile` albo `docker-compose.yml`. Nowy członek zespołu odpala `docker compose up` i dostaje tę samą wersję bazy, cache i aplikacji, niezależnie od tego, czy pracuje na Windowsie, macOS czy Linuxie.

2. **Brak konfliktów zależności na własnym komputerze.** Projekt A może używać Pythona 3.10, a projekt B Pythona 3.13. Kontenery trzymają te wersje osobno, więc nie trzeba przełączać globalnych instalacji ani wirtualnych środowisk systemowych.

3. **Szybki reset stanu.** Bazę z testowymi danymi, kolejkę albo cache da się wyrzucić i postawić od nowa jedną komendą (`docker compose down -v` i ponowne `up`). Nie zostają „brudne” lokalne instalacje po nieudanym eksperymencie.

4. **Usługi pomocnicze bez ręcznej instalacji.** Postgres, Redis, nginx czy broker wiadomości startują jako osobne kontenery obok aplikacji. Programista nie instaluje ich w systemie operacyjnym i nie pilnuje portów oraz ścieżek danych na własną rękę — opisuje je w Compose i montuje dane wolumenem, np. `postgres_data:/var/lib/postgresql/data`.

5. **Ten sam artefakt idzie dalej w pipeline.** Obraz zbudowany lokalnie (`docker build -t app:dev .`) jest tym, co później buduje CI i wdraża na test albo produkcję. Mniej jest sytuacji typu „u mnie działa”, bo różnica między laptopem a serwerem sprowadza się do konfiguracji, a nie do innego zestawu bibliotek.

## Porównanie

Obie odpowiedzi wymieniają te same osie: izolację, przenośność, spójność zespołu, szybkość względem maszyn wirtualnych albo resetu oraz łatwiejsze przejście między środowiskami. Różnią się szczegółowością i przykładami.

ChatGPT jest krótszy i bardziej ogólny. Każdy punkt to jedno zdanie z nazwą korzyści i skutkiem, bez nazw plików, komend ani konkretnych usług. Na końcu dodaje własne podsumowanie całego zestawienia. Porównanie z maszynami wirtualnymi (współdzielone jądro, szybszy start) pojawia się wprost w punkcie 4.

Odpowiedź Cursora jest dłuższa i opiera się na przykładach z pracy programisty: `Dockerfile`, `docker-compose.yml`, `docker compose up`, `docker compose down -v`, obraz `app:dev` oraz usługi takie jak Postgres, Redis i nginx. Szybkość startu względem VM schodzi na dalszy plan; zamiast tego jest reset stanu wolumenów i ten sam obraz w CI. ChatGPT mocniej podkreśla skalowanie wielu instancji, Cursor — powtarzalny artefakt od laptopa do pipeline’u.
