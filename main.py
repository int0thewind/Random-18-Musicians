import random

from musx.generators import choose
from musx.midi.gm import Marimba, AcousticGrandPiano
from musx.midi.midifile import MidiFile
from musx.midi.midiseq import MidiSeq
from musx.ran import between
from musx.rhythm import rhythm
from musx.scales import scale
from musx.scheduler import Scheduler

from src.instrument import bass_double, bass, soprano, ornament, backbone
from src.notes import pentatonic
from src.tools import rotate, multi_operation, pull_octaves

"""
Define composition name
"""

COMP_NAME = __name__

"""
Define rhythm
"""

quarter_beats_per_minute = rhythm('q', between(180, 210))
quarter_beats_per_measure = 6
time_signature = [6, 4]

"""
Define root and scale
"""

TONIC = random.choice(scale(0, 12, 7, fit=[60, 71, 'wrap']))
TONIC_SCALE = pentatonic(TONIC)
PREDOMINANT = TONIC + 5
DOMINANT = TONIC + 7

"""
Define instruments
"""

ins = {
    0: AcousticGrandPiano,  # Chord backbone
    1: AcousticGrandPiano,  # Chord backbone
    2: Marimba,  # Chord backbone
    3: Marimba,  # Chord backbone

    4: next(backbone),  # Sequential backbone

    5: next(soprano),  # 5 sopranos
    6: next(soprano),  # 5 sopranos
    7: next(soprano),  # 5 sopranos
    8: next(soprano),  # 5 sopranos
    9: next(soprano),  # 5 sopranos

    10: next(bass),  # 1 bass
    11: next(bass_double),  # 1 bass playing two notes

    12: next(ornament),  # 1 ornamental instrument
}

backbone_chan = 4
soprano_chan = choose([5, 6, 7, 8, 9])
bass_chan = 10,
bass_double_chan = 11
ornament_chan = 12

"""
MIDI related
"""

meta_seq = MidiSeq().metaseq(tempo=quarter_beats_per_minute, timesig=time_signature, ins=ins)
seq = MidiSeq()
q: Scheduler = Scheduler(seq)

"""
Composing!
"""


def write_file():
    MidiFile(COMP_NAME, [meta_seq, seq]).write()


if __name__ == '__main__':
    write_file()
