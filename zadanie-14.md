# Zadanie 14: Wyjaśnienie fragmentu logów

## Pytanie

Co się dzieje w tych logach? Jakie problemy można zidentyfikować?

## Logi

```text
May 19 10:15:32 server dockerd[1234]: time="2025-05-19T10:15:32.123456789Z" level=info msg="Container 78a2b3c4 health status changed from starting to healthy"
May 19 10:16:45 server dockerd[1234]: time="2025-05-19T10:16:45.987654321Z" level=info msg="Container 78a2b3c4 failed to connect to 172.17.0.3:5432: connection refused"
May 19 10:16:47 server dockerd[1234]: time="2025-05-19T10:16:47.246813579Z" level=warning msg="Container 78a2b3c4 health status changed from healthy to unhealthy"
```

## Co oznaczają linie

Każda linia ma dwa czasy. `May 19 10:15:32` to czas z sysloga hosta o nazwie `server`. Reszta linii to komunikat procesu `dockerd` (PID 1234). Pole `time=` jest znacznikiem z samego Dockera, w UTC.

`78a2b3c4` to skrócony identyfikator jednego kontenera. `level=info` to zwykła informacja, `level=warning` to ostrzeżenie.

1. **10:15:32.** Kontener kończy stan `starting` i przechodzi w `healthy`. Test zdrowia (healthcheck) w tym momencie się udaje.
2. **10:16:45.** Ten sam kontener nie łączy się z adresem `172.17.0.3` na porcie `5432`. `connection refused` znaczy, że pakiet doszedł do hosta, ale nic nie przyjęło połączenia na tym porcie. Port 5432 jest domyślnym portem PostgreSQL. `172.17.0.3` to adres innego kontenera w domyślnej sieci Dockera (`docker0`), nie adres publicznej bazy.
3. **10:16:47.** Dwie sekundy później healthcheck tego kontenera pada: stan zmienia się z `healthy` na `unhealthy`.

## Problem

Kontener aplikacji przez około 73 sekundy był zdrowy, potem stracił bazę i od razu został oznaczony jako niezdrowy. Healthcheck najpewniej zależy od połączenia z Postgresem: gdy port 5432 odmawia połączenia, test zdrowia też się nie udaje.

`connection refused` na `172.17.0.3:5432` wskazuje, że kontener bazy nie nasłuchuje. Typowe przyczyny to zatrzymany albo zrestartowany kontener Postgresa, baza jeszcze niegotowa po restarcie albo aplikacja łączy się ze starym adresem IP kontenera, który już nie istnieje. To nie jest błąd „złe hasło”: przy złych danych logowania połączenie TCP się udaje, a odmawia sama baza.

Do sprawdzenia: czy kontener z Postgresem działa (`docker ps`), czy w jego logach widać restart około 10:16:45 i czy aplikacja łączy się po nazwie usługi z Compose, a nie po wpisanym na sztywno adresie `172.17.0.3`.
