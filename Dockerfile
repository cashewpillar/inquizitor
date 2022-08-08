# https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry

FROM python:3.9 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./inquizitor /code/inquizitor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# TODO 
# TRY: COPY ./ /code