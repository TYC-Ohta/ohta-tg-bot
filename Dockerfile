FROM python:3.12-alpine3.20

WORKDIR /app/

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

CMD ["python3", "/app/main.py"]