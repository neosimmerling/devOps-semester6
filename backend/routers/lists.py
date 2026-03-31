from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.models import ShoppingList
from backend.models.schemas import ListCreate, ListResponse

router = APIRouter(prefix="/lists", tags=["lists"])

### Get all ###
@router.get("/", response_model=list[ListResponse])
def get_lists(db: Session = Depends(get_db)):
    return db.query(ShoppingList).all()

### Get one ###
@router.get("/{list_id}", response_model=ListResponse)
def get_list(list_id: int, db: Session = Depends(get_db)):
    lst = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")
    return lst

### CREATE ###
@router.post("/", response_model=ListResponse, status_code=201)
def create_list(data: ListCreate, db: Session = Depends(get_db)):
    lst = ShoppingList(name=data.name)
    db.add(lst)
    db.commit()
    db.refresh(lst)
    return lst

### DELETE ###
@router.delete("/{list_id}", status_code=204)
def delete_list(list_id: int, db: Session = Depends(get_db)):
    lst = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")
    db.delete(lst)
    db.commit()