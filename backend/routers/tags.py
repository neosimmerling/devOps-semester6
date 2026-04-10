from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.models import Tag
from backend.models.schemas import TagCreate, TagResponse

router = APIRouter(prefix="/tags", tags=["tags"])

### GET ###
@router.get("/", response_model=list[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    return db.query(Tag).order_by(Tag.name).all()

### CREATE ###
@router.post("/", response_model=TagResponse, status_code=201)
def create_tag(data: TagCreate, db: Session = Depends(get_db)):
    existing = db.query(Tag).filter(Tag.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag existiert bereits")
    tag = Tag(name=data.name, color=data.color)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

### UPDATE ###
@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: int, data: TagCreate, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag nicht gefunden")
    tag.name = data.name
    tag.color = data.color
    db.commit()
    db.refresh(tag)
    return tag

### DELETE ###
@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag nicht gefunden")
    db.delete(tag)
    db.commit()