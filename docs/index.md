# Overview

The sonoUno library provides tools to sonify scientific data. It provides generic tools to import audio files, transform the sound waves and export them.

## Installation

To use the library to play sounds, it is required to install the cross-platform [PortAudio](http://www.portaudio.com
) dependencies. To read or write files, the cross-platform library [Libsndfile](http://www.mega-nerd.com/libsndfile) is required. For example, on a debian or ubuntu OS, the following packages need to be installed:
```bash
$ apt update
$ apt install -y libportaudio2 libsndfile1
```
Then, the library can be installed using pip:
```bash
$ pip install sonounolib
```

## Demo

!!! note
    The output sound through a dockerized Jupyter notebook on linux can be very glitchy.
    We are investigating this issue.

On linux, the library can be tried using a dockerized Jupyter notebook.

```bash
$ docker run --network host --device /dev/snd --rm pchanial/sonounolib:0.2.3
```
Instructions are then displayed and the Jupyter lab server can be accessed in a browser by copy and pasting a URL of the form: `http://127.0.0.1:8888/lab?token=bc03475af361693e02cfff472ae54cb879be49b2e6d500c6`. To run the demo, select the notebooke `demo.ipynb` in the left panel.


Otherwise, the demo notebook can be inspected [here](https://gitlab.com/pchanial/sonouno-library/-/blob/main/notebooks/demo.ipynb).
