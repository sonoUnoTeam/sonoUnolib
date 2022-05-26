The sonoUno library uses [pre-commit](https://pre-commit.com) to ensure code quality and uniformity.
To install the pre-commit hooks:

```bash
$ pip install --user pre-commit
$ cd sonounolib
$ pre-commit install
```

The project also uses [poetry](https://python-poetry.org) to manage its package dependencies.

To install the project:
```bash
$ poetry install
```

To run the test suite
```bash
$ poetry run pytest
```
