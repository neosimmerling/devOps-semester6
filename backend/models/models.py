from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from backend.database import Base

item_tags = Table(
    "item_tags",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("shopping_items.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    color = Column(String, default="#3b6b3a")

    items = relationship("ShoppingItem", secondary=item_tags, back_populates="tags")

class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(String, nullable=False, index=True)

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
    tags = relationship("Tag", secondary=item_tags, back_populates="items")