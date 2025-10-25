# |--------- BUILDER ----------|
FROM python:3.13-slim AS builder

ARG HOMEAPP=/usr/src

WORKDIR ${HOMEAPP}

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libmariadb-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip setuptools wheel
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir


# |---------- LOCAL ----------|
FROM python:3.13-slim AS local

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

ARG HOMEAPP=/usr/src

WORKDIR ${HOMEAPP}

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    libmariadb-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

COPY . ${HOMEAPP}

ENTRYPOINT [ "python", "manage.py" ]

CMD [ "runserver", "0.0.0.0:8000" ]
