from __future__ import annotations

import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal, assert_array_equal

from sonounolib import Track


def test_track_init() -> None:
    track = Track()
    assert track.rate == track.DEFAULT_TRACK_RATE
    assert track.duration == 0
    assert track.cue_write == 0.0
    assert_array_equal(track.get_data(), [])
    assert track._index_write == 0
    assert track._size == 0
    assert track._data.shape == (0,)


@pytest.mark.parametrize(
    'max_amplitude, expected_amplitude',
    [
        ('int16', 32767),
        (14, 14),
    ],
)
def test_track_init_max_amplitude(
    max_amplitude: float | str, expected_amplitude: float
) -> None:
    track = Track(max_amplitude=max_amplitude)
    assert track.max_amplitude == expected_amplitude


def test_track_init_max_amplitude_invalid() -> None:
    with pytest.raises(ValueError, match='maximum amplitude cannot be inferred'):
        Track(max_amplitude='unknown type')


def test_set_cue_write_inside() -> None:
    track = Track(rate=4).add_raw_data([1, 1, 1, 1])
    track.set_cue_write(0.25)
    track.add_raw_data([2, 2])
    assert_array_almost_equal(track.get_data(), [1, 3, 3, 1])
    assert track.shape == (4,)
    assert track._data.shape == (4,)
    assert_array_almost_equal(track._data, [1, 3, 3, 1])
    assert track._index_write == 3
    assert track._size == 4


def test_set_cue_write_extend() -> None:
    track = Track(rate=4).add_raw_data([1, 1, 1, 1])
    track.set_cue_write(0.75)
    track.add_raw_data([2, 2])
    assert_array_almost_equal(track.get_data(), [1, 1, 1, 3, 2])
    assert_array_almost_equal(track._data, [1, 1, 1, 3, 2, 0, 0, 0, 0])
    assert track.shape == (5,)
    assert track._data.shape == (9,)
    assert track._index_write == 5
    assert track._size == 5


def test_set_cue_write_negative() -> None:
    track = Track()
    with pytest.raises(ValueError, match='Negative cue write value'):
        track.set_cue_write(-1)


def test_get_data_duration() -> None:
    track = Track()
    with pytest.raises(NotImplementedError):
        track.get_data(duration=1)


def test_get_data_cue_read_negative() -> None:
    track = Track()
    with pytest.raises(ValueError, match='Negative cue read value'):
        track.get_data(cue_read=-1)


@pytest.mark.parametrize('n', [1, 2, 3])
def test_repeat(n: int) -> None:
    track = Track().add_sine_wave(440, 1)
    data = track.get_data()
    size = data.shape[-1]
    track.repeat(n)
    new_data = track.get_data()
    assert new_data.shape[-1] == n * data.shape[-1]
    for i in range(n):
        assert_array_equal(new_data[..., i * size : (i + 1) * size], data)  # noqa: E203


@pytest.mark.parametrize('n', [1, 2, 3])
def test_repeat_empty(n: int) -> None:
    track = Track().repeat(n)
    assert track.shape[-1] == 0


@pytest.mark.parametrize('n', [-1, 0])
def test_repeat_invalid(n: int) -> None:
    with pytest.raises(ValueError, match='The number of repeats is less than one'):
        Track().repeat(n)


def test_add_track_extend() -> None:
    sound = Track(rate=2)
    sound._data = np.array([1.0, -1])
    sound._index_write = 2
    sound._size = 2
    assert_array_equal(sound.get_data(), [1, -1])
    assert sound.duration == 1
    assert sound.cue_write == 1
    track = Track(rate=2)

    track.add_track(sound)
    assert_array_equal(track.get_data(), [1, -1])
    assert track.duration == 1
    assert sound.cue_write == 1
    assert track._index_write == 2
    assert track._size == 2
    assert track._data.shape == (2,)

    track.add_track(sound)
    assert_array_equal(track.get_data(), [1, -1, 1, -1])
    assert track._index_write == 4
    assert track._size == 4
    assert track._data.shape == (6,)

    track.add_blank(1)
    assert_array_equal(track.get_data(), [1, -1, 1, -1, 0, 0])
    assert track._index_write == 6
    assert track._size == 6
    assert track._data.shape == (6,)

    track.add_blank(1)
    assert_array_equal(track.get_data(), [1, -1, 1, -1, 0, 0, 0, 0])
    assert track._index_write == 8
    assert track._size == 8
    assert track._data.shape == (6,)

    track.add_track(sound)
    assert_array_equal(track.get_data(), [1, -1, 1, -1, 0, 0, 0, 0, 1, -1])
    assert track._index_write == 10
    assert track._size == 10
    assert track._data.shape == (18,)


def test_add_track_incompatible_rate() -> None:
    track1 = Track(rate=2)
    with pytest.raises(ValueError, match='Cannot mix tracks with different sampling'):
        track1.add_track(Track(rate=4))


def test_add_track_different_max_amplitude() -> None:
    track1 = Track(rate=2)
    track2 = Track(rate=2, max_amplitude=10)
    track2.add_raw_data([10, -10])
    track1.add_track(track2)
    assert_array_equal(track1.get_data(), [1.0, -1.0])


def test_add_blank() -> None:
    track = Track(rate=2)
    assert track.shape == (0,)
    assert list(track.get_data()) == []
    assert track._data.shape == (0,)
    track.add_blank(2)
    assert_array_equal(track.get_data(), [0, 0, 0, 0])
    assert_array_equal(track._data, [])


def test_add_after_blank() -> None:
    track = Track(rate=2).add_blank(2)
    track.add_raw_data([1, -1])
    assert_array_equal(track.get_data(), [0, 0, 0, 0, 1, -1])
    assert_array_equal(track._data, [0, 0, 0, 0, 1, -1, 0, 0, 0, 0])


def test_add_sine_wave() -> None:
    track = Track(rate=4).add_sine_wave(1, 1, 1)
    assert_array_almost_equal(track.get_data(), [0, 1, 0, -1])
    assert_array_almost_equal(track._data, [0, 1, 0, -1])


def test_add_sine_wave_max_amplitude() -> None:
    track = Track(rate=4, max_amplitude=2).add_sine_wave(1, 1, 2)
    assert_array_almost_equal(track.get_data(), [0, 2, 0, -2])


def test_add_sine_wave_negative_amplitude() -> None:
    with pytest.raises(ValueError, match='is negative'):
        Track(rate=4).add_sine_wave(1, 1, -1)


def test_add_sine_wave_greater_amplitude() -> None:
    with pytest.raises(ValueError, match='greater than'):
        Track(rate=4, max_amplitude=2).add_sine_wave(1, 1, 2.1)
