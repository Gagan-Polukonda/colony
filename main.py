from contextlib import asynccontextmanager
from pydantic_settings import BaseSettings

from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import PlainTextResponse

from reliable_redis.core.client import RedisClient
from reliable_redis.queue import JobQueue


class Settings(BaseSettings):
    api_key : str

    class Config:
        env_file = ".env"

settings = Settings()

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
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

@app.post("/jobs", dependencies=[Depends(verify_api_key)])
def submit_jobs(job: dict):
    app.state.queue.enqueue(job)
    return {"id": job["id"]}

@app.get("/jobs/{job_id}", dependencies=[Depends(verify_api_key)])
def get_job_status(job_id: str):
    return {"id": job_id, "status": app.state.queue.status.get(job_id)}
