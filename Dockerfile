FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir requests

COPY sender.py .

CMD ["python", "sender.py"]
