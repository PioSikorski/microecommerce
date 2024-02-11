FROM python:3.11-slim

WORKDIR /service/src/order/

COPY ./src/__init__.py /service/src/

COPY ./src/core/ /service/src/core/

COPY ./src/order/ /service/src/order/

WORKDIR /service/src/order/

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /service

CMD [ "uvicorn", "src.order.app.main:app", "--host", "0.0.0.0", "--port", "8000" ]