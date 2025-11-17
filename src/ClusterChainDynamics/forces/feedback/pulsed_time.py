import numpy as np


def pulsed_feedback(t:float, pos: np.ndarray, a_0: np.ndarray, t_pulse: np.ndarray, sigma_t: np.ndarray) -> np.ndarray:
    
    
    """ Calculate a pulsed feedback acceleration acting on an object.      
    The pulses are paramaterized by gaussian functions, located at differnt times, with different widths, amplitudes and directions
    Parameters  
    ----------
    t : float
        time
    pos : np.ndarray
        position vector, not used but included for interface consistency.
    a_0 : np.ndarray    
        Acceleration vector at peak of pulse, shape (3, n_pulses)
    t_pulse : np.ndarray
        Timing of pulses, length indicates numner of pulses, same unit as t and sigma_t
    sigma_t: np.ndarray
        width of pulse, same length and units as t and t_pulse
    
    Returns
    ------- 
    np.ndarray
        The feedback acceleration vector.
    """
    
    all_a = a_0  * np.exp(-(t - t_pulse)**2/sigma_t*2)
    return sum(all_a, axis=1)