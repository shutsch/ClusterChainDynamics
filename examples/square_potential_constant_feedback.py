import numpy as np
from ClusterChainDynamics import single_object_solve, plot_coord_vs_vel_2D


def main(): 

    initial_position = np.array([0.0, 0.0, 1.0])
    initial_velocity = np.array([0.0, 0.0, 0.0])
    

    # Propagate the object for a certain time
    sol = single_object_solve(
        t_span=(0.,10.0),
        t_eval=np.linspace(0,10.0,100),
        initial_position=initial_position,
        initial_velocity=initial_velocity,
        potential_func="squared_potential_force",
        feedback_func="constant_feedback",
        feedback_params=dict(a_0=-np.array([0., 0., 1.])),
        potential_params=dict(a_0=np.array([0., 0., 1.]))
    )
  
    velocities = sol.y[3:]
    positions = sol.y[:3]
    # Plot x-coordinate vs x-velocity
    plot_coord_vs_vel_2D(
        positions=positions.T,
        velocities= velocities.T,
        time=sol.t,
        index=2,
        name="squared_constant",
        path="./",
        title="Z Position vs Z Velocity",
        xlabel="Z Position",
        ylabel="Z Velocity"
    )
    
if __name__ == "__main__":
    main()