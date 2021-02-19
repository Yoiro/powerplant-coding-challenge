FROM python:slim

ENV FLASK_ENV=prod \
    FLASK_APP=/app/powerplant

RUN mkdir /app
WORKDIR /app

COPY poetry.lock pyproject.toml wsgi.py README.md config.py /app/
COPY powerplant /app/powerplant

RUN pip install poetry \
 && useradd --create-home -s /bin/bash gunicorn \
 && poetry config virtualenvs.create false \
 && poetry install \
 && poetry install --no-dev \
 && chown -R gunicorn /app \
 && find /app -type f -print0 | xargs -0 chmod 644

EXPOSE 8888

USER gunicorn

ENTRYPOINT ["poetry"]
CMD ["run", "gunicorn", "-w", "4", "-b", "0.0.0.0:8888", "wsgi:app"]
