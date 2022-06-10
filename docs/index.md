# Overview

The sonoUno library provides generic tools to sonify scientific data. These tools import audio files, transform the sound waves, export them and play them as a Python script in a browser, a Jupyter notebook or a regular Python file.

## Installation

The installation steps will depend on the environment in which the sonoUno library is used.
- in the browser: no installation steps are required.
- in a Jupyter notebook, the library simply needs to be installed with `pip`:

    ```bash
    $ pip install sonounolib
    ```

- otherwise, using the classic Python interpreter, in addition to the sonoUno library, the cross-platform [PortAudio](http://www.portaudio.com)
needs to be installed to play sounds. For example, on a debian or ubuntu OS, the following package needs to be installed:

    ```bash
    $ apt update
    $ apt install -y libportaudio2
    ```
