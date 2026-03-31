from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.models import ShoppingItem, ShoppingList
from backend.models.schemas import ItemCreate, ItemResponse

router = APIRouter(prefix="/items", tags=["items"])

### GET by list ###
@router.get("/by-list/{list_id}", response_model=list[ItemResponse])
def get_items_by_list(list_id: int, db: Session = Depends(get_db)):
    lst = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")
    return db.query(ShoppingItem).filter(ShoppingItem.list_id == list_id).all()

### CREATE ###
@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(data: ItemCreate, db: Session = Depends(get_db)):
    lst = db.query(ShoppingList).filter(ShoppingList.id == data.list_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Liste nicht gefunden")
    
    item = ShoppingItem(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

### DELETE ###
@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Artikel nicht gefunden")
    
    db.delete(item)
    db.commit()