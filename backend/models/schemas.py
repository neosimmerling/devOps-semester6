from pydantic import BaseModel
from typing import Optional

class TagBase(BaseModel):
    name: str
    color: str = "#3b6b3a"

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int
    model_config = {"from_attributes": True}

class ItemBase(BaseModel):
    name: str
    quantity: int = 1
    unit: str = "Stück"
    is_checked: bool = False

class ItemCreate(ItemBase):
    list_id: int
    tag_ids: list[int] = []

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    is_checked: Optional[bool] = None
    tag_ids: Optional[list[int]] = None

class ItemResponse(ItemBase):
    id: int
    list_id: int
    tags: list[TagResponse] =[]
    model_config = {"from_attributes": True}

class ListBase(BaseModel):
    name: str

class ListCreate(ListBase):
    pass

class ListUpdate(BaseModel):
    name: Optional[str] = None

class ListResponse(ListBase):
    id: int
    items: list[ItemResponse] = []
    model_config = {"from_attributes": True}