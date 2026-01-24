import os

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select

from eggs.db import get_db, init_db, ListModel

app = FastAPI()


@app.get("/api/v1/health")
def health():
    return "OK"


@app.get("/api/v1/lists/")
def read_lists(db=Depends(get_db)):
    statement = select(ListModel)
    lists = db.exec(statement).all()
    return [list_item.name for list_item in lists]


@app.post("/api/v1/lists/{name}")
def create_list(name: str, db=Depends(get_db)):
    from sqlmodel import select

    existing = db.exec(select(ListModel).where(ListModel.name == name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="List already exists")

    list_item = ListModel(name=name)
    db.add(list_item)
    db.commit()
    db.refresh(list_item)
    return {"message": f"List '{name}' created successfully"}


@app.delete("/api/v1/lists/{name}")
def delete_list(name: str, db=Depends(get_db)):
    from sqlmodel import select

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
