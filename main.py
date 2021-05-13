import random
from typing import List

from musx.generators import choose, markov
from musx.midi.gm import Marimba, AcousticGrandPiano, Harpsichord
from musx.midi.midifile import MidiFile
from musx.midi.midiseq import MidiSeq
from musx.ran import between
from musx.rhythm import rhythm
from musx.scales import scale
from musx.scheduler import Scheduler

from src.instrument import bass, soprano, ornament, backbone
from src.notes import pentatonic, pentatonic_backbone_chord, longing1, longing2, \
    steve_reich_notes1, steve_reich_notes2, steve_reich_notes_random, steve_reich_notes_prep
from src.tools import rotate, multi_operation, pull_octaves, list_reverse
from src.rhythms import fading, steve_reich, alter_chords, longing

"""
Define composition name
"""

COMP_NAME = 'comp.mid'

"""
Define rhythm
"""

TEMPO = between(112, 120)
quarter_beats_per_minute = rhythm('q', TEMPO, beat=0.25)
quarter_beats_per_measure = 6
time_signature = [quarter_beats_per_measure, 4]


def measure_time(measure: int):
    return measure * quarter_beats_per_measure * quarter_beats_per_minute


"""
Define root and scale
"""

TONIC_FIT = [60, 72, 'wrap']
TONIC = random.choice(scale(0, 12, 7, fit=[60, 72, 'wrap']))
TONIC_SCALE = pentatonic(TONIC)
TONIC_SOPRANO = multi_operation(TONIC_SCALE, pull_octaves(1))
TONIC_BASS = multi_operation(TONIC_SCALE, pull_octaves(-2))

"""
Define amplitudes
"""

backbone_chord_amp = 0.35
backbone_sequence_amp = 0.55
bass_amp = 0.5
bass_fade_in_amp = 1.0
soprano_amp = 0.6
soprano_fade_in_amp = 1.0
ornament_amp = 0.55

"""
Define instruments
"""

ins = {
    0: AcousticGrandPiano,  # Chord backbone
    1: AcousticGrandPiano,  # Chord backbone
    2: Marimba,  # Chord backbone
    3: Marimba,  # Chord backbone

    4: next(backbone),  # Sequential backbone

    5: next(soprano),  # 4 sopranos
    6: next(soprano),  # 4 sopranos
    7: next(soprano),  # 4 sopranos
    8: next(soprano),  # 4 sopranos
    # 9: next(soprano),  # drum track. don't touch

    10: next(bass),  # 2 bass
    11: next(bass),  # 2 bass

    12: next(ornament),  # 1 ornamental instrument
}

# piano_chord_chan = [0, 1]
# marimba_chord_chan = [2, 3]
# backbone_chan = 4
soprano_channels = [5, 6, 7, 8]
bass_channels = [10, 11]
ornament_channel = 12

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

give_backbone_loop = choose([False, True], [8, 1])


def compose_backbone_loop(start_measure, total_measures):
    # Only use tonic one

    steve_reich_tonic_note = next(steve_reich_notes_random)(
        multi_operation(TONIC_SCALE, pull_octaves(1))
    )
    for i in range(total_measures):
        q.compose([measure_time(start_measure + i),
                   steve_reich(q, keys=steve_reich_tonic_note, quarter_beats=quarter_beats_per_minute,
                               amp=backbone_sequence_amp, channel=4)])


def compose_backbone(start_measure, measure_length):
    num_beats = measure_length * 2 * quarter_beats_per_measure
    q.compose(
        [measure_time(start_measure),
         alter_chords(q, keys_stacked=piano_chord, quarter_beats=quarter_beats_per_minute, amp=backbone_chord_amp,
                      channel=0, num_beats=num_beats)])
    q.compose(
        [measure_time(start_measure),
         alter_chords(q, keys_stacked=piano_chord_rev, quarter_beats=quarter_beats_per_minute, amp=backbone_chord_amp,
                      channel=1, num_beats=num_beats)])
    q.compose(
        [measure_time(start_measure),
         alter_chords(q, keys_stacked=marimba_chord, quarter_beats=quarter_beats_per_minute, amp=backbone_chord_amp,
                      channel=2, num_beats=num_beats)])
    q.compose(
        [measure_time(start_measure),
         alter_chords(q, keys_stacked=marimba_chord_rev, quarter_beats=quarter_beats_per_minute, amp=backbone_chord_amp,
                      channel=3, num_beats=num_beats)])


soprano_pattern_chain = markov({
    'fade': [['fade', 0.75], ['long2', 0.05], ['sr1', 0.1], ['sr2', 0.1]],
    'long2': [['fade', 0.1], ['long2', 0.5], ['sr1', 0.2], ['sr2', 0.2]],
    'sr1': [['fade', 0.1], ['long2', 0.1], ['sr1', 0.4], ['sr2', 0.4]],
    'sr2': [['fade', 0.1], ['long2', 0.1], ['sr1', 0.4], ['sr2', 0.4]],
})


