from typing import Any, Tuple, Callable
import numpy as np

try:
    import galpy.potential as galpo
    has_galpy = True
except ImportError: 
    has_galpy = False


def _get_galpy_potential(potential_type: str) -> Any:
    """
    Retrieve a galpy potential object based on the specified type.
    
    Args:
        potential_type (str): Name of the galpy potential to retrieve
    
    Returns:
        Any: Galpy potential object | None if galpy not installed
    """
    
    if not has_galpy:
        return None
    
    potential_map = {
        "MiyamotoNagai": galpo.MiyamotoNagaiPotential,
        "NFWPotential": galpo.NFWPotential,
        "HernquistPotential": galpo.HernquistPotential,
    }
    
    if potential_type not in potential_map:
        return None
    
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