from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.strings.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
        print("---Server started---")

        await init_db()

        yield

        print("---Server closed---")


app = FastAPI(
    title="HNG stage 1",
    description="HNG stage 1 endpoints",
    lifespan=lifespan
)

app.include_router(router)