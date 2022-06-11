import numpy as np
import pytest
from pytest_mock import MockerFixture

import sonounolib
from sonounolib import Track
from sonounolib.players import IPythonPlayer, PortAudioPlayer, get_player


def test_player_ipython(mocker: MockerFixture) -> None:
    IPython = pytest.importorskip('IPython')
    mocker.patch('sonounolib.players.IPython', IPython)
    mocker.patch('sonounolib.players.pyodide', None)
    mocker.patch('IPython.get_ipython', return_value='ZMQInteractiveShell')
    audio = Track().add_sine_wave(440, 0.01).play()
    assert isinstance(audio, IPython.display.Audio)


def test_player_portaudio(mocker: MockerFixture) -> None:
    try:
        sounddevice = pytest.importorskip('sounddevice')
    except OSError as exc:
        pytest.skip(str(exc))
    mocker.patch('sonounolib.players.pyodide', None)
    mocker.patch('sonounolib.players.sounddevice', sounddevice)
    if sounddevice.default.device[1] == -1:
        mocker.patch.object(sounddevice.default, 'device', (-1, 0))
        mocker.patch('sounddevice.play')
    player = get_player()
    assert isinstance(player, PortAudioPlayer)
    assert Track().play() is None


def test_player_portaudio_no_device(mocker: MockerFixture) -> None:
    try:
        sounddevice = pytest.importorskip('sounddevice')
    except OSError as exc:
        pytest.skip(str(exc))
    mocker.patch('sonounolib.players.pyodide', None)
    mocker.patch('sonounolib.players.sounddevice', sounddevice)
    mocker.patch.object(sonounolib.players.sounddevice.default, 'device', (-1, -1))  # type: ignore[attr-defined]
    with pytest.raises(OSError, match='There is no output device available'):
        get_player()


def test_player_no_backend(mocker: MockerFixture) -> None:
    mocker.patch('sonounolib.players.pyodide', None)
    mocker.patch('sonounolib.players.sounddevice', None)
    with pytest.raises(OSError, match='Could not find an appropriate player'):
        get_player()


def test_player_ipython_normalization(mocker: MockerFixture) -> None:
    IPython = pytest.importorskip('IPython')
    mocker.patch('sonounolib.players.IPython', IPython)
    track = Track(max_amplitude='int16')
    track.add_sine_wave(440, 0.01, np.iinfo(np.int16).max)
    player = IPythonPlayer()
    player.play(track)
