import os

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from eggs.db import get_db, ListModel

app = FastAPI(
    title="Eggs API",
    description="A simple API for managing lists",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)


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


def main():
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("eggs.api:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
