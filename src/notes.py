import random

from musx.scales import scale
from musx.generators import choose
from musx.tools import fit
from typing import List, Tuple, Optional, Literal

from src.tools import rotate


def pentatonic(root: int, *, fit_option=None) -> List[int]:
    return scale(root, 5, 2, 2, 3, 2, fit_option)


def pentatonic_backbone_chord(root: int, *, convolution: int = 1) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Return the backbone chord note, first one for piano and second one for marimba
    """
    # TODO implement convolution
    root = fit(root, 48, 60, 'wrap')
    piano_chord = [[root, root + 7, root + 12], [root + 14, root + 19, root + 24]]
    marimba_chord = [[root + 12], [root + 19, root + 24]]
    return piano_chord, marimba_chord


def longing1(notes: List[float]) -> Tuple[List[float], List[int]]:
    assert len(notes) >= 4
    i = random.choice(range(3, len(notes)))
    return [notes[i], notes[i - 1], notes[i - 2], notes[i - 1], notes[i - 3]], [2, 4, 2, 4, 6]


def longing2(note1: float, note2: float) -> Tuple[List[float], List[int]]:
    return [note1, note2, note1, note2, note1, note2, note1, note2], [4, 2, 3, 3, 4, 2, 2, 4]


def steve_reich_notes_prep(notes: List[float], rotation: int, fit_lb, fit_ub, fit_mode) -> List[float]:
    rotated_notes = rotate(notes, rotation)
    ret: List[float] = []
    for n in rotated_notes:
        ret.append(fit(n, fit_lb, fit_ub, fit_mode))
    return ret


def steve_reich_notes1(notes: List[float]) -> List[Optional[float]]:
    assert len(notes) >= 5
    notes.sort()
    note1, note2, note3, note4, note5 = tuple(notes)
    return [note1, note5, note3, None, note4, note2, None, note5, None, note3, note4, None]


def steve_reich_notes2(notes: List[float]) -> List[Optional[float]]:
    assert len(notes) >= 5
    notes.sort()
    note1, note2, note3, note4, note5 = tuple(notes)
    return [note1, None, note5, note4, note2, None, note5, note3, None, note5, note4, None]


steve_reich_notes_random = choose([steve_reich_notes1, steve_reich_notes2])
