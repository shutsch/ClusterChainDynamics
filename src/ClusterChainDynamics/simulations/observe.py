from scipy.integrate import OdeSolution
import numpy as np
from typing import Dict, Callable


def observe_single_object(
    solution: OdeSolution,
    observation_times: np.ndarray,
    noise_std: np.ndarray,
    positional_response: Callable = None,
    velocity_response: Callable = None,
) -> Dict[str, np.ndarray]:
    """
    Observe the trajectory and mass evolution of a single compact object
    from the integration solution.
    
    Args:
        solution (OdeResult): The result from the ODE solver containing time points
                              and state vectors.   
    """
    times = solution.t
    positions = solution.y.T  # Transpose to get shape (n_times, n_dimensions)