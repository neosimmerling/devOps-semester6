from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    list_id: int

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True

class ListBase(BaseModel):
    name: str

class ListCreate(ListBase):
    pass

class ListResponse(ListBase):
    id: int

    class Config:
        from_attributes = True