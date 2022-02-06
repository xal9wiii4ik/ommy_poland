FROM python:3.9-alpine as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libjpeg \
    libwebp openjpeg-dev libimagequant-dev

RUN pip3 install --upgrade pip
COPY ./app .

RUN pip3 install -r ./requirements.txt

RUN chmod +x ./entrypoints/web_entrypoint.sh
RUN chmod +x ./entrypoints/bot_entrypoint.sh
