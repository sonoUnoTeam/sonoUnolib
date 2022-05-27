from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pytest
from numpy.testing import assert_allclose

from sonounolib import Track

from .helpers import file_like


@pytest.mark.parametrize('max_amplitude', [1.0, 10.0])
@pytest.mark.parametrize('file_type', [str, Path, BytesIO])
@pytest.mark.parametrize('format', ['int16', 'int32', 'float32', 'float64'])
def test_write_to_wav(max_amplitude: float, file_type: type, format: str) -> None:
    track_in = Track(rate=2, max_amplitude=max_amplitude)
    track_in.add_raw_data([1, -1, 0.5, -0.5])
    with file_like(file_type) as f:
        track_in.to_wav(f)

        if isinstance(f, BytesIO):
            f.seek(0)

        track_out = Track.load(f, max_amplitude=max_amplitude)

    assert track_in.rate == track_out.rate
    assert track_in.max_amplitude == track_out.max_amplitude
    assert_allclose(
        track_in.get_data(), track_out.get_data(), atol=1 / 32767 * max_amplitude
    )


def test_write_to_invalid_format() -> None:
    track = Track(rate=2)
    track.add_raw_data([1, -1, 0.5, -0.5])
    with pytest.raises(ValueError, match='Cannot infer a wave format for data type'):
        track.to_wav('track.wav', format='uint8')  # type: ignore[arg-type]
