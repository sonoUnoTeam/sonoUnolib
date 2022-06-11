The most important class provided by the sonoUno library is the [Track](sonounolib.tracks.Track) class. It stores information intrinsic the sound waves:

- the sampling rate (default: 44100 Hz)
- the maximum amplitude (default: 1)
- the sound wave as a float64 numpy array.

and also a timestamp marker `cue_write` that indicates when will occur the next writing on the track. Tracks manage their own data buffer, which is automatically resized as more sounds are added to it.


## Environments

The sonoUno library can currently be used in three different environments:

- In browsers, through the [PyScript](https://pyscript.net) and [Pyodide](https://pyodide.org) projects, which enable running Python natively without transpilation through [WebAssembly](https://webassembly.org). We added the
functionality to inject WAVE files as BLOBs (Binary Large OBjects) in the HTML5 audio tag. To experiment with running
Python (but also many C-compiled libraries, such as Numpy) in a browser and playing sounds, a [demo](demo_pyscript.html) is available.

- In Jupyter notebooks. Here, we rely on the handling of IPython's Audio instances as widgets by Jupyter.
On linux, this environment can be tried using a dockerized Jupyter notebook.

    ```bash
    $ docker run --network host --device /dev/snd --rm pchanial/sonounolib:0.4.0
    ```

    Instructions are then displayed and the Jupyter lab server can be accessed in a browser by copying and pasting a URL of the form: `http://127.0.0.1:8888/lab?token=bc03475af361693e02cfff472ae54cb879be49b2e6d500c6`. To run the demo, select the notebook `demo.ipynb` in the left panel.

    Unlike the previous case, the actual Python code is not executed by the browser, but by a Jupyter server, which runs a CPython kernel.

- In all other cases, the cross-platform [PortAudio](http://www.portaudio.com) is used to play sounds. For example, on a debian or ubuntu OS, the package `libportaudio2` needs to be installed.


## Reading WAVE files
Wave files (or urls) can be imported as a [Track](sonounolib.tracks.Track):

```python
from sonounolib import Track
sound = Track.load('glass-water.wav')
sound.play()
```

## Playing a sine wave

To add a sine wave to the track, it is required to specify

- the oscillation frequency, in Hertz
- the duration, in seconds
- and the amplitude, relative the track's maximum amplitude.

```python
from sonounolib import Track
track = Track().add_sine_wave(440, duration=2., amplitude=1/4)
track.play()
```

By default, a track's maximum amplitude is 1, but any positive value can be used when
instantiating the track. Aliases can be used to specified it:
- `int16`: 32767
- `int32`: 2147483647

Note that when setting the track's maximum amplitude to a value different from 1,
the sine wave amplitudes need to be adjusted:

```python
from sonounolib import Track
track = Track(max_amplitude='int16').add_sine_wave(440, duration=2., amplitude=32767/4)
track.play()
```


## Playing a superposition of sine waves

To superpose other generated sine waves to the track, one has to rewind the cue write at the time when the new sine waves start:
```python
import numpy as np
from sonounolib import Track

frequencies = {octave: 110 * 2**octave for octave in range(0, 8)}

track = Track()
for octave, frequency in frequencies.items():
    starting_time = octave
    duration = len(frequencies) - octave + 1
    track.set_cue_write(starting_time).add_sine_wave(frequency, duration, amplitude=1/8)
track.play()
```

## Playing notes

The [scientific pitch notation](https://en.wikipedia.org/wiki/Scientific_pitch_notation) can be used to play notes. For instance: the notes C<sub><small>4</small></sub>, F<sup>♯</sup><sub><small>4</small></sub> and G<sup>♭</sup><sub><small>4</small></sub> can be referenced by the strings `'C4'`, `'F#4'` and `'Gb4'`.

```python
from sonounolib import Track

notes = 2 * ['C4', 'D4', 'E4', 'C4']
notes += 2 * ['E4', 'F4', 'G4', 'G4']
track = Track()
for note in notes:
    track.add_sine_wave(note, 0.45)
    track.add_blank(0.05)
track.play()
```
