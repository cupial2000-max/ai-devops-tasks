# Zadanie 3: Podstawowe formatowanie promptu

## Prompt 1 (niestrukturyzowany)

```
dockerfile node
```

### Odpowiedź

Typowy, ogólny Dockerfile dla aplikacji Node.js. Model musi sam dopowiedzieć wersję Node, sposób instalacji i polecenie startu:

```dockerfile
FROM node:20

WORKDIR /app

COPY . .

RUN npm install

EXPOSE 3000

CMD ["node", "index.js"]
```

Założenia, których prompt nie podał: obraz `node:20`, katalog `/app`, instalacja po skopiowaniu całego kodu, start przez `node index.js`, port 3000 „bo tak zwykle bywa”.

## Prompt 2 (strukturyzowany)

```
Napisz prosty Dockerfile dla aplikacji Node.js, który:
- używa Node 18 jako obrazu bazowego
- kopiuje pliki package.json i package-lock.json
- instaluje zależności
- kopiuje resztę plików aplikacji
- wystawia port 3000
- uruchamia aplikację poleceniem "npm start"
```

### Odpowiedź

```dockerfile
FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

`npm ci` instaluje dokładnie wersje z `package-lock.json`. Osobne kopiowanie plików zależności sprawia, że przy zmianie samego kodu aplikacji Docker nie powtarza instalacji pakietów.

## Wnioski

Ten sam temat, dwa różne wyniki.

Prompt `dockerfile node` dał działający szkielet, ale model zgadywał: Node 20 zamiast 18, `COPY . .` przed instalacją, start przez `node index.js` zamiast `npm start`. Taki plik może nie pasować do projektu, który nie ma `index.js` albo wymaga innej wersji Node.

Prompt z listą wymagań dał Dockerfile zgodny z poleceniem: `node:18`, najpierw `package.json` i lockfile, potem instalacja, potem reszta plików, port 3000 i `npm start`. Im więcej decyzji jest w promptcie (wersja, kolejność kroków, komenda startu), tym mniej model dopowiada po swojemu.
