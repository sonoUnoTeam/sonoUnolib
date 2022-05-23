# The sonoUno Sonification Library

## Installation

To use the library interactively to play sounds, it is required to install the cross-platform [PortAudio](http://www.portaudio.com
) dependencies. For example, on a debian or ubuntu OS, the following packages need to be installed:
```bash
$ apt update
$ apt install -y curl libsndfile1-dev libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
```
Then, the library can be installed using pip:
```bash
$ pip install sonounolib
```

## Demo
On linux, the library can be tried using a dockerized Jupyter notebook.

```bash
$ docker run --network host --device /dev/snd -it pchanial/sonounolib:0.1.0
```
Instructions are then displayed and the Jupyter lab server can be accessed in a browser by copy and pasting a URL of the form: `http://127.0.0.1:8888/lab?token=bc03475af361693e02cfff472ae54cb879be49b2e6d500c6`. To run the demo, select the notebooke `demo.ipynb` in the left panel.


Otherwise, the demo notebook can be inspected [here](notebooks/demo.ipynb).


## Examples

Playing a sine waves of different frequencies

```python
import numpy as np
from sonounolib import Track

track = Track()
scale = np.linspace(440, 880, 13)
frequencies = np.tile(np.concatenate([scale, scale[::-1]]), 2)
for frequency in frequencies:
    track.add_sine_wave(frequency, 0.2)
track.play()
```
Playing notes
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
