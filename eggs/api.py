from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/lists/")
async def read_lists():
    return []
