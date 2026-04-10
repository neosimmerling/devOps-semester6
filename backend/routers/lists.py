from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.models import ShoppingList
from backend.models.schemas import ListCreate, ListUpdate, ListResponse

router = APIRouter(prefix="/lists", tags=["lists"])

def get_owner(request: Request) -> str:
    owner = request.headers.get("X-Owner-Id", "")
    if not owner:
        raise HTTPException(status_code=400, detail="X-Owner-Id Header fehlt")
    return owner

### Get all ###
@router.get("/", response_model=list[ListResponse])
def get_lists(db: Session = Depends(get_db), owner_id: str = Depends(get_owner)):
    return db.query(ShoppingList).filter(ShoppingList.owner_id == owner_id).all()

### Get one ###
@router.get("/{list_id}", response_model=ListResponse)
def get_list(list_id: int, db: Session = Depends(get_db), owner_id: str = Depends(get_owner)):
    lst = db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.owner_id == owner_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")
    return lst

### CREATE ###
@router.post("/", response_model=ListResponse, status_code=201)
def create_list(data: ListCreate, db: Session = Depends(get_db), owner_id: str = Depends(get_owner)):
    lst = ShoppingList(name=data.name, owner_id=owner_id)
    db.add(lst)
    db.commit()
    db.refresh(lst)
    return lst

### DELETE ###
@router.delete("/{list_id}", status_code=204)
def delete_list(list_id: int, db: Session = Depends(get_db), owner_id: str = Depends(get_owner)):
    lst = db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.owner_id == owner_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")
    db.delete(lst)
    db.commit()

### PUT ###
@router.put("/{list_id}", response_model=ListResponse)
def update_list(list_id: int, data: ListUpdate, db: Session = Depends(get_db)):
    lst = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")
    if data.name is not None:
        lst.name = data.name
    db.commit()
    db.refresh(lst)
    return lst