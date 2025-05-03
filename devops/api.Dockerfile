FROM python:3.12-slim

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install numpy loguru s3fs

RUN pip install -r requirements.txt

COPY src /app/src
COPY config /app/config

ENV PYTHONPATH="/app:/app/src:$PYTHONPATH"

EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]