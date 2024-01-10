FROM python:3.11

# System deps:
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY .. /code

RUN poetry install

CMD ["poetry", "run", "python", "src/run_api.py"]
