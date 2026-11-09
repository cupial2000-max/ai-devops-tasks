# GET /api/users

Zwraca listę użytkowników. Wynik jest podzielony na strony. Opcjonalny parametr `role` zawęża listę do jednej roli.

## Parametry zapytania

| Parametr | Wymagany | Domyślnie | Opis |
| --- | --- | --- | --- |
| `page` | nie | `1` | Numer strony. Numeracja zaczyna się od 1. |
| `limit` | nie | `10` | Liczba użytkowników na stronie. Wartość maksymalna to 100. |
| `role` | nie | brak | Filtr roli, na przykład `admin` albo `user`. Bez tego parametru zwracane są wszystkie role. |

## Przykładowe żądanie

```http
GET /api/users?page=1&limit=2&role=admin HTTP/1.1
Host: api.example.com
```

## Przykładowa odpowiedź

`200 OK`

```json
{
  "page": 1,
  "limit": 2,
  "role": "admin",
  "users": [
    {
      "id": 14,
      "name": "Anna Kowalska",
      "email": "anna@example.com",
      "role": "admin"
    },
    {
      "id": 27,
      "name": "Jan Nowak",
      "email": "jan@example.com",
      "role": "admin"
    }
  ]
}
```

Gdy `page` albo `limit` jest poza zakresem, serwer zwraca `400 Bad Request` z krótkim opisem błędu:

```json
{
  "error": "Parametr limit nie może być większy niż 100."
}
```
