## Sonification library

Examples

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
