FROM python:3.10.8-alpine3.16

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Moscow \
    LANG=C.UTF-8

COPY ./requirements.txt /app/requirements.txt
COPY ./alembic.ini /alembic.ini

RUN pip install --upgrade pip setuptools && \
    pip install  --no-warn-script-location -r /app/requirements.txt && \
    rm -rf /root/.cache/pip

COPY ./app/ /app/
