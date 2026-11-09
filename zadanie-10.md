# Zadanie 10: Generowanie prostego pliku .gitignore

## Prompt 1

Stwórz plik .gitignore dla projektu Node.js, który używa Docker i przechowuje dane w lokalnej bazie MongoDB.

Wygenerowana zawartość jest w pliku `.gitignore`.

## Prompt 2

Dlaczego ważne jest ignorowanie tych plików?

## Wyjaśnienie

`.gitignore` mówi Gitowi, których plików nie dodawać do repozytorium. W tym projekcie pominięte są trzy grupy: zależności Node.js, sekrety oraz dane lokalne Dockera i MongoDB.

**`node_modules/`** to katalog z pakietami pobranymi przez npm. Jest duży, da się go odtworzyć poleceniem `npm install` z `package.json` i `package-lock.json`, a jego zawartość różni się między systemami. Wrzucenie go do Gita zaśmieca historię i spowalnia klonowanie.

**Logi i cache** (`.npm/`, pliki `npm-debug.log*`) powstają lokalnie przy instalacji i przy błędach. Nie są częścią aplikacji i na każdym komputerze wyglądają inaczej.

**`.env`** trzyma hasła, adres bazy i inne sekrety. Plik z hasłem do MongoDB w publicznym albo nawet prywatnym repozytorium zostaje w historii commitów. Do repozytorium może trafić najwyżej `.env.example` z samymi nazwami zmiennych, bez wartości. Wpis `!.env.example` jest wyjątkiem: Git ma ignorować `.env.*`, ale tego jednego pliku-wzorca nie.

**`dist/` i `build/`** to wynik kompilacji. Źródłem prawdy jest kod, a katalog z buildem powstaje ponownie przy `npm run build`.

**`data/`, `mongo-data/`, `mongodb-data/`** oraz pliki `*.wt` i `mongod.lock` to pliki samej bazy. MongoDB trzyma tam kolekcje, indeksy i dziennik. Są duże, binarne i zmieniają się przy każdym zapisie. W repozytorium zostałby zrzut czyjejś lokalnej bazy, często z danymi testowymi albo danymi osobowymi, a Git słabo trzyma takie pliki. Bazę odtwarza się migracją albo skryptem, nie kopią katalogu danych.

**`docker-data/` i `docker-compose.override.yml`** to lokalne wolumeny i lokalne nadpisanie Compose (inny port, inna ścieżka do danych). Mają zostać na jednym komputerze. Wspólna konfiguracja zostaje w `docker-compose.yml`, który nie jest ignorowany.
