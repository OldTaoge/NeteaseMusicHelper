FROM python:3.9.5-alpine
WORKDIR /usr/src/app
RUN apk add --no-cache git zlib-dev jpeg-dev gcc musl-dev ffmpeg \
    && git clone https://github.com/OldTaoge/NeteaseMusicHelper.git . \
    && pip install --no-cache-dir -r requirements.txt
ENTRYPOINT  python NEM-main.py