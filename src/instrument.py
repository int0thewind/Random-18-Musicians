from musx.generators import choose
from musx.midi.gm import AcousticGrandPiano, Cello, Bassoon, Tuba, Violin, Flute, Clarinet, \
    Xylophone, Celesta, Marimba

backbone = choose([Marimba, AcousticGrandPiano])

# bass_double = choose([AcousticGrandPiano, Cello], [1, 2])

bass = choose([AcousticGrandPiano, Cello, Tuba, Bassoon], [1, 2, 4, 4])

soprano = choose([Flute, Clarinet, Violin, AcousticGrandPiano], [4, 3, 3, 1])

ornament = choose([Xylophone, Celesta], [4, 4])
