FROM python:3.11-slim

WORKDIR /src

ADD ./src/ /src/

RUN pip install -r requirements.txt

CMD ["/src/tests/start-test.sh"]