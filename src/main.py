from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.middleware.errors import setup_exception_handlers
from src.routes.article import router as article_router
from src.routes.comment import router as comment_router
from src.routes.user import router as user_router

app = FastAPI(
    title="Blog Platform API",
    description="REST API for a blog platform with users, articles and comments",
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
app.include_router(article_router)
app.include_router(comment_router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
