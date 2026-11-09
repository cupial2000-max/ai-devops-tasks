# Prosty skrypt do backupu bazy danych

$DB_NAME = "app_database"
$BACKUP_DIR = "C:\backups\db"
$DATE = Get-Date -Format "yyyyMMdd_HHmmss"
$FILENAME = Join-Path $BACKUP_DIR "${DB_NAME}_${DATE}.sql.gz"

if (-not (Test-Path -Path $BACKUP_DIR -PathType Container)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null
    Write-Output "Utworzono katalog $BACKUP_DIR"
}

Write-Output "Rozpoczynam backup bazy $DB_NAME..."

$tempSql = Join-Path $env:TEMP "${DB_NAME}_${DATE}.sql"
& mysqldump -u root -p $DB_NAME "--result-file=$tempSql"

if ($LASTEXITCODE -ne 0) {
    Write-Output "Błąd podczas wykonywania backupu!"
    exit 1
}

Add-Type -AssemblyName System.IO.Compression
$inputStream = [System.IO.File]::OpenRead($tempSql)
$outputStream = [System.IO.File]::Create($FILENAME)
$gzipStream = New-Object System.IO.Compression.GzipStream(
    $outputStream,
    [System.IO.Compression.CompressionMode]::Compress
)

try {
    $inputStream.CopyTo($gzipStream)
}
finally {
    $gzipStream.Dispose()
    $outputStream.Dispose()
    $inputStream.Dispose()
    Remove-Item $tempSql
}

Write-Output "Backup zakończony sukcesem: $FILENAME"
