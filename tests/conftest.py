from typing import Iterator

import pytest
from responses import RequestsMock


@pytest.fixture
def mocked_responses() -> Iterator[RequestsMock]:
    with RequestsMock() as rsps:
        yield rsps
