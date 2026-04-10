from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.models import ShoppingItem, ShoppingList, Tag
from backend.models.schemas import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(prefix="/items", tags=["items"])

### GET ###
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
    item = ShoppingItem(
        name = data.name,
        quantity = data.quantity,
        unit = data.unit,
        is_checked = data.is_checked,
        list_id = data.list_id,
    )
    if data.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()
        item.tags = tags
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

### PUT ###
@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Artikel nicht gefunden")
    for field, value in data.model_dump(exclude_unset=True, exclude={"tag_ids"}).items():
        setattr(item, field, value)
    if data.tag_ids is not None:
        item.tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()
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