FROM python:3.12-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

# RUN mkdir -p /src
# COPY src/ ./src
# COPY tests/ /tests/

COPY . /app/

ENV PYTHONPATH /

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]