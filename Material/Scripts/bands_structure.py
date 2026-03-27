#!/usr/bin/env python3
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# =========================
# FILES
# =========================
GNU_FILE  = "alas.bands.dat.gnu"
PP_OUT    = "bands.pp.out"

# =========================
# OUTPUT (PNG)
# =========================
OUTPUT_PNG = "bandstructure.png"
SAVE_PNG   = True
PNG_DPI    = 600
PNG_PAD_INCHES = 0.02
PNG_BBOX   = "tight"

# =========================
# USER SETTINGS
# =========================
COMPOUND_NAME = r"Na$_2$MgGeI$_6$"   # edit as needed

BORDER_WIDTH      = 4.0
BAND_LINEWIDTH    = 1.2
BAND_COLOR        = "blue"          # selectable

VLINE_WIDTH       = 1.2
VLINE_STYLE       = "--"
VLINE_COLOR       = "darkgreen"

# Adjustable y-limits (current request: -8 to 8)
YMIN = -8.0
YMAX =  8.0

AXIS_LABEL_FONTSIZE = 13
TICK_LABEL_FONTSIZE = 11

# Compound name location (axes fraction)
NAME_X_FRAC     = 0.50
NAME_Y_FRAC     = 1.03
NAME_HA         = "center"
NAME_VA         = "bottom"
NAME_FONTSIZE   = 16

# Eg label location (x as fraction of x-range, y relative to 0 eV)
SHOW_EG_TEXT      = True
EG_TEXT_X_FRAC    = 0.54
EG_TEXT_Y_OFFSET  = 0.66
EG_FONTSIZE       = 13

DRAW_ZERO_LINE = True
XLABEL = "K-path"
YLABEL = "Energy (eV)"

# =========================
# BAND GAP ARROW (double-headed)
# =========================
DRAW_GAP_ARROW   = True
ARROW_MODE = "auto"          # "auto", "direct", "indirect"
ARROW_COLOR = "brown"        # change to "royalblue", "black", etc.
ARROW_LINEWIDTH = 2.4
ARROW_MUTATION_SCALE = 18
ARROW_STYLE = "<->"
ARROW_ZORDER = 3

# Degeneracy tolerance (eV)
ENERGY_TOL = 1e-3

# =========================
# Labels for symmetry points (pp.out does NOT contain labels in your format)
# =========================
DEFAULT_HS_LABELS = ["W", "L", "Γ", "X", "W", "K"]


# =============================================================================
# Helpers
# =============================================================================
def load_qe_gnu(filename: str):
    """
    Robust loader for QE *.dat.gnu files.
    Supports:
      (A) matrix:  x  E1  E2 ...
      (B) blocks:  x  E   (blank lines separate bands)
    """
    # matrix attempt
    try:
        data = np.genfromtxt(filename)
        if isinstance(data, np.ndarray) and data.ndim == 2 and data.shape[1] >= 3:
            return data[:, 0], data[:, 1:]
    except Exception:
        pass

    # block attempt
    bands = []
    current = []
    with open(filename, "r", errors="ignore") as f:
        for line in f:
            s = line.strip()
            if not s:
                if current:
                    bands.append(np.array(current, dtype=float))
                    current = []
                continue
            if s.startswith("#"):
                continue
            parts = s.split()
            if len(parts) < 2:
                continue
            try:
                xx = float(parts[0]); ee = float(parts[1])
            except ValueError:
                continue
            current.append((xx, ee))
    if current:
        bands.append(np.array(current, dtype=float))

    if len(bands) < 2:
        raise RuntimeError(f"Could not parse usable bands from {filename}.")

    x = bands[0][:, 0]
    nks = len(x)
    for i, b in enumerate(bands):
        if len(b) != nks:
            raise RuntimeError(
                f"Inconsistent band block lengths: band {i+1} has {len(b)} points, expected {nks}."
            )

    E = np.column_stack([b[:, 1] for b in bands])
    return x, E


