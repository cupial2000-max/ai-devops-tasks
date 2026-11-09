# Zadanie 24: Interpretacja danych wydajnościowych

## Pytanie

Zinterpretuj te dane. Czy widzisz jakieś potencjalne problemy? Co sugerujesz, aby poprawić wydajność?

## Dane

Metryki serwera API z ostatnich 24 godzin:

- średni czas odpowiedzi: 230 ms
- 95. percentyl czasu odpowiedzi: 450 ms
- 99. percentyl czasu odpowiedzi: 1200 ms
- liczba zapytań: 15 000
- liczba błędów 5xx: 120
- użycie CPU: średnio 45%, maksymalnie 80%
- użycie pamięci: średnio 2,1 GB, maksymalnie 3,5 GB z 4 GB dostępnych

## Interpretacja

Ruch jest niewielki. 15 000 żądań na dobę to około 625 na godzinę, czyli średnio jedno żądanie na kilka sekund. Przy takim obciążeniu sam wolumen nie tłumaczy ani 45% CPU, ani sekundowych odpowiedzi.

Średnia 230 ms wygląda umiarkowanie, ale ogon jest długi. 95. percentyl (450 ms) jest około dwa razy wyższy od średniej, a 99. percentyl (1200 ms) około pięć razy. Co setne żądanie czeka ponad sekundę. Średnia tego nie pokazuje, bo szybkie odpowiedzi ją ściągają w dół.

Błędów 5xx jest 120, czyli 0,8% żądań. To już zauważalna awaryjność: mniej więcej co 125. wywołanie kończy się błędem serwera, nie błędem klienta.

Pamięć w szczycie sięga 3,5 GB z 4 GB, czyli około 88% dostępnego RAM-u. Zostaje pół gigabajta zapasu. Średnie 2,1 GB jest spokojniejsze, więc albo zużycie faluje, albo rośnie i opada. CPU w szczycie ma 80%, więc bywa zajęte, ale nie stoi w 100%.

## Potencjalne problemy

Długi ogon przy małym ruchu zwykle oznacza pojedyncze wolne operacje, nie brak mocy całego serwera. Typowo jest to zapytanie do bazy bez indeksu, wolne wywołanie zewnętrznej usługi albo czekanie na blokadę. Te same żądania mogą kończyć się kodem 5xx, gdy timeout albo brak pamięci ubije obsługę.

Pamięć blisko 4 GB zostawia mało miejsca na skok. Przy dalszym wzroście proces może zwolnić przez odśmiecanie albo zostać zabity. Średnie CPU 45% przy jednym żądaniu na kilka sekund jest wysokie jak na samą obsługę API. Warto sprawdzić, czy czas procesora zjada aplikacja w tle, a nie same żądania.

## Co poprawić

Najpierw rozdzielić metryki, a nie dokładać CPU. 99. percentyl i błędy 5xx trzeba zobaczyć per endpoint i w czasie: czy 1200 ms i błędy wypadają w tych samych minutach co szczyt 3,5 GB.

Dla wolnego procenta żądań: ślad albo log z czasem bazy i czasem wywołań zewnętrznych. Jeśli wolna jest jedna kwerenda, indeks albo mniej danych w odpowiedzi skróci ogon skuteczniej niż mocniejsza maszyna.

Dla pamięci: wykres z całej doby. Jeśli szczyt wraca do 2 GB po ruchu, to zapas jest mały i wystarczy limit albo trochę więcej RAM-u. Jeśli krzywa tylko rośnie, to wyciek i większa maszyna go nie usuwa.

CPU profilować przy tych 45% średniej. Dopiero gdy widać, że procent schodzi na konkretną pętlę albo serializację, jest sens upraszczać kod. Dokładanie rdzeni przy 15 000 żądań na dobę nie skróci 99. percentyla, jeśli te żądania czekają na bazę.
