import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

# --- Listen Tests ---

def test_create_list():
    res = client.post("/api/lists/", json={"name": "Wocheneinkauf"})
    assert res.status_code == 201
    assert res.json()["name"] == "Wocheneinkauf"

def test_get_all_lists():
    client.post("/api/lists/", json={"name": "Liste A"})
    client.post("/api/lists/", json={"name": "Liste B"})
    res = client.get("/api/lists/")
    assert res.status_code == 200
    assert len(res.json()) == 2

def test_get_single_list():
    created = client.post("/api/lists/", json={"name": "Meine Liste"}).json()
    res = client.get(f"/api/lists/{created['id']}")
    assert res.status_code == 200

def test_get_list_not_found():
    res = client.get("/api/lists/999")
    assert res.status_code == 404

def test_update_list():
    created = client.post("/api/lists/", json={"name": "Alt"}).json()
    res = client.put(f"/api/lists/{created['id']}", json={"name": "Neu"})
    assert res.status_code == 200
    assert res.json()["name"] == "Neu"

def test_delete_list():
    created = client.post("/api/lists/", json={"name": "Loeschen"}).json()
    res = client.delete(f"/api/lists/{created['id']}")
    assert res.status_code == 204

# --- Artikel Tests ---

def test_create_item():
    lst = client.post("/api/lists/", json={"name": "Markt"}).json()
    res = client.post("/api/items/", json={"list_id": lst["id"], "name": "Milch", "quantity": 2, "unit": "Liter"})
    assert res.status_code == 201
    assert res.json()["name"] == "Milch"

def test_get_items_by_list():
    lst = client.post("/api/lists/", json={"name": "Markt"}).json()
    client.post("/api/items/", json={"list_id": lst["id"], "name": "Brot"})
    client.post("/api/items/", json={"list_id": lst["id"], "name": "Butter"})
    res = client.get(f"/api/items/by-list/{lst['id']}")
    assert res.status_code == 200
    assert len(res.json()) == 2

def test_update_item_checked():
    lst = client.post("/api/lists/", json={"name": "Test"}).json()
    item = client.post("/api/items/", json={"list_id": lst["id"], "name": "Eier"}).json()
    res = client.put(f"/api/items/{item['id']}", json={"is_checked": True})
    assert res.status_code == 200
    assert res.json()["is_checked"] is True

def test_update_item_name():
    lst = client.post("/api/lists/", json={"name": "Test"}).json()
    item = client.post("/api/items/", json={"list_id": lst["id"], "name": "Kaese"}).json()
    res = client.put(f"/api/items/{item['id']}", json={"name": "Gouda", "quantity": 3})
    assert res.status_code == 200
    assert res.json()["name"] == "Gouda"
    assert res.json()["quantity"] == 3

def test_delete_item():
    lst = client.post("/api/lists/", json={"name": "Test"}).json()
    item = client.post("/api/items/", json={"list_id": lst["id"], "name": "Kaese"}).json()
    res = client.delete(f"/api/items/{item['id']}")
    assert res.status_code == 204

def test_item_invalid_list():
    res = client.post("/api/items/", json={"list_id": 999, "name": "Joghurt"})
    assert res.status_code == 404

def test_delete_list_cascades_items():
    lst = client.post("/api/lists/", json={"name": "Cascade"}).json()
    client.post("/api/items/", json={"list_id": lst["id"], "name": "Item A"})
    client.delete(f"/api/lists/{lst['id']}")
    res = client.get(f"/api/items/by-list/{lst['id']}")
    assert res.status_code == 404