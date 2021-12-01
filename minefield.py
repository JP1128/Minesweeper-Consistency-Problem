from typing import List, Tuple


def neighbors(r: int, c: int, v: int, h: int) -> List[Tuple[int, int]]:
    """
    Minefield utility function. Given the coordinate (r, c)
    and the shape of the field (v, h), return the coordinates
    of neighboring squares. Two numpy arrays are returned such
    that the first array [a_0, a_1, ..., a_n] and the second
    array [b_0, b_1, ..., b_n] form n coordinates (a_0, b_0),
    (a_1, b_1), ..., (a_n, b_n).

    :param r: row offset
    :param c: column offset
    :param v: vertical height
    :param h: horizontal width
    :return: array of row and array of columnss
    """
    _top = max(r - 1, 0)
    _lef = max(c - 1, 0)
    _bot = min(r + 1, v - 1) + 1
    _rig = min(c + 1, h - 1) + 1

    return [(ri, ci)
            for ri in range(_top, _bot)
            for ci in range(_lef, _rig)
            if ri != r or ci != c]
