from collections import defaultdict
from enum import Enum, unique, auto
from typing import List, Set, Dict

import numpy as np

from minefield import neighbors


@unique
class Instate(Enum):
    a0 = 0
    a1 = 1
    a2 = 2
    a3 = 3
    a4 = 4
    a5 = 5
    a6 = 6
    a7 = 7
    a8 = 8
    MINE = auto()


@unique
class Exstate(Enum):
    COVERED = auto()
    FLAGGED = auto()
    REVEALED = auto()


_0 = Instate.a0
_1 = Instate.a1
_2 = Instate.a2
_3 = Instate.a3
_4 = Instate.a4
_5 = Instate.a5
_6 = Instate.a6
_7 = Instate.a7
_8 = Instate.a8

MINE = Instate.MINE

COVERED = Exstate.COVERED
FLAGGED = Exstate.FLAGGED
REVEALED = Exstate.REVEALED


class Square:
    def __init__(self):
        self.instate: Instate = _0
        self.exstate: Exstate = COVERED

    def has_mine(self) -> bool:
        return self.instate is MINE

    def increment(self) -> None:
        if not self.has_mine():
            self.instate = Instate(self.instate.value + 1)

    def __repr__(self) -> str:
        left, right = {
            COVERED: ('[', ']'),
            FLAGGED: ('<', '>'),
            REVEALED: (' ', ' '),
        }[self.exstate]

        instate = self.instate
        if instate is MINE:
            instate = '*'
        elif instate is _0:
            instate = ' '
        else:
            instate = instate.value

        return f'{left}{instate}{right}'


class Minesweeper:
    def __init__(self, v: int, h: int, m: int, seed: int = None):
        self.v: int = v
        self.h: int = h

        self.field: List[List[Square]] = [
            [Square() for _ in range(h)]
            for _ in range(v)
        ]

        self.neighbors: Dict[Square, List[Square]] = {
            self.field[r][c]: [self.field[ri][ci]
                               for ri, ci in neighbors(r, c, v, h)]
            for r in range(v)
            for c in range(h)
        }

        # Generate random mines
        rng = np.random.default_rng(seed)
        flat = rng.choice(np.arange(v * h), m, False)
        xs, ys = np.unravel_index(flat, (v, h))
        mines = list(zip(xs.tolist(), ys.tolist()))

        for r, c in mines:
            square = self.field[r][c]
            square.instate = MINE
            for neighbor in self.neighbors[square]:
                neighbor.increment()

        self.map: Dict[Instate, Set[Square]] = defaultdict(set)
        for row in self.field:
            for square in row:
                self.map[square.instate].add(square)

        self.frontier: Set[Square] = set()

    def reveal(self, r: int, c: int) -> bool:
        square = self.field[r][c]
        self._reveal(square)
        return not square.has_mine()

    def count(self, exstate: Exstate):
        c = 0
        for row in self.field:
            for square in row:
                if square.exstate is exstate:
                    c += 1
        return c

    def _reveal(self, square: Square):
        # Already revealed, do nothing
        if square.exstate is REVEALED:
            return

        square.exstate = REVEALED
        self.frontier.discard(square)

        if square.instate is _0:
            for neighbor in self.neighbors[square]:
                self._reveal(neighbor)
        else:
            for neighbor in self.neighbors[square]:
                if neighbor.exstate is not REVEALED:
                    self.frontier.add(neighbor)

    def __repr__(self):
        s = ''
        for row in self.field:
            for square in row:
                s += repr(square)
            s += '\n'
        return s[:-1]


def main():
    m = Minesweeper(25, 25, 100, 1)
    print(m)


if __name__ == '__main__':
    main()
