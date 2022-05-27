import IPython.display
import pytest
from pytest_mock import MockerFixture

import sonounolib
from sonounolib import Track
from sonounolib.players import PortAudioPlayer, get_player


def test_player_ipython(mocker: MockerFixture) -> None:
    pytest.importorskip('IPython')
    mocker.patch('IPython.get_ipython', return_value='ZMQInteractiveShell')
    audio = Track().add_sine_wave(440, 0.01).play()
    assert isinstance(audio, IPython.display.Audio)


def test_player_portaudio(mocker: MockerFixture) -> None:
    sounddevice = pytest.importorskip('sounddevice')
    mocker.patch('sonounolib.players.sounddevice', sounddevice)
    player = get_player()
    assert isinstance(player, PortAudioPlayer)
    track = Track().add_sine_wave(440, 0.01)
    assert track.play() is None


def test_player_portaudio_no_device(mocker: MockerFixture) -> None:
    sounddevice = pytest.importorskip('sounddevice')
    mocker.patch('sonounolib.players.sounddevice', sounddevice)
    mocker.patch.object(sonounolib.players.sounddevice.default, 'device', (-1, -1))  # type: ignore[attr-defined]
    with pytest.raises(OSError, match='There is no output device available'):
        get_player()


def test_player_no_backend(mocker: MockerFixture) -> None:
    mocker.patch('sonounolib.players.sounddevice', None)
    with pytest.raises(OSError, match='Could not find an appropriate player'):
        get_player()
