# Zadanie 18: Analiza wymagań bezpieczeństwa

## Pytanie

Jakie są 5 kluczowych praktyk bezpieczeństwa dla aplikacji Dockerowych w środowisku produkcyjnym?

## Odpowiedź

1. **Nie uruchamiaj procesu jako root.** Domyślny użytkownik w kontenerze to root. Jeśli aplikacja zostanie przejęta, atakujący ma uprawnienia roota wewnątrz kontenera. Osobny użytkownik bez powłoki ogranicza to, co da się zrobić po włamaniu.

2. **Przypnij konkretną wersję obrazu bazowego.** Tag `latest` zmienia się bez Twojej zmiany w Dockerfile. W produkcji obraz powinien mieć wersję, na przykład `node:18.20.4-alpine`, żeby build dało się powtórzyć i świadomie podnosić.

3. **Nie zapisuj sekretów w obrazie ani w repozytorium.** Hasła, tokeny i klucze nie należą do `ENV` w Dockerfile ani do warstw obrazu. Zostają w zmiennych podawanych przy starcie albo w mechanizmie sekretów, poza Gitem.

4. **Odetnij zbędne uprawnienia kontenera.** Kontener produkcyjny nie potrzebuje `privileged: true`. Warto zabrać zbędne capabilities, wyłączyć zdobywanie nowych uprawnień i, tam gdzie aplikacja na to pozwala, zamontować system plików tylko do odczytu.

5. **Ogranicz zasoby i aktualizuj obraz.** Limit pamięci i CPU sprawia, że jeden kontener nie zajmie całego hosta. Regularna podmiana obrazu bazowego na wersję z poprawkami zamyka znane dziury w systemie i bibliotekach.

## Pytanie uzupełniające

Jak mogę zaimplementować pierwszą z tych praktyk w moim Dockerfile i docker-compose.yml?

## Implementacja: proces bez roota

W Dockerfile użytkownik powstaje przy budowaniu obrazu, a dyrektywa `USER` przełącza na niego wszystkie późniejsze polecenia, w tym `CMD`.

```dockerfile
FROM node:18.20.4-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY . .

RUN addgroup -S app && adduser -S app -G app \
  && chown -R app:app /app

USER app

EXPOSE 3000
CMD ["node", "server.js"]
```

`addgroup` i `adduser` z flagą `-S` tworzą grupę i użytkownika systemowego o nazwie `app`. `chown` oddaje katalog aplikacji temu użytkownikowi, więc proces może czytać własne pliki. `USER app` sprawia, że `node server.js` nie startuje jako root.

W Compose to samo da się wymusić przy uruchomieniu, niezależnie od tego, czy obraz już ma dyrektywę `USER`. Identyfikator `1000:1000` musi odpowiadać użytkownikowi z obrazu. Po `adduser -S` na Alpine numer bywa inny niż 1000, więc pewniejszy zapis to nazwa użytkownika albo ten sam numer, który powstał w obrazie.

```yaml
services:
  app:
    build: .
    user: "app"
    ports:
      - "3000:3000"
```

`user: "app"` w Compose wskazuje tego samego użytkownika, którego utworzył Dockerfile. Jeśli ktoś zbuduje obraz bez `USER`, Compose i tak nie wystartuje procesu jako root.
