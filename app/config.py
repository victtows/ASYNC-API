import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
MAILTRAP = {
    "token": os.getenv("MAILTRAP_TOKEN"),
    "from_email": os.getenv("MAIL_FROM"),
}