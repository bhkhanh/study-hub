# |--------- BUILDER ----------|
FROM python:3.13-alpine AS builder

ARG HOMEAPP=/usr/src

WORKDIR ${HOMEAPP}

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install -U pip
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir


# |---------- LOCAL ----------|
FROM python:3.13-alpine AS local

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

ARG HOMEAPP=/usr/src

WORKDIR ${HOMEAPP}

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY . ${HOMEAPP}

ENTRYPOINT [ "python", "manage.py" ]

CMD [ "runserver", "0.0.0.0:8000" ]


# |---------- PRODUCTION ----------|
FROM python:3.13-alpine AS production

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

ARG HOMEAPP=/usr/src

WORKDIR ${HOMEAPP}

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY . ${HOMEAPP}

RUN chmod +x ${HOMEAPP}/entrypoint.production.sh

ENTRYPOINT [ "./entrypoint.production.sh" ]

