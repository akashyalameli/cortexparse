from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.api.app.routes.document import router as document_router
from shared.config.runtime_state import runtime_state


@asynccontextmanager
async def lifespan(app: FastAPI):

    runtime_state["model_ready"] = True
    runtime_state["templates_loaded"] = True
    runtime_state["few_shot_examples_loaded"] = True
    runtime_state["workflow_initialized"] = True

    yield


app = FastAPI(
    title="CortexParse API",
    version="0.1.0",
    lifespan=lifespan
)


app.include_router(document_router)


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@app.get("/model/status")
async def model_status():
    return runtime_state
