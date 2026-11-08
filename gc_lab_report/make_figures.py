"""Generate figures for the GC fruit-ester post-lab report."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rdkit.Chem import AllChem, Draw

ALCOHOLS = {
    "methanol": "CO", "ethanol": "CCO", "1-butanol": "CCCCO",
    "isobutanol": "CC(C)CO", "isopentanol": "CC(C)CCO",
}
ESTERS = {
    "methanol": "CC(=O)OC", "ethanol": "CC(=O)OCC", "1-butanol": "CC(=O)OCCCC",
    "isobutanol": "CC(=O)OCC(C)C", "isopentanol": "CC(=O)OCCC(C)C",
}
for i, (alc, smi) in enumerate(ALCOHOLS.items(), 1):
    rxn = AllChem.ReactionFromSmarts(f"CC(=O)O.{smi}>>{ESTERS[alc]}.O", useSmiles=True)
    img = Draw.ReactionToImage(rxn, subImgSize=(260, 180))
    img.save(f"figures/rxn_ester{i}.png")

# Model (predicted) chromatogram: qualitative peak positions ordered by boiling point.
# Ramp 30 -> 130 C at 5 C/min; position ~ (bp-30)/5 scaled, purely illustrative.
peaks = [  # label, bp (C), kind
    ("Methyl acetate (57 °C)", 57, "ester"),
    ("Methanol (65 °C)", 64.7, "sm"),
    ("Ethyl acetate (77 °C)", 77, "ester"),
    ("Ethanol (78 °C)", 78, "sm"),
    ("Isobutanol (108 °C)", 107.9, "sm"),
    ("1-Butanol (117 °C)", 117.3, "sm"),
    ("Acetic acid (118 °C)", 118, "sm"),
    ("Isobutyl acetate (117 °C)", 116.5, "ester"),
    ("n-Butyl acetate (126 °C)", 126, "ester"),
    ("Isopentanol (131 °C)", 131, "sm"),
    ("Isopentyl acetate (142 °C)", 142, "ester"),
]
t = np.linspace(0, 20, 4000)
def rt(bp): return 0.6 + (bp - 50) * 0.17
fig, ax = plt.subplots(figsize=(8, 4), dpi=200)
ester_sig = np.zeros_like(t)
for lab, bp, kind in peaks:
    if kind == "ester":
        ester_sig += np.exp(-((t - rt(bp)) ** 2) / (2 * 0.12 ** 2))
ax.plot(t, ester_sig, color="#1f4e79", lw=1.6, label="Possible ester products")
for lab, bp, kind in peaks:
    if kind == "ester":
        name = lab.split(" (")[0]
        dx = {"Isobutyl acetate": -30, "n-Butyl acetate": -6}.get(name, 0)
        ax.annotate(name, (rt(bp), 1.0), xytext=(dx, 6), textcoords="offset points",
                    ha="center", fontsize=7.5, color="#1f4e79")
    else:
        ax.axvline(rt(bp), color="#c55a11", ls="--", lw=0.8)
        name = lab.split(" (")[0]
        ha = "left" if name == "Acetic acid" else "right"
        ax.text(rt(bp) + (0.05 if ha == "left" else -0.05), 0.45, name, rotation=90, fontsize=7,
                color="#c55a11", ha=ha, va="center")
ax.plot([], [], color="#c55a11", ls="--", lw=0.8, label="Starting materials (predicted position)")
ax.set_xlabel("Predicted retention time (min, qualitative)")
ax.set_ylabel("Detector response (arbitrary units)")
ax.set_ylim(0, 1.3); ax.set_xlim(0, 18)
ax.set_yticks([])
ax.legend(fontsize=7.5, loc="upper left", bbox_to_anchor=(0.0, 1.12), ncol=2, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("figures/model_chromatogram.png")
print("done")
