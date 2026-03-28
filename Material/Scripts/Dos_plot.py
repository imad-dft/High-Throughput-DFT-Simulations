import os
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.ticker as ticker

# ================= USER CONFIGURATION =================
# Set these for your specific run
COMPOUND_NAME_PLAIN = "Rb2NaInBr6"
COMPOUND_NAME_LATEX = r"Rb$_2$NaInBr$_6$"     # The latex style name used for the plot naming . 
FERMI_E = 3.5950      # Fermi energy from the SCF , NSCF or BANDS.in files .     
XLIM = (-6, 6)       #  basicaly we see clear bands under the { -6 , 6} but we can change it to according to our will and need . 
SMOOTH = 2           # for smoothness .
TARGET_DPI = 600         
# ======================================================

def smooth_array(arr, window):
    if window <= 1: return arr
    kern = np.ones(window) / window
    return np.convolve(arr, kern, mode='same')

def get_element(name):
    m = re.search(r'\((.*?)\)', name)
    return m.group(1) if m else "Unknown"

# Automatically find files in the current directory
current_dir = os.getcwd()
proj_files = sorted(glob.glob("aiida.pdos.dat.pdos_atm*"))

print(f"--- Processing DOS for {COMPOUND_NAME_PLAIN} ---")

if not proj_files:
    print("Error: No aiida.pdos.dat.pdos_atm* files found in current directory!")
    exit()

# 1. Process Elements & Aggregation
elements = defaultdict(list)
ref_energy = None 

for f in proj_files:
    try:
        data = np.loadtxt(f)
    except:
        data = np.loadtxt(f, skiprows=1)
        
    energy = data[:, 0]
    dos = np.sum(data[:, 1:], axis=1) if data.shape[1] > 2 else data[:, 1]
    el_name = get_element(f)
    elements[el_name].append((energy, dos))
    
    if ref_energy is None or len(energy) > len(ref_energy):
        ref_energy = energy

final_dos = {}
for elem, arrays in elements.items():
    total_elem_dos = np.zeros_like(ref_energy)
    for (e, d) in arrays:
        total_elem_dos += np.interp(ref_energy, e, d, left=0, right=0)
    final_dos[elem] = total_elem_dos

total_dos_curve = sum(final_dos.values())

if SMOOTH > 1:
    total_dos_curve = smooth_array(total_dos_curve, SMOOTH)
    for k in final_dos:
        final_dos[k] = smooth_array(final_dos[k], SMOOTH)

energy_shifted = ref_energy - FERMI_E

# 2. Advanced Publication Plotting
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.major.width': 2.5,
    'ytick.major.width': 2.5,
    'axes.linewidth': 2.5,
    'legend.frameon': False
})

fig, ax = plt.subplots(figsize=(10, 7))

# Plot Total DOS (Always Black)
ax.plot(energy_shifted, total_dos_curve, color='black', lw=3.5, label='Total DOS', zorder=10)
ax.fill_between(energy_shifted, 0, total_dos_curve, color='gray', alpha=0.05)

# --- AUTOMATIC ELEMENT COLOR MAPPING ---
# Uses the 'tab10' colormap to automatically assign unique colors to any elements found
unique_elements = sorted(final_dos.keys())
cmap = plt.get_cmap('tab10') 

for i, elem in enumerate(unique_elements):
    c = cmap(i % 10) # Cycles through 10 distinct professional colors
    ax.plot(energy_shifted, final_dos[elem], color=c, lw=2.2, label=elem, zorder=5)
    ax.fill_between(energy_shifted, 0, final_dos[elem], color=c, alpha=0.25)

# 3. Formatting & Physics Refinements
ax.axvline(0, color='#555555', linestyle='--', linewidth=2.0, zorder=1)
ax.set_xlim(XLIM)
ax.set_ylim(0, np.max(total_dos_curve[(energy_shifted > XLIM[0]) & (energy_shifted < XLIM[1])]) * 1.1)

# Bold Axis Labels with Units
ax.set_xlabel(r'Energy - $E_f$ (eV)', fontsize=16, fontweight='bold', labelpad=10)
ax.set_ylabel('DOS (states/eV)', fontsize=16, fontweight='bold', labelpad=10)
ax.set_title(f'Density of States: {COMPOUND_NAME_LATEX}', fontsize=18, fontweight='bold', pad=15)

# Mirror Ticks
ax.tick_params(top=True, right=True, length=7)

# Bold Tick Labels
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontweight('bold')
    label.set_fontsize(13)

# Legend Configuration
ax.legend(fontsize=13, loc='upper right', prop={'weight': 'bold'})

# Final overlap fix: Prune the bottom y-tick to avoid overlap with x-axis 0
ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins='auto', prune='lower'))

plt.tight_layout()

# Save with dynamic name
out_file = f"DOS_{COMPOUND_NAME_PLAIN}.png"
plt.savefig(out_file, dpi=TARGET_DPI)
print(f"Success! Advanced plot saved as: {out_file}")
plt.show()
