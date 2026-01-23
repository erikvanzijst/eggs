import os

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/health")
async def health():
    return "OK"


@app.get("/api/v1/lists/")
async def read_lists():
    return []


def main():
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
