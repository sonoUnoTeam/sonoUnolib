"""Provides an appropriate audio player according to current environment."""
from __future__ import annotations

import sys
import typing
import warnings
from abc import ABC, abstractmethod
from io import BytesIO
from typing import Any

if typing.TYPE_CHECKING:
    from .tracks import Track

IPython = sys.modules.get('IPython')
pyodide = sys.modules.get('pyodide')
sounddevice = None

if (
    pyodide is None
    and IPython is not None
    and (
        not IPython.get_ipython()
        or IPython.get_ipython().__class__.__name__ == 'TerminalInteractiveShell'
    )
):  # pragma: no cover
    IPython = None

if pyodide is None and IPython is None:  # pragma: no cover
    try:
        import sounddevice  # type: ignore[no-redef]
    except OSError as exc:
        with warnings.catch_warnings():
            warnings.simplefilter('always')
            warnings.warn(str(exc), ImportWarning)


class Player(ABC):
    """The abstract class for an audio player."""

    @abstractmethod
    def play(
        self,
        track: Track,
        cue_read: float = 0,
        duration: float | None = None,
    ) -> Any:
        """Plays the requested audio waves.

        Arguments:
            track: The sound track to be played.
            cue_read: The starting time for playing the data.
            duration: The number of seconds to be played.
        """


class IPythonPlayer(Player):
    """An audio player using IPython as backend."""

    def play(
        self,
        track: Track,
        cue_read: float = 0,
        duration: float | None = None,
    ) -> Any:
        """Plays the requested audio waves using IPython audio.

        Arguments:
            track: The sound track to be played.
            cue_read: The starting time for playing the data.
            duration: The number of seconds to be played.

        Returns:
            An instance of IPython.display.Audio.
        """
        assert IPython is not None
        data = track.get_data(cue_read=cue_read, duration=duration)
        audio = IPython.display.Audio(
            data / track.max_amplitude, rate=track.rate, autoplay=True, normalize=False
        )
        return audio


class PyodidePlayer(Player):
    """An audio player using the browser as backend."""

    def play(
        self,
        track: Track,
        cue_read: float = 0,
        duration: float | None = None,
    ) -> Any:
        """Plays the requested audio waves using browser audio.

        Arguments:
            track: The sound track to be played.
            cue_read: The starting time for playing the data.
            duration: The number of seconds to be played.

        Returns:
            An instance of IPython.display.Audio.
        """
        from pyodide import create_proxy

        buffer = BytesIO()
        track.to_wav(buffer, format='int16', cue_read=cue_read, duration=duration)
        data = buffer.getvalue()

        proxy = create_proxy(data)
        proxy_buffer = proxy.getBuffer()

        try:
            from js import URL, Blob, document

            blob = Blob.new([proxy_buffer.data], {'type': 'audio/wav'})
            blob_url = URL.createObjectURL(blob)
            audio = document.getElementsByTagName('audio')[0]
            audio.src = blob_url
        finally:
            proxy_buffer.release()
            proxy.destroy()


class PortAudioPlayer(Player):
    """An audio player using PortAudio as backend."""

    def __init__(self) -> None:
        """The PortAudioPlayer constructor."""
        assert sounddevice is not None
        if sounddevice.default.device[1] == -1:
            raise OSError('There is no output device available.')

    def play(
        self,
        track: Track,
        cue_read: float = 0,
        duration: float | None = None,
    ) -> None:
        """Plays the requested audio waves using PortAudio.

        Arguments:
            track: The sound track to be played.
            cue_read: The starting time for playing the data.
            duration: The number of seconds to be played.
        """
        assert sounddevice is not None
        data = track.get_data(cue_read=cue_read, duration=duration)
        sounddevice.play(data / track.max_amplitude, track.rate, blocking=True)


def get_player() -> Player:
    """Returns an audio player according to the current environment."""
    if (
        IPython
        and IPython.get_ipython()
        and IPython.get_ipython().__class__.__name__ != 'TerminalInteractiveShell'
    ):
        return IPythonPlayer()
    if pyodide:
        return PyodidePlayer()
    if sounddevice:
        return PortAudioPlayer()
    raise OSError(
        'Could not find an appropriate player. Nor IPython (Jupyter) nor '
        'sounddevice (PortAudio) are installed.'
    )
