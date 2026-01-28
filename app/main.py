from fastapi import FastAPI
from app.api.endpoints import router as entry_router
from fastapi.staticfiles import StaticFiles

# FastAPI 실행 및 엔드포인트 정의
app = FastAPI(
    title = "Pill Identifier solution"
)

app.mount("/data", StaticFiles(directory="data"), name="data")
app.include_router(entry_router, tags = ["API"])