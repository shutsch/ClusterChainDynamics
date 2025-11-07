"""
Module for propagating different types of compact objects in simulations.
"""

import numpy as np
import galpy.potential as galpo
from scipy.integrate import solve_ivp
from typing import Dict, Any, Optional, Tuple
from functools import Partial

from ..core import CompactObject, StarCluster, SelfPropellingMolecularCloud


def create_object(object_type: str, **kwargs) -> CompactObject:
    """
    Factory function to create different types of compact objects.
    
    Args:
        object_type (str): Type of object to create. Options:
            - "star_cluster": A star cluster with constant mass loss
            - "molecular_cloud": A self-propelling molecular cloud
        **kwargs: Arguments to pass to the object constructor:
            Required for all:
                - initial_mass (float): Initial mass in solar masses
                - initial_position (np.ndarray): Initial position [x, y, z] in parsecs
                - initial_velocity (np.ndarray): Initial velocity [vx, vy, vz] in km/s
                - initial_time (Optional[float]): Initial time in years
            For star_cluster:
                - mass_loss_rate (float): Mass loss rate in M☉/yr
            For molecular_cloud:
                - mass_loss_rate (float): Mass loss rate in M☉/yr
                - feedback_factor (float): Feedback force factor in N/M☉
    
    Returns:
        CompactObject: An instance of the requested object type
    """
    object_types = {
        "star_cluster": StarCluster,
        "molecular_cloud": SelfPropellingMolecularCloud
    }
    
    if object_type not in object_types:
        raise ValueError(f"Unknown object type: {object_type}. "
                        f"Must be one of {list(object_types.keys())}")
    
    ObjectClass = object_types[object_type]
    try:
        return ObjectClass(**kwargs)
    except TypeError as e:
        raise ValueError(f"Missing required parameters for {object_type}: {str(e)}")


def single_object_solve(
    initial_conditions: Dict[str, Any],
    t_span: Tuple[float, float],
    t_eval: np.ndarray,
    object_type: str,
    potential_type: str
) -> Any:
    """
    Propagate a compact object under galactic potential and feedback.
    
    Args:
        initial_conditions (Dict[str, Any]): Initial conditions and parameters for the object
        t_span (Tuple[float, float]): Time interval (t_start, t_end) in years
        t_eval (np.ndarray): Times at which to store the solution
        object_type (str): Type of object to propagate ("star_cluster" or "molecular_cloud")
        potential_type (str): Name of the galpy potential to use
    
    Returns:
        Any: Solution object from solve_ivp integration
    """
    
    potential = getattr(galpo, potential_type)()
    
    
    def _propagate(t: float, state: CompactObject, potential: Any) -> CompactObject:
        """
        Propagation function for the numerical integrator.
        
        Args:
            t (float): Current time
            state (CompactObject): Current object state
            potential (Any): Galactic potential object
            
        Returns:
            CompactObject: Updated object state
        """
        pos = state.current_position
        vel = state.current_velocity
            
        # Calculate cylindrical radius
        R = np.sqrt(pos[0]**2 + pos[1]**2)

        # Gravitational acceleration from galpy potential
        aR = galpo.evaluateRforces(potential, R, pos[2])
        az = galpo.evaluatezforces(potential, R, pos[2])
        ax = aR * pos[0] / R if R > 0 else 0
        ay = aR * pos[1] / R if R > 0 else 0
        
        # Propagate the object
        state.propagate(
            dt=t - state.current_time,
            a_g=np.array([ax, ay, az])
        )
        
        return state
    
    propagate = Partial(_propagate, potential=potential)
    
    sol = solve_ivp(propagate, t_span, t_eval=t_eval, rtol=1e-8, atol=1e-10)
    return sol