def compose_soprano(start_measure, total_measures, *, gap_range: List[int], channel: int):
    curr = start_measure
    while curr + 10 < start_measure + total_measures:
        pattern = next(soprano_pattern_chain)
        if pattern == 'fade':
            note = random.choice(TONIC_SOPRANO)
            measures = random.choice(range(4, 9))
            num_beats = measures * 6 * 2
            q.compose([
                measure_time(curr),
                fading(q, keys_stacked=[note], quarter_beats=quarter_beats_per_minute, num_beats=num_beats,
                       max_amp=soprano_fade_in_amp, channel=channel)
            ])
            curr += measures
        elif pattern == 'long2':
            i1 = random.choice(range(1, 4))
            i2 = random.choice([1, -1]) + i1
            note1 = TONIC_SOPRANO[i1]
            note2 = TONIC_SOPRANO[i2]
            long2note, long2beats = longing2(note1, note2)
            for _ in range(random.choice(range(3, 6))):
                q.compose([
                    measure_time(curr),
                    longing(q, keys=long2note, key_beats=long2beats, quarter_beats=quarter_beats_per_minute,
                            channel=channel, amp=soprano_amp)
                ])
                curr += 4
        elif pattern == 'sr1':
            note_list_prep = steve_reich_notes_prep(TONIC_SOPRANO, random.choice(range(0, 5)),
                                                    min(TONIC_SOPRANO), min(TONIC_SOPRANO) + 12, 'wrap')
            note_list = steve_reich_notes1(note_list_prep)
            for i in range(random.choice(range(5, 12))):
                q.compose([
                    measure_time(curr),
                    steve_reich(q, keys=note_list, quarter_beats=quarter_beats_per_minute,
                                amp=soprano_amp, channel=channel)
                ])
                curr += 1
        elif pattern == 'sr2':
            note_list_prep = steve_reich_notes_prep(TONIC_SOPRANO, random.choice(range(0, 5)),
                                                    min(TONIC_SOPRANO), min(TONIC_SOPRANO) + 12, 'wrap')
            note_list = steve_reich_notes2(note_list_prep)
            for i in range(random.choice(range(5, 12))):
                q.compose([
                    measure_time(curr),
                    steve_reich(q, keys=note_list, quarter_beats=quarter_beats_per_minute,
                                amp=soprano_amp, channel=channel)
                ])
                curr += 1
        else:
            assert False

        curr += random.choice(gap_range)


def compose_bass(start_measure, total_measures, *, gap_range: List[int], channel: int):
    curr = start_measure
    while curr + 10 < start_measure + total_measures:
        pattern = random.choice(['fade', 'long2'])
        if pattern == 'fade':
            note = random.choice(TONIC_BASS)
            measures = random.choice(range(5, 11))
            num_beats = measures * 6 * 2
            q.compose([
                measure_time(curr),
                fading(q, keys_stacked=[note], quarter_beats=quarter_beats_per_minute, num_beats=num_beats,
                       max_amp=bass_fade_in_amp, channel=channel)
            ])
            curr += measures
        elif pattern == 'long2':
            i1 = random.choice(range(1, 4))
            i2 = random.choice([1, -1]) + i1
            note1 = TONIC_BASS[i1]
            note2 = TONIC_BASS[i2]
            long2note, long2beats = longing2(note1, note2)
            for _ in range(random.choice(range(3, 6))):
                q.compose([
                    measure_time(curr),
                    longing(q, keys=long2note, key_beats=long2beats, quarter_beats=quarter_beats_per_minute,
                            channel=channel, amp=bass_amp)
                ])
                curr += 4
        else:
            assert False

        curr += random.choice(gap_range)


def compose_ornaments(start_measure, total_measures, *, gap_range: List[int]):
    curr = start_measure
    while curr + 10 <= total_measures + start_measure:
        note_pool = set()
        while len(note_pool) != 4:
            note_pool.add(random.choice(TONIC_SCALE))
        long1note, long1beats = longing1(list(note_pool))
        q.compose([measure_time(curr),
                   longing(q, keys=long1note, key_beats=long1beats, quarter_beats=quarter_beats_per_minute,
                           channel=12, amp=ornament_amp)])
        curr += random.choice(gap_range)


# Start Section

start_measures = between(3, 6)
compose_backbone(curr_measure, start_measures)

curr_measure += start_measures

# Middle Parts

middle_measures = between(108, 156)

for soprano_channel in soprano_channels:
    compose_soprano(curr_measure, middle_measures, gap_range=[i for i in range(2, 5)], channel=soprano_channel)

for bass_channel in bass_channels:
    compose_bass(curr_measure, middle_measures, gap_range=[i for i in range(2, 5)], channel=bass_channel)

compose_ornaments(curr_measure, middle_measures, gap_range=[i for i in range(10, 13)])

if give_backbone_loop:
    compose_backbone_loop(curr_measure, middle_measures)

compose_backbone(curr_measure, middle_measures)

curr_measure = middle_measures

# End Section

end_measures = between(3, 6)
compose_backbone(curr_measure, end_measures)

curr_measure += end_measures

"""
Write file
"""

MidiFile(COMP_NAME, [meta_seq, seq]).write()
