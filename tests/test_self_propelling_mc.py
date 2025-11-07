import numpy as np
from ClusterChainDynamics.core import SelfPropellingMolecularCloud, CompactObject


def test_selfpropelling_mc_basic():
    initial_mass = 100.0
    initial_position = np.array([0.0, 0.0, 0.0])
    initial_velocity = np.array([1.0, 0.0, 0.0])
    feedback_factor = 2.0
    mass_loss_rate = 0.5

    cloud = SelfPropellingMolecularCloud(
        initial_mass=initial_mass,
        initial_position=initial_position,
        initial_velocity=initial_velocity,
        feedback_factor=feedback_factor,
        mass_loss_rate=mass_loss_rate,
        initial_time=0.0,
    )

    # Inheritance
    assert isinstance(cloud, CompactObject)

    # Feedback force should be mass * factor in direction of travel
    force, mdot = cloud.calculate_feedback_force_and_massloss()
    expected_force = np.array([initial_mass * feedback_factor, 0.0, 0.0])
    assert np.allclose(force, expected_force)
    assert mdot == mass_loss_rate

    # Propagate one year with zero external acceleration
    cloud.propagate(dt=1.0, a_g=np.zeros(3))

    # Mass should decrease by mass_loss_rate * dt
    assert np.isclose(cloud.current_mass, initial_mass - mass_loss_rate * 1.0)

    # Velocity should increase because feedback gives acceleration = force / mass
    # a_f = force / initial_mass = feedback_factor * direction
    expected_velocity = initial_velocity + np.array([feedback_factor, 0.0, 0.0]) * 1.0
    assert np.allclose(cloud.current_velocity, expected_velocity)

    # Position update uses the updated velocity in _update: new_position = 0 + expected_velocity * dt
    assert np.allclose(cloud.current_position, expected_velocity * 1.0)

    # Time advanced
    assert cloud.current_time == 1.0
