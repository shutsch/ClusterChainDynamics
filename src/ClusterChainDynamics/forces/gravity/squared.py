import numpy as np


def squared_potential_force(pos: np.ndarray, a_0: np.ndarray):
    """Defines a square potential well force field."""
    a = - a_0 * pos
    return a
