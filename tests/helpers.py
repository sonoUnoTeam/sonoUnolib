from __future__ import annotations

from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import BinaryIO, Iterator


@contextmanager
def file_like(
    file_type: type[str] | type[Path] | type[BytesIO],
) -> Iterator[str | Path | BinaryIO]:
    if file_type is str:
        with NamedTemporaryFile('wb') as f:
            yield f.name
    elif file_type is Path:
        with NamedTemporaryFile('wb') as f:
            yield Path(f.name)
    elif file_type is BytesIO:
        yield BytesIO()
    else:
        raise TypeError
