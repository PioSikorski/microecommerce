FROM python:3.11-slim

WORKDIR /service/src/product/

COPY ./src/__init__.py /service/src/

COPY ./src/core/ /service/src/core/

COPY ./src/product/ /service/src/product/

WORKDIR /service/src/product/

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /service

CMD [ "uvicorn", "src.product.app.main:app", "--host", "0.0.0.0", "--port", "8000" ]