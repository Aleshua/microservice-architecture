from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.middleware.errors import setup_exception_handlers
from src.routes.user import router as user_router

app = FastAPI(
    title="Users Service API",
    description="Microservice for user management and authentication",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_exception_handlers(app)

app.include_router(user_router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
