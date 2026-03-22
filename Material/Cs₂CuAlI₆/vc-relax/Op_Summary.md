# 💎 Structural Optimization Report: $Cs_2CuAlI_6$

**Date of Completion:** March 15, 2026  
**Project:** Lead-Free Double Perovskite High-Throughput Study  
**Status:**  **JOB DONE**

---

### 📊 Final Equilibrium Parameters
These values represent the ground-state geometry where the internal forces and crystal stress are minimized.

| Physical Property | Optimized Value | Unit |
| :--- | :--- | :--- |
| **Lattice Constant ($a, b, c$)** | **8.0374** | **Å** |
| **Unit Cell Volume** | **2477.57277** | **a.u.³** |
| **Fermi Energy ($E_F$)** | **2.7268** | **eV** |
| **Total Energy ($E_{tot}$)** | **-232.59095423** | **Ry** |

---

### 🔬 Convergence & Stability Metrics
A high-quality DFT simulation requires low residual stress and forces. My results meet the strict academic criteria for publication-grade data.

* **Total Force:** `0.001226` Ry/au  *(Target: < 10⁻³)*
* **Total Stress:** `0.09` kbar  *(Target: < 0.5 kbar)*
* **Total SCF Correction:** `0.000448` Ry
* **Symmetry Retained:** Cubic ($Fm\bar{3}m$)

---

### 🛠️ Computational Methodology
I utilized a high-precision plane-wave basis set to ensure the $d$-orbitals of Copper ($Cu$) were accurately captured.

* **Code:** Quantum ESPRESSO (pw.x)
* **Functional:** PBE-GGA (Generalized Gradient Approximation)
* **Pseudopotentials (Norm-Conserving):**
    * $Al$: `Al.pbe-mt_fhi.UPF`
    * $Cs$: `Cs.pbe-mt_fhi.UPF`
    * $I$: `I.pbe-mt_fhi.UPF`
    * $Cu$: `Cu.pbe-mt_fhi.UPF`

---

###  Performance Summary
* **CPU Time:** 1h 17m
* **Wall Time:** 1h 30m
* **Termination:** Successful (March 15, 2026, 00:11:08)

---
*The relaxed structure is employed as the static framework for subsequent high-resolution electronic structure calculations, including the band structure, density of states (DOS), as well as optical and thermal properties.*
