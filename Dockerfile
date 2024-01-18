FROM python:3.11-buster

ENV TZ=Europe/Moscow

RUN apk add --no-cache tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
CMD python3 bot.py