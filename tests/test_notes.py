import numpy as np
import pytest

from sonounolib.notes import asfrequency, get_note_frequencies


@pytest.mark.parametrize(
    'note, expected_frequency',
    [('A0', 27.5), ('A4', 440), ('C#4', 277.1826), ('Db4', 277.1826)],
)
def test_note_frequency(note: str, expected_frequency: float) -> None:
    notes = get_note_frequencies()
    assert np.isclose(notes[note], expected_frequency, atol=1e-4)


@pytest.mark.parametrize('note', ['B-1', 'C11', 'B#4', 'Cb4', 'xxx'])
def test_note_frequency_error(note: str) -> None:
    with pytest.raises(ValueError, match='Unknown note'):
        asfrequency(note)
