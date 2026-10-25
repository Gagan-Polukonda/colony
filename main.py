import secrets
from contextlib import asynccontextmanager
from pydantic_settings import BaseSettings

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from fastapi.responses import PlainTextResponse

from reliable_redis.core.client import RedisClient
from reliable_redis.queue import JobQueue


class Settings(BaseSettings):
    api_keys: dict[str, str]

    class Config:
        env_file = ".env"

settings = Settings()

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(x_api_key: str = Depends(api_key_header)) -> str:
    for key, user in settings.api_keys.items():
        if secrets.compare_digest(x_api_key, key):
            return user
    raise HTTPException(status_code=401, detail="Invalid API key")


@asynccontextmanager
async def lifespan(app: FastAPI):
    with RedisClient() as r:
        app.state.queue = JobQueue(r, name="jobs")
        yield

app = FastAPI(
    title="colony",
    description="The application layer of a distributed system, organized like an ant colony",
    lifespan=lifespan,
)


@app.get("/", response_class=PlainTextResponse)
def root():
    return f"{app.title}\n\n{app.description}"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/jobs")
def submit_jobs(job: dict, user: str = Depends(verify_api_key)):
    app.state.queue.enqueue(job)
    job["user"] = user
    return {"id": job["id"], "user":job["user"]}

@app.get("/jobs/{job_id}", dependencies=[Depends(verify_api_key)])
def get_job_status(job_id: str):
    return {"id": job_id, "status": app.state.queue.status.get(job_id)}