def find_fermi_energy_verbose_last(files):
    """
    Find Ef from QE outputs with strict matching + provenance.
    IMPORTANT: if a file contains multiple Ef lines, we take the LAST match
    (usually the final converged SCF value).

    Searches files in order (so scf.out first, then nscf.out).
    Returns: (Ef, filename, matched_line) or (None, None, None)
    """
    patterns = [
        re.compile(r"the\s+fermi\s+energy\s+is\s+([-+0-9]*\.?[0-9]+)\s*ev", re.IGNORECASE),
        re.compile(r"fermi\s+energy\s*[:=]?\s*([-+0-9]*\.?[0-9]+)\s*ev", re.IGNORECASE),
        re.compile(r"\bef\s*=\s*([-+0-9]*\.?[0-9]+)\s*ev", re.IGNORECASE),
        # sometimes for insulators QE prints these; we keep them as fallback
        re.compile(r"highest\s+occupied\s+level.*?([-+0-9]*\.?[0-9]+)\s*ev", re.IGNORECASE),
        re.compile(r"lowest\s+unoccupied\s+level.*?([-+0-9]*\.?[0-9]+)\s*ev", re.IGNORECASE),
    ]

    for fn in files:
        try:
            last_val = None
            last_line = None
            with open(fn, "r", errors="ignore") as f:
                for line in f:
                    for pat in patterns:
                        m = pat.search(line)
                        if m:
                            try:
                                last_val = float(m.group(1))
                                last_line = line.strip()
                            except:
                                pass
            if last_val is not None:
                return last_val, fn, last_line
        except FileNotFoundError:
            continue

    return None, None, None


def parse_hsymm_from_bands_pp(pp_out: str):
    """
    Your QE bands.pp.out format:
      high-symmetry point: ... x coordinate   0.0000

    We take the LAST number in that line as x-position.
    """
    xs = []
    with open(pp_out, "r", errors="ignore") as f:
        for line in f:
            if "high-symmetry point" in line and "x coordinate" in line:
                parts = line.strip().split()
                try:
                    xs.append(float(parts[-1]))
                except:
                    pass

    # de-duplicate while preserving order
    xs2 = []
    for v in xs:
        if (not xs2) or abs(v - xs2[-1]) > 1e-8:
            xs2.append(v)

    if not xs2:
        raise RuntimeError(f"Could not extract symmetry x-coordinates from {pp_out}.")
    return xs2


def segment_slices(x):
    breaks = np.r_[False, np.diff(x) < -1e-8]
    segs, start = [], 0
    for i in range(1, len(x)):
        if breaks[i]:
            segs.append((start, i))
            start = i
    segs.append((start, len(x)))
    return segs


def vbm_cbm_pick_nearest_pair(E, x, Ef, tol=1e-3):
    """
    GLOBAL VBM/CBM from plotted E (.gnu):
      Ev = max(E <= Ef)
      Ec = min(E >  Ef)

    If VBM and/or CBM are degenerate at multiple points,
    pick the NEAREST PAIR:
      minimize |x_cbm - x_vbm|, tie-break minimize |k_index difference|.
    """
    occ = (E <= Ef)
    emp = (E >  Ef)
    if not np.any(occ) or not np.any(emp):
        raise RuntimeError("Could not find occupied/unoccupied states relative to Ef. Check Ef.")

    Ev = float(np.max(E[occ]))
    Ec = float(np.min(E[emp]))

    v_cand = np.argwhere(np.abs(E - Ev) <= tol)
    c_cand = np.argwhere(np.abs(E - Ec) <= tol)

    v_cand = np.array([p for p in v_cand if E[p[0], p[1]] <= Ef], dtype=int)
    c_cand = np.array([p for p in c_cand if E[p[0], p[1]] >  Ef], dtype=int)

    if v_cand.size == 0 or c_cand.size == 0:
        raise RuntimeError("No VBM/CBM candidates found. Increase ENERGY_TOL.")

    best = None
    for kv, bv in v_cand:
        kv = int(kv); bv = int(bv)
        xv = float(x[kv])
        for kc, bc in c_cand:
            kc = int(kc); bc = int(bc)
            xc = float(x[kc])
            dx = abs(xc - xv)
            dk = abs(kc - kv)
            score = (dx, dk)
            if (best is None) or (score < best[0]):
                best = (score, (kv, bv), (kc, bc))

    _, (kv, bv), (kc, bc) = best
    return Ev, Ec, (kv, bv), (kc, bc)


# =============================================================================
# MAIN
# =============================================================================
x, Egnu = load_qe_gnu(GNU_FILE)

# --- Ef provenance: scf.out first, then nscf.out, but take LAST match in file ---
Ef, ef_file, ef_line = find_fermi_energy_verbose_last(["scf.out", "nscf.out"])
if Ef is None:
    Ef = 0.0
    print("Ef not found in scf.out/nscf.out -> using Ef = 0.0 eV (bands likely already referenced).")
