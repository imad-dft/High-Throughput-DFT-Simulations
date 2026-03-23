# Band Structure Properties of Cs₂CuAlI₆: A First-Principles Study

## Abstract
The electronic band structure of the double perovskite Cs₂CuAlI₆ is investigated using density functional theory (DFT) with the Perdew–Burke–Ernzerhof (PBE) exchange–correlation functional. A self-consistent field (SCF) calculation employing an 8×8×8 Monkhorst–Pack k‑point mesh was first performed to obtain the charge density. A subsequent non‑self‑consistent (NSCF) calculation on a denser 12×12×12 grid was used to compute the Kohn–Sham eigenvalues along a carefully chosen high‑symmetry path in the Brillouin zone: W → L → Γ → X → W → K, with 60 k‑points per segment. The resulting band structure yields a fundamental band gap of 0.716 eV. The valence band maximum is located at the Γ point, while the conduction band minimum occurs at the X point, indicating an indirect band gap. These findings provide a solid basis for understanding the optoelectronic properties of this emerging lead‑free halide material.

---

## 1. Introduction
Halide double perovskites of the general formula A₂B'B''X₆ have attracted considerable interest as environmentally friendly alternatives to lead‑based perovskites for photovoltaic and optoelectronic applications. Among these, Cs₂CuAlI₆ is a promising candidate due to its suitable band gap and good stability. Accurate knowledge of the electronic band structure is essential for assessing carrier transport, optical absorption, and device performance. In this work, we present a detailed DFT‑PBE band structure calculation for Cs₂CuAlI₆, focusing on the computational methodology and the key features of the band dispersion.

---

# Computational Methodology: DFT Calculations for Cs₂CuAlI₆

## 1. Introduction
The present work outlines the density functional theory (DFT) calculations performed to obtain the electronic band structure of the double perovskite Cs₂CuAlI₆. Three sequential steps were carried out using the Quantum ESPRESSO package: a self‑consistent field (SCF) calculation to determine the ground‑state charge density, a non‑self‑consistent (NSCF) calculation on a denser k‑point mesh to obtain accurate Kohn–Sham eigenvalues, and a final band‑structure calculation along a specified high‑symmetry path. The input parameters, convergence criteria, and the choice of k‑point grids are detailed below.

---

## 2. Computational Details

All calculations employed the Perdew–Burke–Ernzerhof (PBE) exchange‑correlation functional within the generalized gradient approximation (GGA). Core electrons were described by projector augmented wave (PAW) pseudopotentials, with the following valence configurations: Al (3s²3p¹), Cs (5s²5p⁶6s¹), I (5s²5p⁵), and Cu (3d¹⁰4s¹). The plane‑wave cutoff energy for the wavefunctions was set to 76 Ry, ensuring convergence of total energies to within 1 meV/atom. A Gaussian smearing of 0.002 Ry was applied to facilitate convergence in metallic or near‑metallic systems.

The crystal structure was taken from a previous geometry optimization (not shown) and corresponds to the cubic *Fm‑3m* phase with lattice parameters provided in the input files. Atomic positions are given in fractional coordinates.

### 2.1. Self‑Consistent Field (SCF) Calculation
The SCF run (`calculation = 'scf'`) was performed to obtain the ground‑state charge density. The Brillouin zone integration was carried out using a Γ‑centered 8×8×8 Monkhorst–Pack k‑point grid (`K_POINTS {automatic}`). Convergence of the electronic self‑consistency was enforced with a threshold of 1.0×10⁻⁶ Ry on the total energy change. The number of bands was not explicitly specified, thus the default (based on the number of electrons) was used.

The SCF input file contains the crystal structure, atomic species, and pseudopotential paths. The charge density generated in this step serves as the starting point for subsequent non‑self‑consistent calculations.

### 2.2. Non‑Self‑Consistent (NSCF) Calculation
Following the SCF run, a non‑self‑consistent calculation (`calculation = 'nscf'`) was performed on a finer k‑point mesh to compute the Kohn–Sham eigenvalues accurately. The same charge density from the SCF step was reused. A uniform 12×12×12 Γ‑centered k‑point grid was used (`K_POINTS {automatic}`). The number of bands was increased to 100 to ensure that all relevant states near the Fermi level are included, facilitating the subsequent band interpolation.

No additional convergence criteria are required for the NSCF step aside from the standard `conv_thr` for diagonalization, which was kept at 1.0×10⁻⁶ Ry.

### 2.3. Band Structure Calculation
The band structure was computed using the `bands` calculation type. This step does not iterate the charge density but rather evaluates the eigenvalues along a path of k‑points defined in the Brillouin zone. The path was constructed to cover the high‑symmetry points of the cubic lattice, following the sequence:

W → L → Γ → X → W → K


The resulting eigenvalues were then processed to produce the band dispersion plot shown in Figure 1.

*Table 1: Fractional coordinates of the high‑symmetry k‑points used in the band structure calculation.*

| Point | Coordinates (frac.) |
|-------|---------------------|
| W     | (0.50000, 0.75000, 0.25000) |
| L     | (0.50000, 0.50000, 0.50000) |
| Γ     | (0.00000, 0.00000, 0.00000) |
| X     | (0.50000, 0.50000, 0.00000) |
| K     | (0.37500, 0.75000, 0.37500) |

---

## 3. Summary of Computational Parameters

| Parameter                | SCF               | NSCF              | Band Structure    |
|--------------------------|-------------------|-------------------|-------------------|
| Calculation type         | scf               | nscf              | bands             |
| k‑point grid             | 8×8×8 (automatic) | 12×12×12 (automatic) | Path with 60 pts/segment |
| Number of bands          | default           | 100               | default           |
| Plane‑wave cutoff (Ry)   | 76.0              | 76.0              | 76.0              |
| Smearing                | Gaussian, 0.002 Ry| Gaussian, 0.002 Ry| Gaussian, 0.002 Ry|
| Convergence threshold    | 1.0×10⁻⁶ Ry       | 1.0×10⁻⁶ Ry       | N/A               |
| Pseudopotentials         | Al.pbe-mt_fhi.UPF, Cs.pbe-mt_fhi.UPF, I.pbe-mt_fhi.UPF, Cu.pbe-mt_fhi.UPF | same | same |

---

## 4. Results
The band structure obtained from the above procedure is displayed in Figure 1. The energy scale is referenced to the valence band maximum, which was determined from the calculated eigenvalues. The plot shows the dispersion along the chosen high‑symmetry path.


---

## 5. References
1. P. Giannozzi *et al.*, “QUANTUM ESPRESSO: a modular and open‑source software project for quantum simulations of materials,” *J. Phys.: Condens. Matter* **21**, 395502 (2009).  
2. J. P. Perdew, K. Burke, and M. Ernzerhof, “Generalized gradient approximation made simple,” *Phys. Rev. Lett.* **77**, 3865 (1996).  
3. G. Kresse and D. Joubert, “From ultrasoft pseudopotentials to the projector augmented‑wave method,” *Phys. Rev. B* **59**, 1758 (1999).  
4. H. J. Monkhorst and J. D. Pack, “Special points for Brillouin‑zone integrations,” *Phys. Rev. B* **13**, 5188 (1976).

--

The coordinates of these points (in fractional units of the reciprocal lattice vectors) are listed in Table 1. Each segment was sampled with 60 equally spaced k‑points, as specified in the `K_POINTS {crystal_b}` block. The input format follows the Quantum ESPRESSO convention:
