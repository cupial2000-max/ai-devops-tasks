# Zadanie 16: Konwersja Bash do PowerShell

## Prompt

Przekonwertuj ten skrypt bash na równoważny skrypt PowerShell dla Windows.

Oryginał jest w `backup-db.sh`. Wersja dla Windows jest w `backup-db.ps1`. Oba robią to samo: tworzą katalog backupu, zrzucają bazę MySQL i pakują zrzut do `.sql.gz`.

## Różnice w tym przykładzie

**Uruchomienie.** Bash zaczyna się od `#!/bin/bash`. PowerShell nie używa shebanga. Plik `.ps1` uruchamia się przez `powershell -File .\backup-db.ps1`. Windows może zablokować skrypt zasadą wykonywania (`ExecutionPolicy`).

**Zmienne.** W bashu przypisanie to `DB_NAME="app_database"`, a odczyt `$DB_NAME`. W PowerShellu nazwa od razu ma znak dolara: `$DB_NAME = "app_database"`.

**Data.** Bash woła zewnętrzne `date +%Y%m%d_%H%M%S`. PowerShell używa `Get-Date -Format "yyyyMMdd_HHmmss"`. Format daje ten sam układ `YYYYMMDD_HHMMSS`, ale polecenie jest wbudowane.

**Ścieżki.** Bash składa ścieżkę ukośnikami: `"${BACKUP_DIR}/${DB_NAME}_${DATE}.sql.gz"`. Na Windowsie katalog to `C:\backups\db` zamiast `/var/backups/db`, a ścieżkę składa `Join-Path`, żeby nie pomylić separatorów.

**Katalog.** Bash sprawdza `[ ! -d "$BACKUP_DIR" ]` i tworzy go przez `mkdir -p`. PowerShell sprawdza `-not (Test-Path ... -PathType Container)` i tworzy katalog przez `New-Item -ItemType Directory`.

**Komunikaty.** `echo` w bashu odpowiada `Write-Output` w PowerShellu.

**Zrzut i kompresja.** Bash puszcza `mysqldump ... | gzip > plik`. Taki potok w PowerShellu przechodzi przez tekst i psuje binarny plik gzip. Dlatego `.ps1` zapisuje SQL przez `mysqldump --result-file`, a potem pakuje go strumieniem `System.IO.Compression.GzipStream`. Plik tymczasowy ląduje w `$env:TEMP` i jest usuwany po spakowaniu.

**Kod wyjścia.** Bash po potoku czyta `$?`. Bez `set -o pipefail` jest to kod ostatniego polecenia, czyli `gzip`, a nie `mysqldump`. PowerShell po programie zewnętrznym czyta `$LASTEXITCODE`. W tej wersji błąd `mysqldump` przerywa skrypt, zanim powstanie archiwum. `$?` w PowerShellu też istnieje, ale oznacza sukces ostatniego polecenia PowerShell, nie kod programu `mysqldump`.
