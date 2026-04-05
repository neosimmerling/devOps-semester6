from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    quantity: int = 1
    unit: str = "Stück"
    is_checked: bool = False

class ItemCreate(ItemBase):
    list_id: int

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    is_checked: Optional[bool] = None

class ItemResponse(ItemBase):
    id: int

    model_config = {"from_attribute": True}

class ListBase(BaseModel):
    name: str

class ListCreate(ListBase):
    pass

class ListUpdate(BaseModel):
    name: Optional[str] = None

class ListResponse(ListBase):
    id: int
    items: list[ItemResponse] = []

    model_config = {"from_attribute": True}