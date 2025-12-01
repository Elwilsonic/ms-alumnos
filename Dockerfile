FROM python:3.14-slim

ENV FLASK_CONTEXT=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/flaskapp/.venv/bin

RUN useradd --create-home --home-dir /home/flaskapp flaskapp
RUN apt-get update
RUN apt-get install -y python3-dev build-essential libpq-dev python3-psycopg2 curl ca-certificates
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /home/flaskapp

# Instalar uv como root y mover el binario a /usr/local/bin
RUN curl -fsSL https://astral.sh/uv/install.sh | sh \
    && install -m 0755 /root/.local/bin/uv /usr/local/bin/uv
ENV PATH="/usr/local/bin:${PATH}"

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --locked

COPY ./app ./app
COPY ./wsgi.py .

RUN chown -R flaskapp:flaskapp /home/flaskapp

USER flaskapp

ENV VIRTUAL_ENV="/home/flaskapp/.venv"

EXPOSE 5000
CMD ["granian", "--port", "5000", "--host", "0.0.0.0", "--http", "auto", "--workers", "4", "--blocking-threads", "4", "--backlog", "2048", "--interface", "wsgi", "wsgi:app"]
