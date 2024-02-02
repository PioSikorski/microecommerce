FROM python:3.11-slim

WORKDIR /service

COPY . /service

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /service/app

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]