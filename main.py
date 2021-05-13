import random

from musx.generators import choose
from musx.midi.gm import Marimba, AcousticGrandPiano, Harpsichord
from musx.midi.midifile import MidiFile
from musx.midi.midiseq import MidiSeq
from musx.ran import between
from musx.rhythm import rhythm
from musx.scales import scale
from musx.scheduler import Scheduler

from src.instrument import bass_double, bass, soprano, ornament, backbone
from src.notes import pentatonic, pentatonic_backbone_chord
from src.tools import rotate, multi_operation, pull_octaves, list_reverse
from src.rhythms import fading, steve_reich, alter_chords, longing

"""
Define composition name
"""

COMP_NAME = 'comp.mid'

"""
Define rhythm
"""

TEMPO = between(96, 120)
quarter_beats_per_minute = rhythm('q', TEMPO, beat=0.25)
quarter_beats_per_measure = 6
time_signature = [quarter_beats_per_measure, 4]


def measure_time(measure: int):
    return measure * quarter_beats_per_measure * quarter_beats_per_minute


"""
Define root and scale
"""

TONIC = random.choice(scale(0, 12, 7, fit=[60, 72, 'wrap']))
TONIC_SCALE = pentatonic(TONIC)
PREDOMINANT = TONIC + 5
DOMINANT = TONIC + 7

soprano_range = multi_operation(TONIC_SCALE, pull_octaves(1))
bass_range = multi_operation(TONIC_SCALE, pull_octaves(-2))

"""
Define amplitudes
"""

backbone_chord_amp = 0.35
backbone_sequence_amp = 0.45
bass_amp = 0.5
bass_fade_in = bass_amp + 0.1
soprano_amp = 0.6
soprano_fade_in = soprano_amp + 0.1
ornament_amp = 0.5

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

piano_chord_chan = {0, 1}
marimba_chord_chan = {2, 3}
backbone_chan = 4
soprano_chan = choose([5, 6, 7, 8, 9])
bass_chan = 10,
bass_double_chan = 11
ornament_chan = 12

"""
MIDI related
"""

meta_seq = MidiSeq.metaseq(ins=ins, timesig=time_signature, tempo=TEMPO)
seq = MidiSeq()
q: Scheduler = Scheduler(seq)

"""
Composing!
"""

curr_measure = 0

piano_chord, marimba_chord = pentatonic_backbone_chord(TONIC)
piano_chord_rev = list_reverse(piano_chord)
marimba_chord_rev = list_reverse(marimba_chord)

# Start Section

start_measures = between(5, 8)
num_beats = 2 * 6 * start_measures
q.compose(
    [measure_time(curr_measure),
     alter_chords(q, keys_stacked=piano_chord, quarter_beats=quarter_beats_per_minute, amp=backbone_chord_amp,
                  channel=0, num_beats=num_beats)])
q.compose(
    [measure_time(curr_measure),
     alter_chords(q, keys_stacked=piano_chord_rev, quarter_beats=quarter_beats_per_minute, amp=backbone_chord_amp,
                  channel=1, num_beats=num_beats)])
q.compose(
    [measure_time(curr_measure),
     alter_chords(q, keys_stacked=marimba_chord, quarter_beats=quarter_beats_per_minute, amp=backbone_chord_amp,
                  channel=2, num_beats=num_beats)])
q.compose(
    [measure_time(curr_measure),
     alter_chords(q, keys_stacked=marimba_chord_rev, quarter_beats=quarter_beats_per_minute, amp=backbone_chord_amp,
                  channel=3, num_beats=num_beats)])

curr_measure += start_measures

# Middle Parts

for i in range(between(4, 6)):
    pass

# End Section

end_measures = between(5, 8)
num_beats = 2 * 6 * start_measures
q.compose(
    [measure_time(curr_measure),
     alter_chords(q, keys_stacked=piano_chord, quarter_beats=quarter_beats_per_minute, amp=backbone_chord_amp,
                  channel=0, num_beats=num_beats)])
q.compose(
    [measure_time(curr_measure),
     alter_chords(q, keys_stacked=piano_chord_rev, quarter_beats=quarter_beats_per_minute, amp=backbone_chord_amp,
                  channel=1, num_beats=num_beats)])
q.compose(
    [measure_time(curr_measure),
     alter_chords(q, keys_stacked=marimba_chord, quarter_beats=quarter_beats_per_minute, amp=backbone_chord_amp,
                  channel=2, num_beats=num_beats)])
q.compose(
    [measure_time(curr_measure),
     alter_chords(q, keys_stacked=marimba_chord_rev, quarter_beats=quarter_beats_per_minute, amp=backbone_chord_amp,
                  channel=3, num_beats=num_beats)])

curr_measure += end_measures

"""
Write file
"""

MidiFile(COMP_NAME, [meta_seq, seq]).write()
