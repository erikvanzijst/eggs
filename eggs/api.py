# Standard library imports
import os
import logging
import re

# Third-party imports
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select, Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field
from typing import Annotated

# Local imports
from eggs.db import get_db, ListModel, ItemModel

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Eggs API",
    description="A simple API for managing lists",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)


# Reusable validated name field using Pydantic's Field constraints
ValidatedName = Annotated[
    str, Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9 _-]+$")
]


class ItemCreate(BaseModel):
    """Model for creating a new item."""

    name: ValidatedName


class ListResponse(BaseModel):
    """Response model for List objects."""

    model_config = {"from_attributes": True}

    id: int
    name: ValidatedName


class ItemResponse(BaseModel):
    """Response model for Item objects."""

    model_config = {"from_attributes": True}

    id: int
    list_id: int
    name: ValidatedName


async def get_list_by_name(list_name: str, db: Session) -> ListModel:
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
async def health():
    """
    Check the health of the API.

    Returns:
        str: "OK" if the API is healthy
    """
    logger.info("Health check requested")
    return "OK"


@app.get("/api/v1/lists/")
async def read_lists(db: Session = Depends(get_db)) -> list[str]:
    """
    Get all lists.

    Returns:
        List[str]: A list of list names
    """
    logger.info("Reading all lists")
    statement = select(ListModel)
    lists = db.exec(statement).all()
    logger.debug(f"Found {len(lists)} lists")
    return [list_item.name for list_item in lists]


@app.post("/api/v1/lists/{name}")
async def create_list(
    name: ValidatedName, db: Session = Depends(get_db)
) -> ListResponse:
    """
    Create a new list.

    Args:
        name (str): The name of the list to create

    Returns:
        ListResponse: The created list object

    Raises:
        HTTPException: If the list already exists
    """

    logger.info(f"Creating list: {name}")
    try:
        list_item = ListModel(name=name)
        db.add(list_item)
        db.commit()
        db.refresh(list_item)
        logger.info(f"Successfully created list: {name} with id: {list_item.id}")
        return ListResponse.model_validate(list_item)
    except IntegrityError:
        db.rollback()
        logger.warning(f"Failed to create list {name}: already exists")
        raise HTTPException(status_code=400, detail="List already exists")


@app.delete("/api/v1/lists/{name}")
async def delete_list(name: str, db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Delete a list.

    Args:
        name (str): The name of the list to delete

    Returns:
        dict: A success message

    Raises:
        HTTPException: If the list is not found
    """
    logger.info(f"Deleting list: {name}")
    statement = select(ListModel).where(ListModel.name == name)
    list_item = db.exec(statement).first()

    if not list_item:
        logger.warning(f"Attempted to delete non-existent list: {name}")
        raise HTTPException(status_code=404, detail="List not found")

    db.delete(list_item)
    db.commit()
    logger.info(f"Successfully deleted list: {name}")
    return {"message": f"List '{name}' deleted successfully"}


@app.post("/api/v1/lists/{list_name}/items/")
async def create_item(
    list_name: ValidatedName, item: ItemCreate, db: Session = Depends(get_db)
) -> ItemResponse:
    """
    Create a new item in a list.

    Args:
        list_name (str): The name of the list
        item (ItemCreate): The item to create

    Returns:
        ItemResponse: The created item object

    Raises:
        HTTPException: If the list is not found or item already exists
    """

    logger.info(f"Creating item '{item.name}' in list: {list_name}")
    list_obj = await get_list_by_name(list_name, db)

    try:
        new_item = ItemModel(name=item.name, list_id=list_obj.id)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        logger.info(
            f"Successfully created item '{item.name}' in list '{list_name}' with id: {new_item.id}"
        )
        return ItemResponse.model_validate(new_item)
    except IntegrityError:
        db.rollback()
        logger.warning(
            f"Failed to create item '{item.name}' in list '{list_name}': already exists"
        )
        raise HTTPException(status_code=400, detail="Item already exists in this list")


@app.get("/api/v1/lists/{list_name}/items/")
async def get_items(list_name: str, db: Session = Depends(get_db)) -> list[str]:
    """
    Get all items from a list.

    Args:
        list_name (str): The name of the list

    Returns:
        List[str]: A list of item names

    Raises:
        HTTPException: If the list is not found
    """
    logger.info(f"Reading items from list: {list_name}")
    list_obj = await get_list_by_name(list_name, db)

    statement = select(ItemModel).where(ItemModel.list_id == list_obj.id)
    items = db.exec(statement).all()
    logger.debug(f"Found {len(items)} items in list '{list_name}'")
    return [item.name for item in items]


@app.delete("/api/v1/lists/{list_name}/items/{item_name}")
async def delete_item(
    list_name: str, item_name: str, db: Session = Depends(get_db)
) -> dict[str, str]:
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
    logger.info(f"Deleting item '{item_name}' from list: {list_name}")
    list_obj = await get_list_by_name(list_name, db)

    statement = select(ItemModel).where(
        ItemModel.list_id == list_obj.id, ItemModel.name == item_name
    )
    item = db.exec(statement).first()

    if not item:
        logger.warning(
            f"Attempted to delete non-existent item '{item_name}' from list '{list_name}'"
        )
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    logger.info(f"Successfully deleted item '{item_name}' from list '{list_name}'")
    return {
        "message": f"Item '{item_name}' deleted successfully from list '{list_name}'"
    }


async def main() -> None:
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("eggs.api:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
