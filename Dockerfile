FROM python:3.6-alpine

WORKDIR /usr/src/app

ADD requirements.txt ./
RUN apk add --no-cache libressl-dev musl-dev libffi-dev gcc && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk del libressl-dev musl-dev libffi-dev gcc

ADD . .

CMD [ "python", "-u", "./bot.py" ]
