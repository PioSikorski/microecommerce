FROM python:3.11-slim

WORKDIR /service/src/order/

COPY ./src/__init__.py /service/src/

COPY ./src/core/ /service/src/core/

COPY ./src/order/ /service/src/order/

COPY ./src/requirements.txt /service/

WORKDIR /service

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "uvicorn", "src.order.app.main:app", "--host", "0.0.0.0", "--port", "8000" ]