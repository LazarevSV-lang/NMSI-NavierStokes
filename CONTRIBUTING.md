# 🤝 Contributing to NMSI–π*–HDQG Simulations

We invite colleagues to collaborate by providing **PINN-discovered unstable profiles** for hybrid testing under the  
**Classical Navier–Stokes vs NMSI–π*–HDQG augmented framework**.

Initial runs will be performed at **64³ (ν≈5e-4)** for quick validation, followed by **128³** for turbulence spectra and Lyapunov analysis.

---

## 📌 Minimal Data Format (NPZ/HDF5)

Please submit your profile in one of the following formats:

- **Real space (preferred):**
  - `u`: velocity field, shape **(3, nx, ny, nz)**
  - `L`: box lengths, e.g. `[2π, 2π, 2π]`
  - `meta` (optional):  
    ```json
    {
      "nu": 5e-4,
      "grid": [nx, ny, nz],
      "normalized_E": ...,
      "notes": "PINN profile XYZ"
    }
    ```

- **Fourier space (optional):**
  - `uhat`: velocity Fourier coefficients
  - `KX, KY, KZ`: matching wavenumber grids

---

## 🔬 Export Script (PyTorch/NumPy → NPZ)

Here is a minimal script to export a PINN profile into NPZ format:

```python
import torch, numpy as np

# Example: load/generate PINN output
# u_pt must have shape [3, nx, ny, nz] (channels-first)
with torch.no_grad():
    nx = ny = nz = 64
    u_pt = torch.zeros(3, nx, ny, nz)
    # ... fill u_pt with your predicted velocity field ...

# Convert to NumPy
u = u_pt.detach().cpu().numpy()

# Domain (periodic 2π box by default)
L = np.array([2*np.pi, 2*np.pi, 2*np.pi], dtype=np.float64)

# Optional metadata
meta = {
    "nu": 5e-4,
    "grid": [u.shape[1], u.shape[2], u.shape[3]],
    "normalized_E": None,
    "notes": "Example PINN profile export"
}

# Save NPZ
np.savez("IC_pinn_profile.npz", u=u, L=L, meta=np.array(meta, dtype=object))
```

---

## 📤 How to Contribute

1. Fork this repository.  
2. Add your `IC_pinn_profile.npz` (or HDF5) under a new folder `profiles/YourName_ProfileName/`.  
3. Create a Pull Request with a short description.  

---

## 📣 Acknowledgment

All contributors of profiles will be **credited in plots and in the README of results PRs**.

---

🔗 **Repository link:**  
[https://github.com/LazarevSV-lang/NMSI-NavierStokes](https://github.com/LazarevSV-lang/NMSI-NavierStokes)
