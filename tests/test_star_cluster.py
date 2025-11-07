import numpy as np
from ClusterChainDynamics.core import StarCluster, CompactObject


def test_starcluster_basic():
    initial_mass = 100.0
    initial_position = np.array([0.0, 0.0, 0.0])
    initial_velocity = np.array([1.0, 0.0, 0.0])
    mass_loss_rate = 1.0

    cluster = StarCluster(
        initial_mass=initial_mass,
        initial_position=initial_position,
        initial_velocity=initial_velocity,
        mass_loss_rate=mass_loss_rate,
        initial_time=0.0,
    )

    # Inheritance
    assert isinstance(cluster, CompactObject)

    # Feedback force is zero and mass loss rate matches
    force, mdot = cluster.calculate_feedback_force_and_massloss()
    assert np.allclose(force, np.zeros(3))
    assert mdot == mass_loss_rate

    # Propagate one year with zero external acceleration
    cluster.propagate(dt=1.0, a_g=np.zeros(3))

    # Mass should decrease by mass_loss_rate * dt
    assert cluster.current_mass == initial_mass - mass_loss_rate * 1.0

    # Time should increase by dt
    assert cluster.current_time == 1.0

    # Velocity should remain unchanged (no force)
    assert np.allclose(cluster.current_velocity, initial_velocity)

    # Position should advance by velocity * dt (note: CompactObject._update uses velocity*dt)
    assert np.allclose(cluster.current_position, initial_position + initial_velocity * 1.0)
