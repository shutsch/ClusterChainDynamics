"""
Module for propagating different types of compact objects in simulations.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Dict, Any, Optional, Tuple
from functools import Partial

from ..core import CompactObject, StarCluster, SelfPropellingMolecularCloud


def _get_galpy_potential(potential_type: str) -> Any:
    """
    Retrieve a galpy potential object based on the specified type.
    
    Args:
        potential_type (str): Name of the galpy potential to retrieve
    
    Returns:
        Any: Galpy potential object
    """
    
    try:
        import galpy.potential as galpo
    except ImportError: 
        raise ImportError("If 'potential_func' is provieded as a string, it is assumed to refer to a potential in galpy, but galpy is not installed."
                    "Please install it via 'pip install galpy'. Alternatively, provide a custom potential function.")
    
    potential_map = {
        "MWPotential2014": galpo.MWPotential2014,
        "NFWPotential": galpo.NFWPotential,
        "HernquistPotential": galpo.HernquistPotential,
    }
    
    if potential_type not in potential_map:
        raise ValueError(f"Unknown potential type: {potential_type}. "
                         f"Must be one of {list(potential_map.keys())}")
    
    potential = potential_map[potential_type]()
    
    def potential_callable(pos: np.ndarray) -> Tuple[float, float, float]:
                # Calculate cylindrical radius
        R = np.sqrt(pos[0]**2 + pos[1]**2)

        # Gravitational acceleration from galpy potential
        aR = potential.Rforce(R, pos[2])
        az = potential.zforce(R, pos[2])
        ax = aR * pos[0] / R if R > 0 else 0
        ay = aR * pos[1] / R if R > 0 else 0
        return ax, ay, az
    
    return  potential_callable


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
    initial_position: np.ndarray,
    initial_conditions: Dict[str, Any],
    t_span: Tuple[float, float],
    t_eval: np.ndarray,
    object_type: str,
    potential_func: str | callable
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
    
    if isinstance(potential_func, str):
        potential_func = _get_galpy_potential(potential_func)
    
    compact_object = create_object(object_type, **initial_conditions, initial_position=initial_position)
    
    
    def _propagate(t: float, pos:np.ndarray, _compact_object: CompactObject, _potential: callable) -> CompactObject:
        """
        Propagation function for the numerical integrator.
        
        Args:
            t (float): Current time
            pos (np.ndarray): Current position vector [x, y, z]
            _compact_object (CompactObject): Current object state
            _potential (callable): Galactic potential function
            
        Returns:
            CompactObject: Updated object state
        """
            
        ax, ay, az = _potential(pos[0], pos[1], pos[2])
        # Propagate the object
        _compact_object.propagate(
            dt=t - _compact_object.current_time,
            a_g=np.array([ax, ay, az])
        )
        
        return compact_object.current_position
    
    propagate = Partial(_propagate, _compact_object=compact_object, _potential=potential_func)
    
    sol = solve_ivp(propagate, t_span, y0=initial_position, t_eval=t_eval, rtol=1e-8, atol=1e-10)
    return sol, compact_object
