from fastapi import FastAPI
from app.task import celery_app, long_task, process_data_and_send_email, long_task_with_progress
from celery.result import AsyncResult

app = FastAPI()

@app.get("/sync-process")
def sync_process():
    import time
    time.sleep(10)  # Simulate a blocking operation
    return {"message": "Processamento síncrono concluído"}

@app.get("/async-process")
def async_process(time: int = 10):
    task= long_task.delay(time)
    return {
        'task_id': task.id, 
        'message': "Tarefa enviada para processamento assíncrono",
    }

@app.get("/process-and-email")
def process_and_email(data: str, email: str):
    task = process_data_and_send_email.delay(data, email)
    return {"message": "Processamento iniciado, você receberá um email quando concluído.", "task_id": task.id}

@app.get("/process-with-progress")
def progress_with_progress():
    task = long_task_with_progress.delay()
    return {"message": "Tarefa com progresso iniciada.", "task_id": task.id}

@app.get("/task-status/{task_id}")
def task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.state == 'PENDING':
        return {"state": result.state, "progress": 0}
    if result.state == 'PROGRESS':
        return {"state": result.state, "progress": result.info.get("percent", 0)}
    if result.state == 'SUCCESS':
        return {"state": result.state, "result": result.info}
    return {"state": result.state, "info": str(result.info)}
