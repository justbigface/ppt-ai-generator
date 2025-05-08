FROM python:3.12-slim
WORKDIR /code
COPY worker/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY worker /code/worker
CMD ["celery", "-A", "worker.celery_app", "worker", "--loglevel=info"]
