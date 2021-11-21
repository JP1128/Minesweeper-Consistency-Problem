import numpy as np


def neighbors(r: int, c: int, v: int, h: int):
    """
    :param r:
    :param c:
    :param v:
    :param h:
    :return:
    """
    _top = max(r - 1, 0)
    _lef = max(c - 1, 0)
    _bot = min(r + 1, v - 1) + 1
    _rig = min(c + 1, h - 1) + 1

    row = []
    col = []

    for ri in range(_top, _bot):
        for ci in range(_lef, _rig):
            if ri != r or ci != c:
                row.append(ri)
                col.append(ci)

    return np.array(row), np.array(col)


if __name__ == '__main__':
    field = np.zeros((5, 5))

    # Top left corner
    row, col = neighbors(0, 0, 5, 5)
    print(row, col)
    assert np.array_equal([0, 1, 1], row)
    assert np.array_equal([1, 0, 1], col)

    # Top mid
    row, col = neighbors(0, 2, 5, 5)
    print(row, col)
    assert np.array_equal([0, 0, 1, 1, 1], row)
    assert np.array_equal([1, 3, 1, 2, 3], col)

    # Top right corner
    row, col = neighbors(0, 4, 5, 5)
    print(row, col)
    assert np.array_equal([0, 1, 1], row)
    assert np.array_equal([3, 3, 4], col)

    # Mid left corner
    row, col = neighbors(2, 0, 5, 5)
    print(row, col)
    assert np.array_equal([1, 1, 2, 3, 3], row)
    assert np.array_equal([0, 1, 1, 0, 1], col)

    # Center
    row, col = neighbors(2, 2, 5, 5)
    print(row, col)
    assert np.array_equal([1, 1, 1, 2, 2, 3, 3, 3], row)
    assert np.array_equal([1, 2, 3, 1, 3, 1, 2, 3], col)

    # Mid right corner
    row, col = neighbors(2, 4, 5, 5)
    print(row, col)
    assert np.array_equal([1, 1, 2, 3, 3], row)
    assert np.array_equal([3, 4, 3, 3, 4], col)

    # Bottom left corner
    row, col = neighbors(4, 0, 5, 5)
    print(row, col)
    assert np.array_equal([3, 3, 4], row)
    assert np.array_equal([0, 1, 1], col)

    # Bottom mid
    row, col = neighbors(4, 2, 5, 5)
    print(row, col)
    assert np.array_equal([3, 3, 3, 4, 4], row)
    assert np.array_equal([1, 2, 3, 1, 3], col)

    # Bottom right corner
    row, col = neighbors(4, 4, 5, 5)
    print(row, col)
    assert np.array_equal([3, 3, 4], row)
    assert np.array_equal([3, 4, 3], col)
