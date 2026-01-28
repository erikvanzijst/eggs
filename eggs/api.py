import os

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select, Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from eggs.db import get_db, ListModel, ItemModel

app = FastAPI(
    title="Eggs API",
    description="A simple API for managing lists",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)


class ItemCreate(BaseModel):
    """Model for creating a new item."""
    name: str


def get_list_by_name(list_name: str, db: Session) -> ListModel:
    """
    Get a list by name.

    Args:
        list_name: The name of the list to retrieve
        db: Database session

    Returns:
        ListModel: The list object

    Raises:
        HTTPException: If the list is not found
    """
    statement = select(ListModel).where(ListModel.name == list_name)
    list_item = db.exec(statement).first()

    if not list_item:
        raise HTTPException(status_code=404, detail="List not found")

    return list_item


@app.get("/api/v1/health")
def health():
    """
    Check the health of the API.

    Returns:
        str: "OK" if the API is healthy
    """
    return "OK"


@app.get("/api/v1/lists/")
def read_lists(db=Depends(get_db)):
    """
    Get all lists.

    Returns:
        List[str]: A list of list names
    """
    statement = select(ListModel)
    lists = db.exec(statement).all()
    return [list_item.name for list_item in lists]


@app.post("/api/v1/lists/{name}")
def create_list(name: str, db=Depends(get_db)):
    """
    Create a new list.

    Args:
        name (str): The name of the list to create

    Returns:
        dict: A success message

    Raises:
        HTTPException: If the list already exists
    """
    try:
        list_item = ListModel(name=name)
        db.add(list_item)
        db.commit()
        db.refresh(list_item)
        return {"message": f"List '{name}' created successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="List already exists")


@app.delete("/api/v1/lists/{name}")
def delete_list(name: str, db=Depends(get_db)):
    """
    Delete a list.

    Args:
        name (str): The name of the list to delete

    Returns:
        dict: A success message

    Raises:
        HTTPException: If the list is not found
    """
    statement = select(ListModel).where(ListModel.name == name)
    list_item = db.exec(statement).first()

    if not list_item:
        raise HTTPException(status_code=404, detail="List not found")

    db.delete(list_item)
    db.commit()
    return {"message": f"List '{name}' deleted successfully"}


@app.post("/api/v1/lists/{list_name}/items/")
def create_item(list_name: str, item: ItemCreate, db=Depends(get_db)):
    """
    Create a new item in a list.

    Args:
        list_name (str): The name of the list
        item (ItemCreate): The item to create

    Returns:
        dict: A success message

    Raises:
        HTTPException: If the list is not found or item already exists
    """
    list_obj = get_list_by_name(list_name, db)

    try:
        new_item = ItemModel(name=item.name, list_id=list_obj.id)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return {"message": f"Item '{item.name}' created successfully in list '{list_name}'"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Item already exists in this list")


@app.get("/api/v1/lists/{list_name}/items/")
def get_items(list_name: str, db=Depends(get_db)):
    """
    Get all items from a list.

    Args:
        list_name (str): The name of the list

    Returns:
        List[str]: A list of item names

    Raises:
        HTTPException: If the list is not found
    """
    list_obj = get_list_by_name(list_name, db)

    statement = select(ItemModel).where(ItemModel.list_id == list_obj.id)
    items = db.exec(statement).all()
    return [item.name for item in items]


@app.delete("/api/v1/lists/{list_name}/items/{item_name}")
def delete_item(list_name: str, item_name: str, db=Depends(get_db)):
    """
    Delete an item from a list.

    Args:
        list_name (str): The name of the list
        item_name (str): The name of the item to delete

    Returns:
        dict: A success message

    Raises:
        HTTPException: If the list or item is not found
    """
    list_obj = get_list_by_name(list_name, db)

    statement = select(ItemModel).where(
        ItemModel.list_id == list_obj.id,
        ItemModel.name == item_name
    )
    item = db.exec(statement).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"message": f"Item '{item_name}' deleted successfully from list '{list_name}'"}


def main():
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("eggs.api:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
