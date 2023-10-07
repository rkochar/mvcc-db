FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE=1

RUN pip3 install kafka-python faker

COPY producer/producer.py .

COPY ./../utils ./utils

CMD ["python3", "-u", "./producer.py"]
