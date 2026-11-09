from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

import jobs

from reliable_redis.core.client import KVStore, RedisClient
from reliable_redis.queue import JobQueue


@asynccontextmanager
async def lifespan(app: FastAPI):
    with RedisClient() as r:
        app.state.queue = JobQueue(r, name="jobs")
        app.state.owners = KVStore(r, prefix="job_owner")
        yield

app = FastAPI(
    title="colony",
    description="The application layer of a distributed system, organized like an ant colony",
    lifespan=lifespan,
)

app.include_router(jobs.router)


@app.get("/", response_class=PlainTextResponse)
def root():
    return f"{app.title}\n\n{app.description}"

@app.get("/health")
def health():
    return {"status": "ok"}
