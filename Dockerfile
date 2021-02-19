FROM python:alpine

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
 && mkdir /app \
 && useradd -G gunicorn

WORKDIR /app

ADD powerplant/ /app/powerplant/
ADD wsgi.py /app/wsgi.py
ADD poetry.lock /app/poetry.lock

RUN poetry install \
 && rm /app/poetry.lock \
 && chown -r /app gunicorn
 && chmod -R 440 /app

USER gunicorn

ENTRYPOINT ["poetry"]
CMD ["run", "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]