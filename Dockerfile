# Pull base image
FROM python:3.10-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN adduser --disabled-password --gecos '' sonounolib

# Install the PortAudio dependencies
RUN apt-get update && apt-get install -y curl libsndfile1-dev libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0

WORKDIR /code/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry POETRY_PREVIEW=1 python \
 && cd /usr/local/bin \
 && ln -s /opt/poetry/bin/poetry \
 && poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /code/

# Allow installing dev dependencies to run tests
RUN poetry install --no-root

# Add Python dependencies
RUN bash -c "poetry run pip install jupyterlab"

# copy application files
COPY . /code

#USER sonounolib
ENTRYPOINT ["poetry", "run", "jupyter", "lab", \
  "--ip=0.0.0.0", "--allow-root", \
  "--NotebookApp.custom_display_url=http://127.0.0.1:8888", \
  "--NotebookApp.root_dir=./notebooks" \
]

ENV PYTHONPATH=/code
