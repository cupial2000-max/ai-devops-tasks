# Zadanie 4: Określanie roli w promptach

## Prompt 1

Jak rozwiązać problem z dużym zużyciem pamięci przez kontener Docker?

### Odpowiedź

Duże zużycie pamięci przez kontener ogranicza się w dwóch miejscach: limitem Dockera oraz konfiguracją samej aplikacji.

Najpierw sprawdź, ile kontener bierze:

```bash
docker stats
```

Kolumna pamięci pokazuje zużycie i limit. Jeśli limitu nie ma, kontener może rosnąć aż do RAM-u hosta. W środku kontenera zobacz, który proces jest największy:

```bash
docker exec -it <nazwa> ps aux --sort=-rss
```

Potem ustaw górną granicę, na przykład 512 MB, bez dodatkowego swapu:

```bash
docker run -d --name app --memory=512m --memory-swap=512m twoj-obraz
```

W Docker Compose:

```yaml
services:
  app:
    image: twoj-obraz
    mem_limit: 512m
    memswap_limit: 512m
```

Sam limit kontenera nie zmniejsza apetytu programu. Trzeba też ograniczyć stertę:

- Node.js: `NODE_OPTIONS=--max-old-space-size=256`
- Java: `-Xmx256m`
- Python (Gunicorn, Uvicorn): mniej procesów workerów, bo każdy trzyma własną pamięć

Jeśli zużycie rośnie godzinami i nie spada po końcu ruchu, to zwykle wyciek albo cache bez limitu. Wtedy sam limit tylko powoduje restart. Warto też rozdzielić bazę, cache i aplikację na osobne kontenery oraz nie trzymać kilku kopii tej samej aplikacji na małym hoście. Obraz `alpine` albo `slim` zmniejsza rozmiar obrazu na dysku, a nie RAM działającego procesu.

## Prompt 2

Jesteś doświadczonym DevOps Engineerem z 10-letnim doświadczeniem. Jak rozwiązać problem z dużym zużyciem pamięci przez kontener Docker?

### Odpowiedź

Najpierw oddzielam objaw od przyczyny. Wysoka liczba w `docker stats` nie znaczy jeszcze, że aplikacja wycieka.

Sprawdzam, czy jądro ubija proces:

```bash
docker inspect <nazwa> --format '{{.State.OOMKilled}} {{.State.ExitCode}}'
docker stats --no-stream
```

`OOMKilled=true` oznacza, że cgroup ściął kontener po limicie. Potem rozbijam pamięć na pamięć procesów i cache plików:

```bash
docker exec <nazwa> cat /sys/fs/cgroup/memory.current
docker exec <nazwa> cat /sys/fs/cgroup/memory.stat
```

W `memory.stat` pole `anon` to RAM procesów, pole `file` to page cache. Duże `file` przy małym `anon` zwykle odda jądro, gdy inny proces poprosi o pamięć. Rosnące `anon` to już proces, worker albo sidecar.

```bash
docker exec <nazwa> ps aux --sort=-rss
```

Limit ustawiam pod zmierzone `anon`, z zapasem około 20–30% na stos, wątki i biblioteki natywne. Sterta języka musi być niższa niż limit kontenera, inaczej proces dostanie OOM, zanim zdąży zwolnić pamięć:

```bash
docker run -d --memory=512m --memory-swap=512m \
  -e NODE_OPTIONS=--max-old-space-size=384 \
  twoj-obraz
```

Dla Javy `-Xmx` też zostawiam poniżej `--memory`. Dla Node i Pythona najczęściej zawyża RAM liczba workerów: cztery procesy na kontenerze 512 MB zwykle się nie mieszczą, bo każdy ma własną stertę.

```yaml
services:
  app:
    mem_limit: 512m
    memswap_limit: 512m
```

`memswap_limit` równe `mem_limit` wyłącza swap. Swap ukrywa wyciek i tylko wydłuża czas odpowiedzi.

Jeśli `anon` rośnie przez cały ruch i nie wraca po jego końcu, limit niczego nie leczy. Zbieram heap dump przy szczycie i patrzę na pule połączeń, lokalny cache oraz bufory klienta kolejki. Osobno koryguję usługi, które wyglądają jak „ciężka aplikacja”, a są złą konfiguracją: Redis bez `maxmemory`, Postgres z domyślnym `shared_buffers`, Java bez `-Xmx` biorąca ułamek RAM widzianego przez kontener. Obraz Alpine albo `slim` nie obniża tego zużycia.

## Obserwacje

Oba prompty dostały tę samą receptę: zmierzyć zużycie, nałożyć limit kontenera, zejść ze stertą i liczbą procesów poniżej tego limitu, a rosnącą krzywą traktować jako wyciek. Rola nie podmieniła rozwiązania.

Zmieniła szczegółowość i charakter tekstu.

| | Zwykłe pytanie | Rola DevOps Engineera |
| --- | --- | --- |
| Wejście | Od razu `docker stats` i limit | Najpierw `OOMKilled`, potem rozdział cache (`file`) i pamięci procesów (`anon`) |
| Liczby | Node 256 MB i Java `-Xmx256m` przy limicie kontenera 512 MB | Limit liczony od `anon`, zapas 20–30%, Node 384 MB przy 512 MB |
| Specjalistyczne pojęcia | OOM, sterta, worker | cgroup, `memory.stat`, page cache, `memswap_limit`, pule połączeń |
| Forma | Instrukcja „zrób to” | Procedura w pierwszej osobie: co sprawdzam i kiedy limit nie wystarcza |

Zwykłe pytanie dało poprawną, krótszą listę kroków, z gotowymi wartościami sterty. Rola przesunęła odpowiedź w stronę diagnostyki z dyżuru: zanim padnie liczba megabajtów, widać, czy licznik w ogóle oznacza pamięć procesu. Staż „10 lat” sam nie dodaje nowych faktów. Widać to po różnych wartościach sterty Node (256 MB i 384 MB) przy tym samym limicie 512 MB. Rola zwiększa precyzję sprawdzeń i język operacyjny, a kierunek porady zostaje ten sam.
