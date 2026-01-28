from fastapi import FastAPI
from endpoints import router as entry_router

# FastAPI 실행 및 엔드포인트 정의
app = FastAPI(
    title = "Pill Identifier solution"
)

app.include_router(entry_router, tags = ["API"])