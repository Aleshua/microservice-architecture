from fastapi import FastAPI

app = FastAPI(title="Blog Platform")

@app.get("/api/health")
async def health():
    return {"status": "ok"}
