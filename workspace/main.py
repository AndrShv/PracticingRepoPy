from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


fast_api_app = FastAPI(
    title="Repo For Practicing Skills",
    version="1.0.0",
    lifespan=lifespan,
)

if __name__ == "__main__":
    uvicorn.run(fast_api_app, host="0.0.0.0", port=8000)
