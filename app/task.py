from celery import Celery
import mailtrap as mt
from app.config import REDIS_URL, MAILTRAP
import asyncio

celery_app = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)
client_mt = mt.MailtrapClient(token=MAILTRAP["token"])

@celery_app.task
def long_task(sleep_time: int = 10):
    import time
    time.sleep(sleep_time)  # Simulate a long-running task
    return "Processamento assíncrono concluído"


@celery_app.task
def process_data_and_send_email(data: str, to: str):
    import time
    time.sleep(15)  # Simulate data processing

    subject = "Processamento de Dados Concluído"
    body = f"O processamento dos seus dados foi concluído. Dados: {data}"
    asyncio.run(send_email(to, subject, body))
    return "Email enviado com sucesso"

async def send_email(to: str, subject: str, body: str):
    mail = mt.Mail(
        sender=mt.Address(email="mailtrap@demomailtrap.co", name="Mailtrap Testing"),
        to=[mt.Address(email=to, name=to)],
        subject=subject,
        text=body,
    )

    client_mt.send(mail)

@celery_app.task
def long_task_with_progress(self, total: int = 100):
    import time
    for i in range(total):
        time.sleep(0.1)  # Simulate work
        self.update_state(state='PROGRESS', meta={'current': i, 'total': total})
    return {"status": "Task completed!"}