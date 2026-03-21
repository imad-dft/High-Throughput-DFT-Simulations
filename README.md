# High-Throughput DFT Simulations: Lead-Free Perovskites ⚛️☀️

Time-stamped computational lab notebook and database for first-principles calculations of lead-free double perovskite halides.

### 🔬 Project Objective
Simulating a library of halide compounds to identify stable, high-efficiency candidates for next-generation solar energy harvesting, moving away from toxic lead-based materials.

### 📂 Repository Architecture
The database is structured by compound. Each material folder contains:
* **`/Inputs`**: Raw Quantum ESPRESSO `.in` files (SCF, NSCF, Bands, DOS).
* **`/Notebooks`**: LaTeX-compiled daily logs detailing calculation parameters, convergence testing, and physical observations.
* **`/Visuals`**: High-fidelity band structure and optical property plots.

### 🛠️ Computational Methodology
* **Core Engine:** Quantum ESPRESSO 
* **Pseudopotentials:** Norm-Conserving / Ultrasoft (depending on optical vs. electronic requirements)
* **Approximation:** PBE

---
*Maintained as part of ongoing undergraduate physics research. All calculations are logged chronologically to ensure scientific integrity and reproducibility.*
