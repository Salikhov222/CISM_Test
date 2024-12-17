FROM python:3.12-slim

WORKDIR /src

COPY requirements.txt .
RUN pip install --proxy http://akhmed@gu-ito-ws05:S@likh0v@proxy.giop.local:3128 --no-cache-dir -r requirements.txt

COPY src/ .

ENV PYTHONPATH /

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]