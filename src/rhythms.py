from typing import List, Optional, Generator, Any

from musx.generators import cycle
from musx.midi.midinote import MidiNote
from musx.scheduler import Scheduler

from src.tools import flatten, multi_operation


def _channel_check(channel):
    assert 0 <= channel <= 15


def _amp_check(amp):
    assert 0.0 < amp <= 1.0


def _num_beats_check(num_beats):
    assert 0 < num_beats


def _microtone_check(microtone):
    assert 1 <= microtone <= 16


def _quarter_beats_check(q):
    assert 0 < q


def fading(q: Scheduler, /,
           keys_stacked: List[float], quarter_beats: float, num_beats: int, max_amp: float, channel: int, *,
           microtone: int = 1):
    """
    A gradual fade in-out note/chord composer
    """
    _channel_check(channel)
    _amp_check(max_amp)
    _num_beats_check(num_beats)
    _microtone_check(microtone)
    _quarter_beats_check(quarter_beats)

    duration = quarter_beats / 2
    amp_inc = max_amp / (num_beats / 2)
    curr_amp = 0.0

    for i in range(num_beats):
        for key in keys_stacked:
            note = MidiNote(time=q.now, dur=duration, key=key, chan=channel, tuning=microtone, amp=curr_amp)
            q.out.addevent(note)
        yield duration
        curr_amp += amp_inc if i < num_beats / 2 else -amp_inc

    return


def steve_reich(q: Scheduler, /,
                keys: List[Optional[float]], quarter_beats: float, amp: float, channel: int, *,
                microtone: int = 1):
    """
    The iconic Steve-Reich repetitive sequence composer
    """
    _channel_check(channel)
    _amp_check(amp)
    _quarter_beats_check(quarter_beats)

    duration = quarter_beats / 2

    for key in keys:
        if key is not None:
            note = MidiNote(time=q.now, dur=duration, key=key, chan=channel, tuning=microtone, amp=amp)
            q.out.addevent(note)
        yield duration

    return


def alter_chords(q: Scheduler, /,
                 keys_stacked: List[Optional[List[float]]], quarter_beats: float, amp: float, channel: int, *,
                 microtone: int = 1, num_beats: int = 2, ossia: bool = False):
    """
    Alternating chordal generators
    """
    _channel_check(channel)
    _amp_check(amp)
    _num_beats_check(num_beats)
    _microtone_check(microtone)
    _quarter_beats_check(quarter_beats)
    assert len(keys_stacked) <= num_beats

    if ossia:
        keys_stacked[0] = flatten(keys_stacked)
        keys_stacked[1:] = [None] * (len(keys_stacked) - 1)

    keys_stacked_gen: Generator[Optional[List[float]], Any, None] = cycle(keys_stacked, stop=num_beats)
    duration = quarter_beats / 2

    for i in range(num_beats):
        keys = next(keys_stacked_gen)
        if keys is not None:
            for key in keys:
                note_amp = amp if i % len(keys_stacked) == 0 else amp - 0.1
                note = MidiNote(time=q.now, dur=duration, key=key, chan=channel, tuning=microtone, amp=note_amp)
                q.out.addevent(note)
        yield duration


def longing(q: Scheduler, /,
            keys: List[float], key_beats: List[float], quarter_beats: float, amp, channel: int, *,
            microtone: int = 1):
    _channel_check(channel)
    _amp_check(amp)
    _microtone_check(microtone)
    _quarter_beats_check(quarter_beats)
    assert len(keys) == len(key_beats)

    durations = multi_operation(key_beats, lambda x: x * quarter_beats)

    for key, dur in zip(keys, durations):
        if key is not None:
            note = MidiNote(time=q.now, dur=dur, key=key, chan=channel, tuning=microtone, amp=amp)
            q.out.addevent(note)
        yield dur

    return
