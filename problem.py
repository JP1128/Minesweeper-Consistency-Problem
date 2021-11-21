import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.callback import Callback
from pymoo.core.problem import ElementwiseProblem
from pymoo.factory import get_sampling, get_mutation, get_crossover
from pymoo.optimize import minimize

from generator import create_consistent_field
from minefield import neighbors


class MCP(ElementwiseProblem):
    def __init__(self, field: np.ndarray, mines: np.ndarray) -> None:
        assert field.ndim == 2
        assert mines.ndim == 1

        super().__init__(
            n_var=len(mines),
            xl=0, xu=1,
            type_var=int
        )

        self.field: np.ndarray = field
        self.v: int  # vertical height
        self.h: int  # horizontal width
        self.v, self.h = self.field.shape

        self.mines: np.ndarray = mines

        self.mask: np.ndarray  # squares that are not mines
        self.mask = np.ones((self.v, self.h), dtype=bool)
        self.mask.flat[self.mines] = False

    def _calc_pareto_front(self):
        return 0

    def _evaluate(self, x, out, *args, **kwargs):
        field: np.ndarray = self.field.copy()
        for r, c in np.c_[np.unravel_index(self.mines[x], self.field.shape)]:
            nc = neighbors(r, c, self.v, self.h)
            field[nc] -= 1

        out['F'] = np.sum(np.square(field[self.mask]))


class CustomCallback(Callback):
    def __init__(self) -> None:
        super().__init__()
        self.data['best'] = []


if __name__ == '__main__':
    # Problem
    field, mines = create_consistent_field(30, 16)
    problem = MCP(field, mines)

    algorithm = GA(
        pop_size=200,
        sampling=get_sampling('bin_random'),
        crossover=get_crossover("bin_hux"),
        mutation=get_mutation("bin_bitflip"),
        # save_history=True,
        eliminate_duplicates=True
    )

    res = minimize(problem,
                   algorithm,
                   ('n_gen', 30),
                   callback=CustomCallback(),
                   verbose=True)

    print("best individual: ", res.X)
    print("best fitness: ", res.F)
