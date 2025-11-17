import numpy as np

def constant_feedback(t:float, pos: np.ndarray, a_0: np.ndarray) -> np.ndarray:
    """
    Calculate the constant feedback force acting on an object.

    Parameters
    ----------
    t : float
        time, not used in this function but included for interface consistency.
    pos : np.ndarray
        position vector, not used in this function but included for interface consistency.
    a_0 : np.ndarray
        Constant acceleration vector due to feedback (e.g., from stellar winds or supernovae).

    Returns
    -------
    np.ndarray
        The constant feedback force vector.
    """
    return a_0