else:
    print(f"Ef (LAST match) taken from {ef_file}: {Ef:.6f} eV")
    print(f"Matched line: {ef_line}")

Ev, Ec, (kv, bv), (kc, bc) = vbm_cbm_pick_nearest_pair(Egnu, x, Ef, tol=ENERGY_TOL)
Eg = Ec - Ev

# Shift so VBM = 0 eV
Eshift = Egnu - Ev

# Arrow endpoints (exact points, tips touch)
xv, yv = float(x[kv]), float(Eshift[kv, bv])
xc, yc = float(x[kc]), float(Eshift[kc, bc])

# detect direct/indirect (not printed)
is_direct = (abs(xv - xc) < 1e-8)

mode = ARROW_MODE.lower()
if mode == "auto":
    mode = "direct" if is_direct else "indirect"
if mode == "direct":
    xc = xv  # vertical arrow at VBM k

# High-symmetry positions ALWAYS from bands.pp.out
hs_points = parse_hsymm_from_bands_pp(PP_OUT)

# Labels: supplied manually (positions are correct from pp.out)
hs_labels = DEFAULT_HS_LABELS[:len(hs_points)]
if len(hs_labels) < len(hs_points):
    hs_labels += [""] * (len(hs_points) - len(hs_labels))

# =============================================================================
# PLOT
# =============================================================================
fig, ax = plt.subplots(figsize=(8, 6))

for b in range(Eshift.shape[1]):
    for s, t in segment_slices(x):
        ax.plot(x[s:t], Eshift[s:t, b], linewidth=BAND_LINEWIDTH, color=BAND_COLOR)

for xp in hs_points:
    ax.axvline(x=xp, color=VLINE_COLOR, linestyle=VLINE_STYLE, linewidth=VLINE_WIDTH)

ax.set_xticks(hs_points)
ax.set_xticklabels(hs_labels, fontweight="bold", fontsize=TICK_LABEL_FONTSIZE)

for tick in ax.get_yticklabels():
    tick.set_fontweight("bold")
    tick.set_fontsize(TICK_LABEL_FONTSIZE)

ax.set_xlabel(XLABEL, fontweight="bold", fontsize=AXIS_LABEL_FONTSIZE)
ax.set_ylabel(YLABEL, fontweight="bold", fontsize=AXIS_LABEL_FONTSIZE)

if DRAW_ZERO_LINE:
    ax.axhline(0.0, color="black", linestyle="--", linewidth=2.5)

# Compound name
ax.text(
    NAME_X_FRAC, NAME_Y_FRAC, COMPOUND_NAME,
    transform=ax.transAxes,
    fontsize=NAME_FONTSIZE,
    fontweight="bold",
    ha=NAME_HA, va=NAME_VA,
    color="black",
)

# Eg label (only Eg)
if SHOW_EG_TEXT:
    x_min, x_max = float(np.min(x)), float(np.max(x))
    x_eg = x_min + EG_TEXT_X_FRAC * (x_max - x_min)
    y_eg = 0.0 + EG_TEXT_Y_OFFSET
    ax.text(
        x_eg, y_eg,
        rf"E$_g$ = {Eg:.3f} eV",
        fontsize=EG_FONTSIZE,
        fontweight="bold",
        ha="left", va="center",
        color="black",
    )

# Double-headed arrow (adjustable)
if DRAW_GAP_ARROW:
    arrow = FancyArrowPatch(
        (xv, yv), (xc, yc),
        arrowstyle=ARROW_STYLE,
        mutation_scale=ARROW_MUTATION_SCALE,
        linewidth=ARROW_LINEWIDTH,
        color=ARROW_COLOR,
        zorder=ARROW_ZORDER,
        shrinkA=0.0, shrinkB=0.0,
    )
    ax.add_patch(arrow)

# No empty space at x ends
ax.set_xlim(float(np.min(x)), float(np.max(x)))
ax.set_ylim(float(YMIN), float(YMAX))

# Thick border
for spine in ax.spines.values():
    spine.set_linewidth(BORDER_WIDTH)

ax.grid(False)

if SAVE_PNG:
    fig.savefig(OUTPUT_PNG, dpi=PNG_DPI, bbox_inches=PNG_BBOX, pad_inches=PNG_PAD_INCHES)
    print(f"Saved: {OUTPUT_PNG}  (dpi={PNG_DPI})")

fig.tight_layout()
plt.show()


