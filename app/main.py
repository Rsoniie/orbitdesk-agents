import os

import uvicorn

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI


from app.config.neon_connect import check_database_connection
from app.routes.health_route import router as health_router
from app.routes.get_prd_route import router as get_prd_router


load_dotenv("app/.env")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_database_connection()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(health_router)
app.include_router(get_prd_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=int(os.getenv("APP_PORT", "8000")),
        reload=os.getenv("APP_RELOAD", "false").lower() == "true",
    )

