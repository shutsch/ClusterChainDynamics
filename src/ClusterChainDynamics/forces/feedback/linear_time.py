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
    
    
def linear_feedback_no_sign_flip(t:float, pos: np.ndarray, a_0: np.ndarray, a_1: np.ndarray) -> np.ndarray:
    
    """ Calculate the linear feedback force acting on an object, returning 0 in case of full  decellaration instead of a sign flip.      
    If both a0 and a1 have the same sign, this will never happen, and the function `linear_feedback' should be used as it is cheaper. 
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
    
    a = a_0 + a_1 * t
    
    return a if np.sign(a) == np.sign(a_0) else 0.
    