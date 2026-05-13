from fastapi import FastAPI

app = FastAPI(
    title="CortexParse API",
    version="0.1.0"
)


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
