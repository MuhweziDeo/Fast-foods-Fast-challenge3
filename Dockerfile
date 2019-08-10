FROM ubuntu:16.04

RUN apt-get update -y

RUN apt-get install -y python3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD python3 run.py
