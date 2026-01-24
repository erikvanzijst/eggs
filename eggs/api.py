import os
import sqlite3

import uvicorn
from fastapi import FastAPI, HTTPException, Depends

from eggs.db import get_db, init_db

app = FastAPI()


@app.get("/api/v1/health")
def health():
    return "OK"


@app.get("/api/v1/lists/")
def read_lists(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute("SELECT name FROM lists")
    lists = [row[0] for row in cursor.fetchall()]
    return lists


@app.post("/api/v1/lists/{name}")
def create_list(name: str, db: sqlite3.Connection = Depends(get_db)):
    try:
        db.execute("INSERT INTO lists (name) VALUES (?)", (name,))
        return {"message": f"List '{name}' created successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="List already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("eggs.api:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
