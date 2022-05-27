# The sonoUno Sonification Library

## Installation

If used in a Jupyter notebook, the library do not require an external library to play sounds. Otherwise, the cross-platform [PortAudio](http://www.portaudio.com) is needed. To read or write files, the cross-platform library [Libsndfile](http://www.mega-nerd.com/libsndfile) is required. For example, on a debian or ubuntu OS, the following packages need to be installed:
```bash
$ apt update
$ apt install -y libportaudio2 libsndfile1
```
Then, the library can be installed using pip:
```bash
$ pip install sonounolib
```

## Demo
On linux, the library can be tried using a dockerized Jupyter notebook.

```bash
$ docker run --network host --device /dev/snd --rm pchanial/sonounolib:0.2.3
```
Instructions are then displayed and the Jupyter lab server can be accessed in a browser by copy and pasting a URL of the form: `http://127.0.0.1:8888/lab?token=bc03475af361693e02cfff472ae54cb879be49b2e6d500c6`. To run the demo, select the notebooke `demo.ipynb` in the left panel.


Otherwise, the demo notebook can be inspected [here](notebooks/demo.ipynb).


## Examples

More examples are available in the [demo](notebooks/demo.ipynb).

### Playing a sine waves of different frequencies

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

### Playing notes

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

## Contributing

The sonoUno library uses [pre-commit](https://pre-commit.com) to ensure code quality and uniformity.
To install the pre-commit hooks:

```bash
$ pip install --user pre-commit
$ cd sonounolib
$ pre-commit install
```

The project also uses [poetry](https://python-poetry.org) to manage its package dependencies.

To install the project:
```bash
$ poetry install
```

To run the test suite
```bash
$ poetry run pytest
```
