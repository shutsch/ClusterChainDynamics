import numpy as np

def linear_feedback(t:float, pos: np.ndarray, a_0: np.ndarray, a_1: np.ndarray) -> np.ndarray:
    
    """ Calculate the linear feedback force acting on an object.        
    Parameters  
    ----------
    t : float
        time
    pos : np.ndarray
        position vector, not used but included for interface consistency.
    a_0 : np.ndarray    
        Constant acceleration vector due to feedback (e.g., from stellar winds or supernovae).
    a_1 : np.ndarray
        Linear acceleration coefficient vector due to feedback.
    Returns
    ------- 
    np.ndarray
        The linear feedback force vector.
    """
    
    return a_0 + a_1 * t
    