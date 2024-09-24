# `python-base` sets up all our shared environment variables
FROM python:3.12.4-slim

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        # deps for building python deps
        build-essential


# install postgres dependencies inside of Docker
RUN apt-get update \
    && apt-get -y install libpq-dev gcc python3-dev \
    && pip install psycopg2 

# copy project requirement files here to ensure they will be cached.

# quicker install as runtime deps are already installed

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "entrypoint.sh"]