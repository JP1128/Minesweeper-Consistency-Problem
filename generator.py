import numpy as np
import math
from minefield import neighbors

RNG = np.random.default_rng()


def create_consistent_field(v: int, h: int, p: float = 0.2):
    _minefield: np.ndarray = np.zeros((v, h), dtype=np.int_)
    _mines: np.ndarray = RNG.choice(np.arange(v * h),
                                    math.floor(v * h * p),
                                    False)

    _minefield.flat[_mines] = -1

    for index, cell in np.ndenumerate(_minefield):
        ri, ci = index
        if cell == 0:
            n = _minefield[neighbors(ri, ci, v, h)]
            n_mines = np.count_nonzero(n == -1)
            _minefield[ri, ci] = n_mines

    return _minefield, _mines


if __name__ == '__main__':
    field, mines = create_consistent_field(30, 16)
    print(field)
