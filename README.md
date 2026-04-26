# DevOps Semester 6 Projekt

## Live-Demo
Die App ist live erreichbar unter: **https://einkaufsliste-t8qg.onrender.com/**

> **Hinweis:** Die App läuft auf einer kostenlosen Render-Instanz und fährt nach längerer Inaktivität herunter. Der erste Aufruf kann daher **30-60 Sekunden** dauern, bis die App wieder hochgefahren ist. Danach läuft sie normal.

> Bei jedem neuen Deployment **UND** nach jedem "Aufwecken" aus der Inaktivität wird die Datenbank zurückgesetzt. Lokal (Docker oder Python) bleiben die Daten persistent.

---

## Projektbeschreibung
Dieses Projekt ist eine einfache Fullstack-Anwendung zur Verwaltung von Einkaufslisten, entwickelt im Rahmen des Moduls **DevOps** im Studiengang Praktische Informatik an der DHGE.

| Komponente | Technologie |
|------------|-------------|
| Backend | Python 3.11, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Datenbank | SQLite (via SQLAlchemy) |
| Container | Docker & Docker Compose |
| CI/CD | GitHub Actions |
| Code-Qualität | SonarCloud |
| Versionierung | Git / GitHub |

---

## Features
- Einkaufslisten erstellen, umbenennen, löschen
- Artikel hinzufügen, bearbeiten, löschen
- Mengenangabe mit Einheit (Stück, kg, ml, ...)
- Artikel abhaken
- erledigte Artikel auf einmal löschen
- Tags erstellen und Artikeln zuweisen
- Sortierung nach Name, Menge, Einheit oder Status
- CSV-Export der Einkaufsliste
- Dark-Mode mit Persistenz im Browser
- Konfetti-Animation, wenn alle Artikel abgehakt sind
- Nutzer-Isolation per Browser-ID (jeder sieht nur seine eigenen Listen)
- responsives Design für Mobile und Desktop

---

## Technische Voraussetzungen
- Python 3.10+
- Docker & Docker Compose
- Git

---

## a) Projekt lokal starten

### 1. Repository klonen
```bash
git clone https://github.com/neosimmerling/devOps-semester6
cd devOps-semester6
```

### 2. Virtuelle Umgebung erstellen
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux / Mac
```

### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 4. Backend starten
```bash
python -m uvicorn backend.main:app --reload
```
Die App ist erreichbar unter: http://127.0.0.1:8000

---

## b) Projekt mit Docker starten

### 1. Build + Start
```bash
docker compose up --build
```

### 2. Zugriff
Die App ist erreichbar unter: http://127.0.0.1:8000

### 3. Stoppen
```bash
docker compose down
```

---

## c) Tests

Die Tests befinden sich in `backend/tests/` und werden mit **pytest** ausgeführt.
```bash
python -m pytest backend\tests -v
```

Mit Coverage-report:
```bash
python -m pytest backend/tests -v --cov=backend --cov-report=term-missing
```

Die Tests decken folgende Bereiche ab:
- Erstellen, Lesen, Aktualisieren und Löschen von Einkaufslisten
- Erstellen, Lesen, Aktualisieren und Löschen von Artikeln
- Validierung ungültiger Eingaben (z.B. nicht existierende Listen-ID)
- Cascade-Löschen von Artikeln beim Löschen einer Liste

---

## d) CI/CD (GitHub Actions)
Die CI-Pipeline befindet sich in `.github/workflows/ci.yml` und wird bei jedem Push und Pull automatisch ausgeführt.

### Pipeline-Übersicht

```
Push / Pull Request
        │
        ├── Test & Coverage        Tests ausführen + Coverage-Report erstellen
        ├── Dependency Scan        Pakete auf Sicherheitslücken prüfen (pip-audit)
        │
        ├── SonarCloud Analyse     Code-Qualität, Bugs und Security analysieren
        ├── API Health Check       App starten und Erreichbarkeit prüfen
        │
        └── Docker Build & Push   Image bauen und auf Docker Hub pushen (nur main)
```

### Jobs im Detail

**Test & Coverage** - führt alle pytest-Tests aus und erstellt einen XML-Coverage-Report, der an SonarCloud weitergegeben wird.

**Dependency Scan** - nutzt `pip-audit`, um bekannte CVEs (Sicherheitslücken) in den verwendeten Python-Paketen zu erkennen.

**SonarCloud Analyse** - statische Code-Analyse auf Bugs, Code-Smells und Security-Issues.

**API Health Check** - startet die App in der CI-Umgebung und prüft per `curl`, ob die API unter `http://127.0.0.1:8000` antwortet.

**Docker Build & Push** - baut das Docker-Image und pusht es auf Docker Hub. Dies läuft nur bei Pushes auf den `main`-Branch.

### Benötigte GitHub Secrets

| Secret | Beschreibung |
|--------|-------------|
| `SONAR_TOKEN` | API-Token von sonarcloud.io |
| `DOCKERHUB_USERNAME` | Docker Hub Benutzername |
| `DOCKERHUB_TOKEN` | Docker Hub Access Token |

---

## e) API-Dokumentation
FastAPI generiert automatisch eine interaktive API-Dokumentation:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Endpunkte
| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| GET | `/api/lists/` | Alle Listen abrufen |
| POST | `/api/lists/` | Neue Liste erstellen |
| PUT | `/api/lists/{id}` | Liste umbenennen |
| DELETE | `/api/lists/{id}` | Liste löschen |
| GET | `/api/items/by-list/{id}` | Artikel einer Liste abrufen |
| POST | `/api/items/` | Neuen Artikel erstellen |
| PUT | `/api/items/{id}` | Artikel bearbeiten |
| DELETE | `/api/items/{id}` | Artikel löschen |
| GET | `/api/tags/` | Alle Tags abrufen |
| POST | `/api/tags/` | Neuen Tag erstellen |
| DELETE | `/api/tags/{id}` | Tag löschen |

---

## f) Projektstruktur

```
devOps-semester6/
├── backend/
│   ├── models/
│   │   ├── models.py        # SQLAlchemy Datenbankmodelle
│   │   └── schemas.py       # Pydantic Schemas (Request/Response)
│   ├── routers/
│   │   ├── lists.py         # CRUD-Endpunkte für Listen
│   │   ├── items.py         # CRUD-Endpunkte für Artikel
│   │   └── tags.py          # CRUD-Endpunkte für Tags
│   ├── tests/
│   │   └── test_api.py      # Pytest-Tests
│   ├── database.py          # Datenbankverbindung (SQLite)
│   └── main.py              # FastAPI App & Routing
├── frontend/
│   ├── static/
│   │   ├── app.js           # Frontend-Logik
│   │   ├── styles.css       # Styling & Dark Mode
│   │   └── DHGE.png         # Logo
│   └── index.html           # Single-Page-App
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD Pipeline
├── sonar-project.properties # SonarCloud Konfiguration
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Autoren
- Franz Krätzer
- Neo Simmerling
- Luke Treder