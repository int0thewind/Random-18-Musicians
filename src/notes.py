from musx.scales import scale
from musx.tools import fit
from typing import List, Tuple, Optional, Literal


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
