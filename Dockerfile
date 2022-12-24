FROM docker.io/library/python:3.11-alpine AS poetry-exporter

WORKDIR /work

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN python -m pip install poetry \
 && poetry export -o requirements.txt

FROM docker.io/library/python:3.11

WORKDIR /app

COPY --from=poetry-exporter /work/requirements.txt requirements.txt
RUN python -m pip install pip wheel --upgrade \
 && python -m pip install -r requirements.txt

COPY . .

CMD ["python", "pcm.py"]