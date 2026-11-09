# Zadanie 4 – Określanie roli w promptach

## 1. Pierwszy prompt

Jak rozwiązać problem z dużym zużyciem pamięci przez kontener Docker?

## 2. Pierwsza odpowiedź AI

Najpierw zmierz, co zjada pamięć, potem ogranicz kontener i samą aplikację. Sam obraz Dockera rzadko jest przyczyną wysokiego zużycia RAM w trakcie działania.

### 1. Zobacz, ile naprawdę bierze

```bash
docker stats
```

Kolumna `MEM USAGE / LIMIT` pokazuje zużycie i limit. Jeśli limit to cały RAM hosta, kontener może rosnąć aż do braku pamięci na maszynie.

W środku kontenera sprawdź procesy:

```bash
docker exec -it <nazwa> sh
ps aux --sort=-rss | head
```

### 2. Ustaw limit, żeby nie zabił hosta

W `docker run`:

```bash
docker run -d --name app --memory=512m --memory-swap=512m twoj-obraz
```

W Compose:

```yaml
services:
  app:
    image: twoj-obraz
    mem_limit: 512m
    memswap_limit: 512m
```

`--memory-swap` równe `--memory` wyłącza dodatkowy swap. Po przekroczeniu limitu jądro ubija proces w kontenerze (OOM), a nie cały system. Limit dobierz do realnego zużycia z `docker stats`, z zapasem, a nie „na sztywno” 512 MB.

### 3. Ogranicz stertę aplikacji

Limit Dockera nie zmniejsza apetytu programu. Trzeba zejść do konfiguracji procesu:

- **Node.js:** `NODE_OPTIONS=--max-old-space-size=256` (wartość w MB, poniżej limitu kontenera).
- **Java:** `-Xmx256m`.
- **Python:** mniej workerów (Gunicorn/Uvicorn) — każdy proces trzyma własną kopię pamięci.
- **Bazy w kontenerze** (Postgres, Redis, Elasticsearch): mają własne bufory. Redis trzyma dane w RAM; Postgresa nie zostawiaj z domyślnym `shared_buffers` na małej maszynie.

Częsta przyczyna to wyciek: zużycie w `docker stats` rośnie przez godziny i nie spada po obciążeniu. Wtedy limit tylko wymusza restart. Trzeba znaleźć wyciek w aplikacji (heap snapshot, liczba workerów, cache bez limitu).

### 4. To, co zwykle dokłada RAM bez potrzeby

- Kilka replik tej samej aplikacji na jednym hoście.
- Zbędne usługi w tym samym kontenerze (baza, cache i aplikacja naraz).
- Cache w pamięci bez górnej granicy.
- Logi pisane do pliku wewnątrz kontenera zamiast na stdout — to raczej dysk, ale duży proces logujący też potrafi rosnąć.

Obraz `slim` albo Alpine zmniejsza dysk, nie zużycie RAM działającego procesu.

Praktyczna kolejność: `docker stats` → limit `--memory` → limit sterty i liczby procesów → jeśli krzywa pamięci cały czas rośnie, szukaj wycieku w aplikacji.

## 3. Drugi prompt

Jesteś doświadczonym DevOps Engineerem z 10-letnim doświadczeniem. Jak rozwiązać problem z dużym zużyciem pamięci przez kontener Docker?

## 4. Druga odpowiedź AI

Najpierw ustal, czy kontener naprawdę zjada pamięć, czy tylko podlicza cache jądra. Dopiero potem zmniejszaj limit albo stertę aplikacji.

### Co sprawdzam po kolei

**1. Czy proces został zabity, czy tylko „dużo” pokazuje `docker stats`.**

```bash
docker inspect <nazwa> --format '{{.State.OOMKilled}} {{.State.ExitCode}}'
docker stats --no-stream
```

`OOMKilled=true` oznacza, że cgroup ubił proces po limicie. Sam wysoki odczyt w `docker stats` często obejmuje page cache, który jądro odda, gdy ktoś poprosi o RAM.

**2. Rozbicie pamięci kontenera, nie tylko jedna liczba.**

```bash
docker exec <nazwa> cat /sys/fs/cgroup/memory.current
docker exec <nazwa> cat /sys/fs/cgroup/memory.stat
```

W `memory.stat` patrz na `anon` (pamięć procesów) i `file` (cache plików). Duże `file` przy małym `anon` zwykle nie jest wyciekiem. Duże i rosnące `anon` już tak.

**3. Który proces.**

```bash
docker exec <nazwa> ps aux --sort=-rss
```

Jedna aplikacja, kilka workerów albo sidecar w tym samym kontenerze to trzy różne decyzje.

### Co zmieniam

Limit ustawiam pod zmierzony `anon`, z zapasem około 20–30% na stos, wątki i natywne biblioteki. Sterta języka musi być niższa niż limit kontenera, inaczej proces nie zdąży zwolnić pamięci i dostanie OOM.

```bash
docker run -d --memory=512m --memory-swap=512m \
  -e NODE_OPTIONS=--max-old-space-size=384 \
  twoj-obraz
```

Dla Javy to `-Xmx` wyraźnie poniżej `--memory`. Dla Pythona i Node najczęściej problemem jest liczba workerów: każdy trzyma własną kopię procesu. Cztery workery na kontenerze 512 MB to zwykle za dużo.

W Compose to samo:

