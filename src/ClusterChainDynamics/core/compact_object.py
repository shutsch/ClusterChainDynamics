"""
Module containing the abstract compact object class for representing and propagating star clusters and / or molecular clouds.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Tuple, List, Optional


@dataclass
class CompactObject:
    """
    A abstract class representing a star cluster and / or molecular cloud with physical properties.
    
    Attributes:
        initial_mass (float): Initial mass of the cluster chain in solar masses
        initial_position (np.ndarray): Initial 3D position vector [x, y, z] in parsecs
        initial_velocity (np.ndarray): Initial 3D velocity vector [vx, vy, vz] in km/s
        initial_time (float): Initial time in years
        current_mass (float): Current mass of the cluster chain in solar masses
        current_position (np.ndarray): Current 3D position vector [x, y, z] in parsecs
        current_velocity (np.ndarray): Current 3D velocity vector [vx, vy, vz] in km/s
        current_time (float): Current time in years
    """
    initial_mass: float
    initial_position: np.ndarray
    initial_velocity: np.ndarray
    initial_time: Optional[float] = None
    current_mass: float = field(init=False)
    current_position: np.ndarray = field(init=False)
    current_velocity: np.ndarray = field(init=False)
    current_time: float = field(init=False)

    
    def __post_init__(self):
        """Initialize current properties from initial values."""
        self.initial_position = np.asarray(self.initial_position, dtype=np.float64)
        self.initial_velocity = np.asarray(self.initial_velocity, dtype=np.float64)
        self.current_mass = self.initial_mass
        self.current_position = self.initial_position.copy()
        self.current_velocity = self.initial_velocity.copy()
        self.current_time = self.initial_time if self.initial_time is not None else 0.0
        
    def spawn_new(self) -> 'CompactObject':
        """
        Create a new CompactObject instance from the current object.
        This method should be implemented by concrete subclasses to define
        how new objects are spawned from existing ones.
        
        Returns:
            CompactObject: A new instance of a CompactObject subclass
            
        Raises:
            NotImplementedError: This is an abstract method that must be implemented by subclasses
        """
        raise NotImplementedError("Spawn method is not implemented in this abstract class.")

    def get_age(self) -> float:
        """Get the age of the cluster chain in years."""
        return self.current_time - (self.initial_time if self.initial_time is not None else 0.0)
    
    def calculate_feedback_force_and_massloss(self, **kwargs) -> Tuple[np.ndarray, float]:
        """
        Calculate the feedback force and mass loss rate for the compact object.
        This method should be implemented by concrete subclasses to define
        the specific physics of feedback and mass loss.

        Args:
            **kwargs: Additional keyword arguments that may be needed by specific implementations

        Returns:
            Tuple[np.ndarray, float]: A tuple containing:
                - np.ndarray: 3D force vector in N representing the feedback force
                - float: Mass loss rate in solar masses per year
        
        Raises:
            NotImplementedError: This is an abstract method that must be implemented by subclasses
        """
        raise NotImplementedError("Feedback force calculation is not implemented yet.")
    
    
    def _update(self, dt: float, dm: float, acceleration: np.ndarray):
        """
        Update the current state of the compact object based on physical changes.
        This is an internal method used by propagate() to apply the calculated changes.

        Args:
            dt (float): Time step in years
            dm (float): Mass loss in solar masses
            acceleration (np.ndarray): Total acceleration vector in km/s/yr
        
        Note:
            This method ensures mass remains non-negative and updates all current
            properties (position, velocity, mass, time) consistently.
        """
        self.current_velocity += acceleration * dt
        self.current_position += self.current_velocity * dt
        
        self.current_mass -= dm
        if self.current_mass < 0:
            self.current_mass = 0.0
            
        self.current_time += dt
    

        
        
    

    def propagate(self, dt: float, a_g: np.ndarray):
        """
        Propagate the compact object forward in time, accounting for gravitational
        and feedback forces.

        Args:
            dt (float): Time step in years
            a_g (np.ndarray): Gravitational acceleration vector in km/s/yr

        This method:
        1. Calculates feedback forces and mass loss
        2. Combines gravitational and feedback accelerations
        3. Updates the object's state using _update()
        """
        # Calculate feedback forces and mass loss rate
        f_f, mdot = self.calculate_feedback_force_and_massloss()
        
        # Convert feedback force to acceleration
        a_f = f_f / self.current_mass

        # Combine all accelerations
        a = a_g + a_f
        
        # Update the object's state
        self._update(dt=dt, dm=mdot * dt, acceleration=a)



    
    def __str__(self) -> str:
        """Return a string representation of the cluster chain."""
        return (f"ClusterChain(current_mass={self.current_mass:.2f} M☉, "
                f"current_position=[{', '.join(f'{x:.2f}' for x in self.current_position)}] pc, "
                f"current_velocity=[{', '.join(f'{v:.2f}' for v in self.current_velocity)}] km/s, "
                f"current_time={self.current_time:.2f} yr)")