The sonoUno library provides generic tools to import audio files, transform the sound waves and export them.
The most important class is the `Track` class. It stores information intrinsic the sound waves:

- the sampling rate (default: 44100 Hz)
- the maximum amplitude (default: 1)
- the sound wave as a float64 numpy array.

and also a timestamp marker `cue_write` that indicates when will occur the next writing on the track. Tracks manage their own data buffer, which is automatically resized as more sounds are added to it.

## Reading WAV files
Wave files can be imported as a `Track`:

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
    track.set_cue_write(starting_time).add_sine_wave(frequency, duration)
track.play()
```

## Playing notes

The [scientific pitch notation](https://en.wikipedia.org/wiki/Scientific_pitch_notation) can be used to play notes. For instance: the notes C<sub><small>4</small></sub>, F<sup>♯</sup><sub><small>4</small></sub> and G<sup>♭</sup><sub><small>4</small></sub> can be referenced by the strings `'C4'`, `'F#4'` and `'Gb4'`.
```python
```

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
