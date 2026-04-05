# DevOps Semester 6 Projekt

## Projektbeschreibung
Dieses Projekt ist eine einfache Fullstack-Anwendung bestehend aus:
- **Backend:** Python (FastAPI)
- **Frontend:** HTML, CSS, JavaScript
- **Datenbank:** SQLite, konfiguriert in `database.py`
- **Container:** Docker & Docker Compose
- **CI/CD:** GitHub Actions
- **Versionierung:** Git

Die Anwendung stellt eine API zur Verwaltung von Listen und Items bereit und bietet ein einfaches Frontend zur Interaktion.

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
uvicorn backend.main:app --reload
http://localhost:8000
```

---

## b) Projekt mit Docker starten

### 1. Build + Start
```bash
docker-compose up --build
```

### 2. Zugriff
```bash
http://localhost:8000
```

### 3. Stoppen
```bash
docker-compose down
```

---

## c) Tests
```bash
pytest backend\tests
```

---

## d) CI/CD (GitHub Actions)
Die CI-Pipeline befindet sich in:
```bash
.github/workflows/ci.yml
```

---

## Autoren
- Franz Krätzer
- Neo Simmerling
- Luke Treder