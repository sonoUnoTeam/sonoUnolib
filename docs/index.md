# Overview

The sonoUno library provides tools to sonify scientific data. It provides generic tools to import audio files, transform the sound waves, export them and play them as a Python script in a browser, a Jupyter notebook or a regular Python file.

## Installation

When used in the browser, no installation steps are required. When used in Jupyter notebooks, the library simply needs to be installed with `pip`:
```bash
$ pip install sonounolib
```

Otherwise, the cross-platform [PortAudio](http://www.portaudio.com) is used to play sounds. For example, on a debian or ubuntu OS, the following package needs to be installed, in addition to the sonoUno library:
```bash
$ apt update
$ apt install -y libportaudio2
```
