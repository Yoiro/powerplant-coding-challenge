FROM python:slim

ENV FLASK_ENV=prod \
    FLASK_APP=/app/powerplant

RUN mkdir /app
WORKDIR /app

# Install poetry
RUN pip install poetry \
 && useradd --create-home -s /bin/bash gunicorn

COPY poetry.lock pyproject.toml wsgi.py README.md config.py /app/

RUN poetry config virtualenvs.create false \
 &&poetry install \
 && poetry install --no-dev

COPY powerplant /app/powerplant

RUN chown -R gunicorn /app \
 && find /app -type f -print0 | xargs -0 chmod 644

EXPOSE 8888

USER gunicorn

ENTRYPOINT ["poetry"]
CMD ["run", "gunicorn", "-w", "4", "-b", "0.0.0.0:8888", "powerplant:create_app()"]
