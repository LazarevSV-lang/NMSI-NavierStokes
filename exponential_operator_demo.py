import numpy as np

def apply_exponential_operator(field, dt, alpha=0.05):
    """
    Exponential operator 'e' for regularization of Navier–Stokes fields.
    
    Parameters
    ----------
    field : np.ndarray
        The input field (velocity, vorticity, or energy density array).
    dt : float
        Time step of the simulation.
    alpha : float
        Damping/regularization coefficient (controls the exponential decay rate).
    
    Returns
    -------
    np.ndarray
        Regularized field after applying the exponential operator.
    """
    return field * np.exp(-alpha * dt)

# --- Demo on synthetic vorticity data ---
if __name__ == "__main__":
    vorticity = np.linspace(-5, 5, 11)
    dt = 0.1
    print("Original vorticity:", vorticity)
    vorticity_reg = apply_exponential_operator(vorticity, dt, alpha=0.1)
    print("Regularized vorticity:", vorticity_reg)
