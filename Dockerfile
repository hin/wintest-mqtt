FROM python:3.7.1-alpine3.8

RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY main.py /app

CMD python main.py
