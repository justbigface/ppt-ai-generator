FROM python:3.12-slim
WORKDIR /app
COPY export_service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY export_service /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7100"]
