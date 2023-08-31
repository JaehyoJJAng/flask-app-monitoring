FROM python:3.9-slim-buster

WORKDIR /app

ENV PYTHONBUFFERED=0

COPY ./requirements/requirements.txt ./requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./ ./

ARG PORT=5001

EXPOSE ${PORT}

CMD [ "python", "main.py" ]
