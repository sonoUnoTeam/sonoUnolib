# Pull base image
FROM python:3.10-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN adduser --disabled-password --gecos '' sonounolib

WORKDIR /code/

# Install Poetry
RUN pip install poetry==1.2.0b1 \
 && poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /code/

# Allow installing dev dependencies to run tests
RUN poetry install --no-root --without dev

# Add Python dependencies
RUN poetry run pip install --upgrade pip
RUN poetry run pip install --root-user-action=ignore jupyterlab

# copy application files
COPY . /code

#USER sonounolib
ENTRYPOINT ["poetry", "run", "jupyter", "lab", \
  "--ip=0.0.0.0", "--allow-root", \
  "--ServerApp.custom_display_url=http://127.0.0.1:8888", \
  "--ServerApp.root_dir=./notebooks" \
]

ENV PYTHONPATH=/code
