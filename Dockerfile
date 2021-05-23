FROM python:3.9.5-alpine
WORKDIR /usr/src/app
COPY Utils requirements.txt data.json NEM*.py /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT  python NEM-main.py