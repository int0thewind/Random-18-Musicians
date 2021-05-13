from musx.scales import scale
from typing import List, Tuple


def pentatonic(root: int) -> List[int]:
    return scale(root, 5, 2, 2, 3, 2)


def pentatonic_backbone_chord(root: int, transpose) -> Tuple[List[int]]:
    pent_scale = pentatonic(root)
    pass