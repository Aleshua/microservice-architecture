from fastapi import FastAPI

from src.routes.article import router as article_router
from src.routes.user import router as user_router

app = FastAPI(title="Blog Platform")

app.include_router(user_router)
app.include_router(article_router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
