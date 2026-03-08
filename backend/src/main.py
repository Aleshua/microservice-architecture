from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.middleware.errors import setup_exception_handlers
from src.routes.article import router as article_router
from src.routes.comment import router as comment_router

app = FastAPI(
    title="Backend API",
    description="Microservice for articles and comments",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_exception_handlers(app)

app.include_router(article_router)
app.include_router(comment_router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
