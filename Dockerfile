FROM python:3.9-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install --no-install-recommends -y curl build-essential
RUN apt-get install -y git
RUN apt install -y netcat

RUN pip3 install --upgrade pip
COPY ./app .
RUN mkdir ~/.config
RUN mkdir ~/.config/gspread
COPY service_account.json .
RUN mv service_account.json ~/.config/gspread/service_account.json

RUN pip3 install -r ./requirements.txt

RUN chmod u+x ./entrypoints/web_entrypoint.sh
RUN chmod u+x ./entrypoints/bot_entrypoint.sh
