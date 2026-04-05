from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    items = relationship("ShoppingItem", back_populates="list", cascade="all, delete")

class ShoppingItem(Base):
    __tablename__ = "shopping_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    unit = Column(String, default="Stück")
    is_checked = Column(Boolean, default=False)
    list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False)

    list = relationship("ShoppingList", back_populates="items")