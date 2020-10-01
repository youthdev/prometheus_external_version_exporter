FROM python:3.7-alpine

WORKDIR /app/exporter

ADD exporter/requirements.txt ./

RUN pip install -r requirements.txt

WORKDIR /app

ENV PYTHONUNBUFFERED=1

ADD ./exporter /app/exporter
ADD ./config.yaml ./config.yaml

CMD [ "python", "exporter" ]