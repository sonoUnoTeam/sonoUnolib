from __future__ import annotations

from typing import Any

import numpy as np
import pytest
from numpy.testing import assert_array_equal
from numpy.typing import ArrayLike

from sonounolib.utils import asmax_amplitude, pad_along_axis


@pytest.mark.parametrize(
    'max_amplitude, expected_amplitude',
    [
        ('int16', 32767),
        ('int32', 2147483647),
        ('float', 1),
        ('float32', 1),
        ('float64', 1),
        (3, 3),
        (3.0, 3),
        (np.float32(3), 3),
    ],
)
def test_track_init_max_amplitude(
    max_amplitude: float | str, expected_amplitude: float
) -> None:
    actual_amplitude = asmax_amplitude(max_amplitude)
    assert asmax_amplitude(max_amplitude) == expected_amplitude
    assert type(actual_amplitude) is float


@pytest.mark.parametrize('value', [True, slice(10)])
def test_asmax_amplitude_invalid_type(value: Any) -> None:
    with pytest.raises(TypeError, match='Invalid maximum amplitude of type'):
        asmax_amplitude(value)


@pytest.mark.parametrize('value', ['uint8', 'xxx'])
def test_asmax_amplitude_invalid_str(value: str) -> None:
    with pytest.raises(ValueError, match='The maximum amplitude cannot be inferred'):
        asmax_amplitude(value)


@pytest.mark.parametrize(
    'array, axis, expected',
    [
        ([1, 1], -1, [1, 1, 0]),
        ([1, 1], 0, [1, 1, 0]),
        ([[1, 1], [2, 2]], -1, [[1, 1, 0], [2, 2, 0]]),
        ([[1, 1], [2, 2]], 0, [[1, 1], [2, 2], [0, 0]]),
    ],
)
def test_pad_along_axis(array: ArrayLike, axis: int, expected: ArrayLike) -> None:
    actual = pad_along_axis(array, 1, axis=axis)
    assert_array_equal(actual, expected)
