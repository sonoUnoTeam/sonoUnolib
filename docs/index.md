# Overview

The sonoUno library provides tools to sonify scientific data. It provides generic tools to import audio files, transform the sound waves and export them.

## Installation

If used in a Jupyter notebook, the library do not require an external library to play sounds. Otherwise, the cross-platform [PortAudio](http://www.portaudio.com) is needed. For example, on a debian or ubuntu OS, the following package needs to be installed:
```bash
$ apt update
$ apt install -y libportaudio2
```
Then, the library can be installed using pip:
```bash
$ pip install sonounolib
```

## Demo

On linux, the library can be tried using a dockerized Jupyter notebook.

```bash
$ docker run --network host --device /dev/snd --rm pchanial/sonounolib:0.4.0
```
Instructions are then displayed and the Jupyter lab server can be accessed in a browser by copy and pasting a URL of the form: `http://127.0.0.1:8888/lab?token=bc03475af361693e02cfff472ae54cb879be49b2e6d500c6`. To run the demo, select the notebooke `demo.ipynb` in the left panel.


Otherwise, the demo notebook can be inspected [here](https://gitlab.com/pchanial/sonouno-library/-/blob/main/notebooks/demo.ipynb).
