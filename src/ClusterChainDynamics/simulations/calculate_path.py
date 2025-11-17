"""
Module for propagating different types of compact objects in simulations.
"""

import numpy as np
from scipy.integrate import solve_ivp, OdeSolution
from typing import Dict, Any, Optional, Tuple, Callable
from functools import partial

from ..forces import feedback, gravity
from ..forces.gravity.galpy_wrapper import _get_galpy_potential

        
def propagate(t: float, pos_and_vel: np.ndarray, calculate_a_g: np.ndarray | Callable[[np.ndarray,], np.ndarray], calculate_a_f: np.ndarray | Callable[[float, np.ndarray,], np.ndarray],) -> np.ndarray: 
    """
    Propagate the compact object forward in time, accounting for gravitational
    and feedback forces.

    Args:
        t (float): Time
        a_g (np.ndarray): Gravitational acceleration vector 

    This method:
    1. Calculates feedback forces and mass loss
    2. Combines gravitational and feedback accelerations
    3. Updates the object's state using _update()
    """
    pos = pos_and_vel[0:3]
    vel = pos_and_vel[3:6]
    
    # Calculate feedback acceleration
    a_f = calculate_a_f(t, pos)
    
    # Calculate gravitational acceleration
    a_g = calculate_a_g(pos)

    # Combine all accelerations
    a = a_g + a_f
    
    return np.concatenate((vel, a))
    

def single_object_solve(
    initial_position: np.ndarray,
    initial_velocity: np.ndarray,
    t_span: Tuple[float, float],
    t_eval: np.ndarray,
    feedback_func: str | Callable[[float, np.ndarray], Tuple[float, float, float]],
    potential_func: str | Callable[[np.ndarray], Tuple[float, float, float]],
    feedback_params: Dict,
    potential_params: Dict = None, # Not needed for galpy potentials
) -> OdeSolution:
    """
    Propagate a compact object under galactic potential and feedback.
    
    Args:
        initial_conditions (Dict[str, Any]): Initial conditions and parameters for the object
        t_span (Tuple[float, float]): Time interval (t_start, t_end) in years
        t_eval (np.ndarray): Times at which to store the solution
        object_type (str): Type of object to propagate ("star_cluster" or "molecular_cloud")
        potential (str): Name of the potential to use, can be a galpy potential
    
    Returns:
        Any: Solution object from solve_ivp integration
    """
    
    if isinstance(potential_func, str):
        _potential_func = _get_galpy_potential(potential_func)
        
        if _potential_func is None:
            try: 
                potential_func = getattr(gravity, potential_func) 
            except ImportError:
                raise ImportError(f"single_object_solve: potential provided ('{potential_func}') not in galpy or this libary")
            
            if potential_params is not None:
                potential_func = partial(potential_func, potential_params)
        else:
            potential_func = _potential_func
            
    
    if isinstance(feedback_func, str):
        try: 
            feedback_func = getattr(feedback, feedback_func) 
        except ImportError:
            raise ImportError(f"single_object_solve: feedback model provided ('{feedback_func}') not part of this library")
        
        feedback_func = partial(feedback_func, feedback_params)

    
    
    _propagate = partial(propagate, calculate_a_f=feedback_func, calculate_a_g=potential_func)
    
    return solve_ivp(_propagate, t_span, y0=np.concatenate([initial_position, initial_velocity]), t_eval=t_eval, rtol=1e-8, atol=1e-10)

