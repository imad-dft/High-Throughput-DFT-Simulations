# K-Point Convergence Study: $Cs_2CuAlI_6$

Before performing the final relaxation, I conducted a convergence test for the Monkhorst-Pack K-point grid to ensure the stability of the Total Energy. My goal was to find the "elbow" point where accuracy meets computational efficiency.

### 📊 Manual Data Collection
I ran several SCF calculations while keeping the energy cutoff constant at 85 Ry. Below is the recorded data:

| K-Point Grid | Total Energy (Ry) | ΔE (Ry) |
| :--- | :--- | :--- |
| 3 x 3 x 3 | -232.5911552900 | -- |
| 4 x 4 x 4 | -232.5910952111 | 0.1297 |
| 5 x 5 x 5 | -232.5909870819 | 0.0054 |
| 6 x 6 x 6 | -232.5909542325 | 0.00003 |

**Observation:** The energy stabilizes significantly at **5x5x5**. The difference between 5x5x5 and 6x6x6 is less than 1 mRy, making **6x6x6** the optimal choice for this high-throughput study.

### 🐍 Python Visualization
I used a custom Python script (using Matplotlib) to visualize the convergence trend. This allows for a clear view of the asymptotic behavior of the total energy.

![K-Point Convergence](./kpoints_convergence.png)

---
*Note: All calculations were performed using the PBE-GGA functional in Quantum ESPRESSO.*
