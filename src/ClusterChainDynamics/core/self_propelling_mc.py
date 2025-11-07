"""
Module containing the SelfPropellingMolecularCloud class, representing a molecular cloud
with mass-dependent self-propulsion feedback.
"""

import numpy as np
from typing import Tuple, Optional
from .compact_object import CompactObject


class SelfPropellingMolecularCloud(CompactObject):
    """
    A class representing a molecular cloud that generates feedback force proportional
    to its mass in its direction of travel.
    
    Attributes:
        initial_mass (float): Initial mass of the molecular cloud in solar masses
        initial_position (np.ndarray): Initial 3D position vector [x, y, z] in parsecs
        initial_velocity (np.ndarray): Initial 3D velocity vector [vx, vy, vz] in km/s
        initial_time (float): Initial time in years
        feedback_factor (float): Proportionality factor for mass-dependent feedback force
        mass_loss_rate (float): Constant mass loss rate in solar masses per year
        current_mass (float): Current mass of the cloud in solar masses
        current_position (np.ndarray): Current 3D position vector [x, y, z] in parsecs
        current_velocity (np.ndarray): Current 3D velocity vector [vx, vy, vz] in km/s
        current_time (float): Current time in years
    """
    
    def __init__(
        self,
        initial_mass: float,
        initial_position: np.ndarray,
        initial_velocity: np.ndarray,
        feedback_factor: float,
        mass_loss_rate: float,
        initial_time: Optional[float] = None
    ):
        """
        Initialize a SelfPropellingMolecularCloud instance.
        
        Args:
            initial_mass (float): Initial mass in solar masses
            initial_position (np.ndarray): Initial position [x, y, z] in parsecs
            initial_velocity (np.ndarray): Initial velocity [vx, vy, vz] in km/s
            feedback_factor (float): Factor determining feedback force strength (N/M_sun)
            mass_loss_rate (float): Constant mass loss rate in solar masses per year
            initial_time (Optional[float]): Initial time in years, defaults to None
        """
        super().__init__(
            initial_mass=initial_mass,
            initial_position=initial_position,
            initial_velocity=initial_velocity,
            initial_time=initial_time
        )
        self.feedback_factor = feedback_factor
        self.mass_loss_rate = mass_loss_rate
    
    def spawn_cloudcluster(self) -> 'CompactObject':
        """
        Molecular clouds cannot spawn new objects in this implementation.
        
        Raises:
            NotImplementedError: This molecular cloud model does not support spawning
        """
        raise NotImplementedError("This molecular cloud model does not support spawning new objects.")
    
    def calculate_feedback_force_and_massloss(self, **kwargs) -> Tuple[np.ndarray, float]:
        """
        Calculate the feedback force and mass loss rate for the molecular cloud.
        The feedback force is proportional to the current mass and acts in the
        direction of travel.
        
        Returns:
            Tuple[np.ndarray, float]:
                - np.ndarray: Feedback force vector (N), proportional to mass and
                  aligned with velocity direction
                - float: Constant mass loss rate in solar masses per year
        """
        # Calculate direction of travel (unit vector)
        velocity_magnitude = np.linalg.norm(self.current_velocity)
        if velocity_magnitude > 0:
            direction = self.current_velocity / velocity_magnitude
        else:
            direction = np.zeros(3)
        
        # Calculate feedback force: mass * factor * direction
        force = self.current_mass * self.feedback_factor * direction
        
        return force, self.mass_loss_rate
    
    def __str__(self) -> str:
        """
        Return a string representation of the molecular cloud.
        
        Returns:
            str: A formatted string showing current properties, feedback factor,
                 and mass loss rate
        """
        base_str = super().__str__()
        # Insert feedback factor and mass loss rate info before the final parenthesis
        return base_str[:-1] + (f", feedback_factor={self.feedback_factor:.2e} N/M☉, "
                               f"mass_loss_rate={self.mass_loss_rate:.2e} M☉/yr)")
