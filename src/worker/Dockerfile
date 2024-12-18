FROM python:3.12-slim

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

ENV PYTHONPATH /

CMD ["sh", "-c", "sleep 10 && python /src/worker/worker.py"]
