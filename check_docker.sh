#!/usr/bin/env bash

if systemctl is-active --quiet docker; then
  echo "Usługa Docker działa."
else
  echo "Usługa Docker nie działa. Próba uruchomienia..."
  sudo systemctl start docker

  if systemctl is-active --quiet docker; then
    echo "Usługa Docker została uruchomiona."
  else
    echo "Nie udało się uruchomić usługi Docker."
    exit 1
  fi
fi
