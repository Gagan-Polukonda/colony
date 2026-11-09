from fastapi import APIRouter, Request, HTTPException, Depends

from auth import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])

@router.post("/jobs")
def submit_jobs(request: Request, job: dict, user: str = Depends(verify_api_key)):
    request.app.state.queue.enqueue(job)
    job["user"] = user
    request.app.state.owners.set(job["id"], user)
    return {"id": job["id"], "user": user}

@router.get("/jobs/{job_id}")
def get_job_status(request: Request, job_id: str, user: str = Depends(verify_api_key)):
    owner = request.app.state.owners.get(job_id)
    if owner != user:
        raise HTTPException(status_code=403, detail="Not your job")
    return {"id": job_id, "status": request.app.state.queue.status.get(job_id)}
