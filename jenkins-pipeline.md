
# Pipeline CI/CD w Jenkins

```mermaid
flowchart TD
    A([Start pipeline]) --> B[Checkout - pobranie kodu]
    B --> C[Build - budowanie aplikacji]
    C --> D[Test - testy jednostkowe]
    D --> E[Static Code Analysis - analiza statyczna]
    E --> F[Security Scan - analiza bezpieczeństwa]
    F --> G[Build Docker Image - budowanie obrazu Docker]
    G --> H[Integration Tests - testy integracyjne]
    H --> I{Czy wszystkie testy zakończone sukcesem?}

    I -->|Nie| J[Przerwanie pipeline]
    J --> K([Koniec - niepowodzenie])

    I -->|Tak| L[Deploy to Staging - wdrożenie na staging]
    L --> M[Smoke Tests - testy środowiska staging]
    M --> N{Czy staging działa poprawnie?}

    N -->|Nie| J
    N -->|Tak| O{Zatwierdzenie wdrożenia?}

    O -->|Nie| P([Oczekiwanie na decyzję])
    O -->|Tak| Q[Deploy to Production - wdrożenie na produkcję]
    Q --> R[Weryfikacja wdrożenia]
    R --> S([Koniec - sukces])

    style J fill:#f8d7da,stroke:#dc3545,color:#721c24
    style K fill:#f8d7da,stroke:#dc3545,color:#721c24
    style S fill:#d4edda,stroke:#28a745,color:#155724
