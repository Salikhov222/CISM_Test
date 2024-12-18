from fastapi import FastAPI

from tasks.handlers import router as task_router


app =  FastAPI(
    title="Task management service",
    summary="Simple task management service",
    version="1.0.0"
    )

app.include_router(task_router)

