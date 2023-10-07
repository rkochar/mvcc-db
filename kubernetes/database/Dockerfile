FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE=1

RUN pip3 install kafka-python

COPY database/database.py .
COPY ./../utils ./utils

CMD ["python3", "-u", "./database.py"]
