"""
Module containing the StarCluster class, representing a cluster of stars with simplified dynamics.
"""

import numpy as np
from typing import Tuple, Optional
from .compact_object import CompactObject


class StarCluster(CompactObject):
    """
    A class representing a star cluster with simplified dynamics.
    Inherits from CompactObject and implements specific star cluster behavior.
    
    Attributes:
        initial_mass (float): Initial mass of the star cluster in solar masses
        initial_position (np.ndarray): Initial 3D position vector [x, y, z] in parsecs
        initial_velocity (np.ndarray): Initial 3D velocity vector [vx, vy, vz] in km/s
        initial_time (float): Initial time in years
        mass_loss_rate (float): Constant mass loss rate in solar masses per year
        current_mass (float): Current mass of the cluster in solar masses
        current_position (np.ndarray): Current 3D position vector [x, y, z] in parsecs
        current_velocity (np.ndarray): Current 3D velocity vector [vx, vy, vz] in km/s
        current_time (float): Current time in years
    """
    
    def __init__(
        self,
        initial_mass: float,
        initial_position: np.ndarray,
        initial_velocity: np.ndarray,
        mass_loss_rate: float,
        initial_time: Optional[float] = None
    ):
        """
        Initialize a StarCluster instance.
        
        Args:
            initial_mass (float): Initial mass in solar masses
            initial_position (np.ndarray): Initial position [x, y, z] in parsecs
            initial_velocity (np.ndarray): Initial velocity [vx, vy, vz] in km/s
            mass_loss_rate (float): Constant mass loss rate in solar masses per year
            initial_time (Optional[float]): Initial time in years, defaults to None
        """
        super().__init__(
            initial_mass=initial_mass,
            initial_position=initial_position,
            initial_velocity=initial_velocity,
            initial_time=initial_time
        )
        self.mass_loss_rate = mass_loss_rate
    
    def spawn_cloudcluster(self) -> 'CompactObject':
        """
        Star clusters cannot spawn new clusters in this implementation.
        
        Raises:
            NotImplementedError: Star clusters do not support spawning new clusters
        """
        raise NotImplementedError("Star clusters cannot spawn new clusters in this implementation.")
    
    def calculate_feedback_force_and_massloss(self, **kwargs) -> Tuple[np.ndarray, float]:
        """
        Calculate the feedback force and mass loss rate for the star cluster.
        For this simplified implementation, there is no feedback force and
        mass loss rate is constant.
        
        Returns:
            Tuple[np.ndarray, float]:
                - np.ndarray: Zero force vector (no feedback)
                - float: Constant mass loss rate in solar masses per year
        """
        # No feedback force (zero vector)
        force = np.zeros(3)
        
        # Return constant mass loss rate
        return force, self.mass_loss_rate
    
    def __str__(self) -> str:
        """
        Return a string representation of the star cluster.
        
        Returns:
            str: A formatted string showing current properties and mass loss rate
        """
        base_str = super().__str__()
        # Insert mass loss rate info before the final parenthesis
        return base_str[:-1] + f", mass_loss_rate={self.mass_loss_rate:.2e} M☉/yr)"
