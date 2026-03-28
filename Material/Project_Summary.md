# Systematic DFT Screening of Al‑Based Double Perovskites: A‑Site, B‑Site, and X‑Site Engineering

## Project Summary
This investigation presents a high‑throughput density functional theory (DFT) screening campaign exploring a series of double‑perovskite materials with the general formula **A₂B(Al)X₆**, where aluminum is incorporated as a fixed B‑site cation in the ordered double‑perovskite structure. The systematic series encompasses three independent compositional dimensions:  
- **A‑site engineering** (Cs⁺, MA⁺, FA⁺)  
- **B‑site host lattice variation** (Pb²⁺, Sn²⁺, Ge²⁺)  
- **X‑site halide tuning** (I⁻, Br⁻, Cl⁻)  

Using first‑principles calculations within Quantum ESPRESSO (PBE functional, FHI pseudopotentials), we perform full structural relaxation, electronic structure calculation, and comparative analysis to evaluate the photovoltaic potential of each composition. This repository contains all input files, automation scripts, and raw data required to reproduce the entire screening workflow.

---

## 1. Research Framework & Compositional Series

The experimental design follows a systematic substitution strategy where the double‑perovskite structure accommodates aluminum (Al³⁺) as one of the two B‑site cations, creating a well‑defined octahedral framework across three independent compositional families. Each composition corresponds to the ordered double‑perovskite stoichiometry with a fixed 1:1 B‑site ratio (B:Al).

### 1.1. Compositional Series Overview

| Series | Fixed Component | Variable Component | Rationale |
|:-------|:----------------|:-------------------|:----------|
| **Series A** | B = Pb, X = I, Al‑fixed | A = Cs, MA, FA | Investigate A‑cation size effects on lattice distortion and band gap |
| **Series B** | A = Cs, X = I, Al‑fixed | B = Pb, Sn, Ge | Probe B‑site electronic structure influence on carrier transport |
| **Series C** | A = Cs, B = Pb, Al‑fixed | X = I, Br, Cl | Examine halide electronegativity effect on band edge positions |

### 1.2. General Formula
```math
\text{A}_2\text{B}(\text{Al})\text{X}_6
