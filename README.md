# The sonoUno Sonification Library

The sonoUno library provides generic tools to sonify scientific data. These tools import audio files, transform the sound waves, export them and play them as a Python script in a browser, a Jupyter notebook or a regular Python file.

The documentation is [https://pchanial.gitlab.io/sonouno-library](https://pchanial.gitlab.io/sonouno-library).

## Demo

On linux, one can experiment with the library using a dockerized Jupyter notebook.

```bash
$ docker run --network host --rm pchanial/sonounolib:0.5.2
```
Instructions are then displayed and the Jupyter lab server can be accessed in a browser by copy and pasting a URL of the form: `http://127.0.0.1:8888/lab?token=bc03475af361693e02cfff472ae54cb879be49b2e6d500c6`. To run the demo, select the notebooke `demo.ipynb` in the left panel.


Otherwise, the demo notebook can be inspected [here](notebooks/demo.ipynb).
