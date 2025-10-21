from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    
    # Check if it's a missing field error
    for error in errors:
        if error["type"] == "missing":
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid request body or missing 'value' field"}
            )
    
    # For wrong type errors, keep 422
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": "Invalid data type for 'value' (must be string)"}
    )
app.include_router(router, prefix= "/strings",tags=["strings"])