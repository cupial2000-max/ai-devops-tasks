# Simple Task API

REST API do zarządzania zadaniami. Aplikacja jest napisana w Node.js z Express i trzyma dane w MongoDB.

## Opis

API pozwala tworzyć, odczytywać, aktualizować i usuwać zadania. Listę można zawęzić do wybranego statusu i priorytetu. Dostęp do zadań wymaga prostego logowania: po podaniu danych użytkownika serwer zwraca token, który kolejne żądania wysyłają w nagłówku.

## Instalacja

Wymagane są Node.js oraz działająca instancja MongoDB.

```bash
npm install
cp .env.example .env
npm start
```

W pliku `.env` ustaw adres bazy i port:

```text
MONGODB_URI=mongodb://localhost:27017/simple-task-api
PORT=3000
```

Serwer nasłuchuje na `http://localhost:3000`.

## Użycie

Najpierw zaloguj użytkownika i zachowaj token:

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"jan@example.com\",\"password\":\"secret\"}"
```

Potem podawaj token przy żądaniach do zadań:

```bash
curl http://localhost:3000/api/tasks?status=open&priority=high \
  -H "Authorization: Bearer <token>"
```

Nowe zadanie:

```bash
curl -X POST http://localhost:3000/api/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Napisać testy\",\"status\":\"open\",\"priority\":\"high\"}"
```

## Endpointy API

| Metoda | Ścieżka | Opis |
| --- | --- | --- |
| `POST` | `/api/auth/register` | Zakłada konto użytkownika. |
| `POST` | `/api/auth/login` | Zwraca token do nagłówka `Authorization`. |
| `GET` | `/api/tasks` | Lista zadań. Parametry `status` i `priority` są opcjonalne. |
| `POST` | `/api/tasks` | Tworzy zadanie z polami `title`, `status` i `priority`. |
| `GET` | `/api/tasks/:id` | Zwraca jedno zadanie. |
| `PATCH` | `/api/tasks/:id` | Aktualizuje podane pola zadania. |
| `DELETE` | `/api/tasks/:id` | Usuwa zadanie. |