```yaml
services:
  app:
    mem_limit: 512m
    memswap_limit: 512m
```

`memswap_limit` równe `mem_limit` wyłącza dokładanie swapu. Swap maskuje wyciek i zabija opóźnienie.

### Kiedy limit nie jest rozwiązaniem

Jeśli `anon` rośnie przez godziny i nie spada po końcu ruchu, to wyciek albo cache bez sufitu. Limit wtedy tylko wymusza restart. Zbieram heap dump albo profil przy szczycie i sprawdzam pule połączeń, lokalny cache i bufory klienta kolejki.

Osobno odcinam rzeczy, które wyglądają jak „pamięć aplikacji”, a są konfiguracją:

- Redis bez `maxmemory` trzyma cały zbiór w RAM.
- Postgres z domyślnym `shared_buffers` na małym hoście.
- Java bez ustawionego `-Xmx` bierze ułamek RAM widzianego przez kontener. Na hoście bez limitu cgroup potrafi wziąć gigabajty.
- Logi i pliki tymczasowe w warstwie zapisu kontenera. To głównie dysk, ale duże bufory zapisu też podbijają RAM.

Obraz Alpine albo `slim` zmniejsza rozmiar obrazu na dysku. Na zużycie RAM działającego procesu prawie nie wpływa.

Krótka ścieżka: `OOMKilled` i `memory.stat` (`anon` kontra `file`), potem limit cgroup, potem sterta i liczba procesów ustawione poniżej tego limitu. Krzywa `anon`, która nie wraca po obciążeniu, to już wyciek w aplikacji, nie „za mały kontener”.

## 5. Porównanie obu odpowiedzi

Oba teksty dotyczą tego samego pytania i prowadzą do tej samej kolejności działań: najpierw pomiar, potem limit kontenera, potem sterta i liczba procesów, a na końcu wyciek, jeśli zużycie nie spada. W obu pojawia się ten sam przykład limitu 512 MB w `docker run` i w Compose, ta sama uwaga o wyłączeniu dodatkowego swapu oraz ta sama końcowa uwaga, że obraz `slim` albo Alpine zmniejsza dysk, a nie RAM działającego procesu.

Różni się punkt startu. Pierwsza odpowiedź od razu mówi: zmierz zużycie i ogranicz kontener oraz aplikację. Druga zaczyna od rozróżnienia, czy kontener naprawdę zużywa pamięć procesów, czy w liczniku widać też cache jądra.

Różni się głębokość diagnostyki.

| Element | Pierwsza odpowiedź | Druga odpowiedź |
| --- | --- | --- |
| Pomiar | `docker stats`, potem `ps aux` w kontenerze | `docker inspect` (`OOMKilled`, kod wyjścia), `docker stats --no-stream`, pliki cgroup `memory.current` i `memory.stat` |
| Co uznaje za problem | Wysokie zużycie i brak limitu na hoście | Osobno page cache (`file`) i pamięć procesów (`anon`); rośnie `anon`, nie sam odczyt `docker stats` |
| Limit aplikacji | Node `--max-old-space-size=256`, Java `-Xmx256m`, mniej workerów Pythona | Limit pod zmierzone `anon`, zapas 20–30%, Node `--max-old-space-size=384` przy limicie 512 MB, Java `-Xmx` poniżej limitu, przykład czterech workerów na 512 MB |
| Przykłady poza aplikacją | Repliki, kilka usług w jednym kontenerze, cache bez limitu, logi do pliku; Postgres, Redis, Elasticsearch | Redis bez `maxmemory`, Postgres `shared_buffers`, Java bez `-Xmx` widząca RAM hosta, pule połączeń, cache, bufory klienta kolejki, pliki tymczasowe w warstwie zapisu |
| Forma | Instrukcja w czterech numerowanych krokach, zakończona skrótem kolejności | Procedura w pierwszej osobie: „Co sprawdzam”, „Co zmieniam”, „Kiedy limit nie jest rozwiązaniem” |

Pierwsza odpowiedź jest krótsza i podaje gotowe wartości sterty (256 MB) obok limitu kontenera 512 MB. Druga jest dłuższa, nie podaje osobnej wartości `-Xmx` i wiąże stertę Node (384 MB) z limitem 512 MB oraz z zapasem na stos i biblioteki natywne. Druga dopowiada też, że swap maskuje wyciek.

## 6. Wnioski

Przypisanie roli doświadczonego DevOps Engineera nie zmieniło kierunku odpowiedzi. Nadal jest to pomiar, limit cgroup, sterta poniżej limitu i szukanie wycieku, gdy zużycie nie wraca.

Rola zmieniła sposób odpowiedzi. Tekst przeszedł z listy porad na procedurę osoby, która najpierw oddziela objaw od przyczyny: OOM, cache jądra i pamięć procesów. Pojawiły się konkretne pliki cgroup, rozróżnienie `anon` i `file` oraz uzasadnienie, dlaczego sterta ma być niższa niż limit kontenera. Liczby nie są bardziej „oficjalne” tylko dlatego, że w promptcie jest staż 10 lat. W pierwszej odpowiedzi Node ma 256 MB, w drugiej 384 MB przy tym samym limicie kontenera 512 MB. Rola zwiększyła szczegółowość diagnostyki i nadała tekstowi formę własnej kolejki sprawdzeń, a nie inną receptę na ten sam problem.
