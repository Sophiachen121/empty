import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "/home/user/empty/figs/"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "font.family": "DejaVu Sans"})
LW = 2.2

def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT + name + ".png", dpi=200)
    plt.close(fig)

def dotted(ax, x, y, x0=0, y0=0):
    ax.plot([x0, x], [y, y], ":", color="gray", lw=1)
    ax.plot([x, x], [y0, y], ":", color="gray", lw=1)

# Q3: four PPFs (wheat vs computers)
fig, axs = plt.subplots(2, 2, figsize=(6.5, 5))
for ax, (name, w, c) in zip(axs.flat, [("A", 30, 10), ("B", 20, 40), ("C", 40, 20), ("D", 10, 30)]):
    ax.plot([0, c], [w, 0], "k", lw=LW)
    ax.set_xlim(0, 45); ax.set_ylim(0, 45)
    ax.set_xticks(range(0, 45, 10)); ax.set_yticks(range(0, 45, 10))
    ax.set_title(f"Country {name}", fontsize=10, fontweight="bold")
    ax.set_xlabel("Computers"); ax.set_ylabel("Wheat (tons)")
save(fig, "q03")

# Q9: total gains from trade
fig, ax = plt.subplots(figsize=(3.8, 3))
q = np.linspace(0, 240, 10)
ax.plot(q, 30 - 0.1*q, "k", lw=LW); ax.plot(q, 6 + 0.1*q, "k", lw=LW)
ax.text(240, 6, "Demand", va="center"); ax.text(240, 30, "Supply", va="center")
dotted(ax, 120, 18); ax.plot(120, 18, "ko")
ax.set_xlim(0, 280); ax.set_ylim(0, 36)
ax.set_yticks([6, 18, 30]); ax.set_yticklabels(["$6", "18", "30"]); ax.set_xticks([60, 120, 180, 240])
ax.set_xlabel("Q"); ax.set_ylabel("P", labelpad=8)
save(fig, "q09")

# Q10: which statement true
fig, ax = plt.subplots(figsize=(3.8, 3))
q = np.linspace(0, 20, 10)
ax.plot(q, 100 - 5*q, "k", lw=LW); ax.plot(q, 5*q, "k", lw=LW)
ax.text(20.3, 4, "Demand"); ax.text(20.3, 98, "Supply")
for x in (4, 10, 16):
    for y in (100 - 5*x, 5*x):
        dotted(ax, x, y); ax.plot(x, y, "ko", ms=4)
ax.set_xlim(0, 25); ax.set_ylim(0, 110)
ax.set_xticks([4, 10, 16, 20]); ax.set_yticks([20, 50, 80, 100]); ax.set_yticklabels(["$20", "50", "80", "100"])
ax.set_xlabel("Q"); ax.set_ylabel("P")
save(fig, "q10")

# Q12: four shift panels
fig, axs = plt.subplots(2, 2, figsize=(6.2, 5))
x = np.linspace(1, 9, 10)
def panel(ax, title, kind, direction):
    if kind == "D":
        s, = ax.plot(x, x, ":", color="k", lw=1.5); ax.text(9.1, 9, "Supply", fontsize=8)
        d0 = 10 - x; ax.plot(x, d0, "k", lw=LW); ax.text(9.1, 0.8, "D$_0$", fontsize=9)
        sh = 1.6 * direction
        ax.plot(x + sh, d0, "k", lw=LW); ax.text(9.1 + sh, 0.8, "D$_1$", fontsize=9)
        ax.annotate("", xy=(6 + sh*0.8, 5.2), xytext=(6, 5.2), arrowprops=dict(arrowstyle="->"))
    else:
        ax.plot(x, 10 - x, ":", color="k", lw=1.5); ax.text(9.1, 0.8, "Demand", fontsize=8)
        ax.plot(x, x, "k", lw=LW); ax.text(9.1, 9, "S$_0$", fontsize=9)
        sh = 1.6 * direction
        ax.plot(x + sh, x, "k", lw=LW); ax.text(9.1 + sh, 9, "S$_1$", fontsize=9)
        ax.annotate("", xy=(6 + sh*0.8, 7), xytext=(6, 7), arrowprops=dict(arrowstyle="->"))
    ax.set_xlim(0, 12); ax.set_ylim(0, 11); ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("Q"); ax.set_ylabel("P"); ax.set_title(title, fontsize=10, fontweight="bold")
panel(axs[0, 0], "Figure A", "D", +1)
panel(axs[0, 1], "Figure B", "S", -1)
panel(axs[1, 0], "Figure C", "S", +1)
panel(axs[1, 1], "Figure D", "D", -1)
save(fig, "q12")

# Q19: tax incidence
fig, ax = plt.subplots(figsize=(4, 3.2))
q = np.linspace(0, 760, 10)
ax.plot(q, 5.25 - 0.0045*q, "k", lw=LW); ax.text(665, 2.3, "D")
ax.plot(q, 2.25 + 0.0015*q, "k", lw=LW); ax.text(780, 3.45, "S$_1$")
ax.plot(q, 3.25 + 0.0015*q, "k", lw=LW); ax.text(780, 4.45, "S$_2$")
q2 = 1000/3
for (xx, yy) in [(500, 3.0), (q2, 3.75), (q2, 2.75)]:
    dotted(ax, xx, yy); ax.plot(xx, yy, "ko", ms=4)
ax.set_xlim(0, 800); ax.set_ylim(2.2, 4.6)
ax.set_yticks([2.75, 3.0, 3.75]); ax.set_yticklabels(["$2.75", "$3.00", "$3.75"])
ax.set_xticks([q2, 500]); ax.set_xticklabels(["333", "500"])
ax.set_xlabel("Quantity of pizza slices"); ax.set_ylabel("Price")
save(fig, "q19")

# Q20: three demand curves rotating through common point
fig, ax = plt.subplots(figsize=(4, 3.2))
px, py = 5, 5
for slope, lab in [(-3, "A"), (-1, "B"), (-0.35, "C")]:
    xs = np.linspace(px - (5 if slope != -3 else 1.6), px + (4 if slope != -3 else 1.6), 10)
    ys = py + slope*(xs - px)
    m = ys >= 0
    ax.plot(xs[m], ys[m], "k", lw=LW); ax.text(xs[m][-1] + 0.15, ys[m][-1], lab, fontweight="bold")
ax.set_xlim(0, 11); ax.set_ylim(0, 11); ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("Quantity of landline phone service"); ax.set_ylabel("Price ($)")
save(fig, "q20")

# Q21: labeled surplus diagram
fig, ax = plt.subplots(figsize=(4, 3.3))
q = np.linspace(0, 10, 10)
ax.plot(q[q <= 8], 10 - q[q <= 8], "k", lw=LW); ax.text(8.1, 1.8, "Demand")
ax.plot(q[q <= 8], 2 + q[q <= 8], "k", lw=LW); ax.text(8.1, 10, "Supply")
for y in (8, 6, 4):
    ax.plot([0, 6], [y, y], "--", color="gray", lw=0.8)
for xv in (2, 6):
    ax.plot([xv, xv], [0, 8], "--", color="gray", lw=0.8)
pts = {"A": (0, 10), "B": (0, 8), "E": (0, 6), "J": (0, 4), "M": (0, 2),
       "C": (2, 8), "F": (2, 6), "G": (4, 6), "H": (6, 6), "D": (6, 8), "K": (6, 4), "L": (2, 4)}
off = {"A": (-0.45, 0), "B": (-0.45, 0), "E": (-0.45, 0), "J": (-0.45, 0), "M": (-0.45, 0),
       "C": (0, 0.35), "F": (-0.4, 0.25), "G": (0, 0.4), "H": (0.15, 0.25), "D": (0, 0.35),
       "K": (0.2, 0.2), "L": (0.2, -0.4)}
for k, (xx, yy) in pts.items():
    ax.plot(xx, yy, "ko", ms=4, clip_on=False)
    ax.text(xx + off[k][0], yy + off[k][1], k, style="italic", ha="center", va="center")
ax.set_xlim(0, 10); ax.set_ylim(0, 11); ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("Quantity"); ax.set_ylabel("Price", labelpad=14)
save(fig, "q21")

# Q24: price ceiling on coffee
fig, ax = plt.subplots(figsize=(4, 3.2))
q = np.linspace(0, 120, 10)
ax.plot(q, 12 - 0.1*q, "k", lw=LW); ax.text(118, 0.6, "D")
q2 = np.linspace(0, 140, 10)
ax.plot(q2, 3 + 0.05*q2, "k", lw=LW); ax.text(141, 10, "S")
ax.set_xticks(range(0, 161, 20)); ax.set_yticks(range(0, 15, 2))
ax.grid(True, color="#ddd"); ax.set_xlim(0, 160); ax.set_ylim(0, 14)
ax.set_xlabel("Pounds of coffee (thousands)"); ax.set_ylabel("Price per pound ($)")
save(fig, "q24")

# Q31: demand shift right (curved)
fig, ax = plt.subplots(figsize=(4, 3.2))
qq = np.linspace(20, 60, 50)
ax.plot(qq, 1600/qq + 0, "k", lw=LW); ax.text(60, 1600/60 - 5, "D$_1$")
ax.plot(qq + 25, 1600/qq, "k", lw=LW); ax.text(86, 1600/60 - 5, "D$_2$")
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_xticks(range(0, 101, 20)); ax.set_yticks(range(0, 101, 20))
ax.set_xlabel("Quantity"); ax.set_ylabel("Price ($)")
save(fig, "q31")

# Q32: supply with points
fig, ax = plt.subplots(figsize=(4, 3.2))
q = np.linspace(200, 800, 10)
ax.plot(q, -20 + 0.1*q, "k", lw=LW); ax.text(805, 60, "S")
for lab, (xx, yy) in {"A": (300, 10), "B": (400, 20), "C": (500, 30), "D": (700, 50)}.items():
    dotted(ax, xx, yy); ax.plot(xx, yy, "ko", ms=5); ax.text(xx + 15, yy - 5, lab)
ax.set_xlim(0, 850); ax.set_ylim(0, 65)
ax.set_xticks([300, 400, 500, 700]); ax.set_yticks([10, 20, 30, 50])
ax.set_xlabel("Quantity"); ax.set_ylabel("Price ($)")
save(fig, "q32")

# Q38: two PPFs
fig, axs = plt.subplots(1, 2, figsize=(6.4, 3))
for ax, name, fmax, bmax, pt in [(axs[0], "Country X", 60, 30, (15, 30)), (axs[1], "Country Y", 20, 40, (20, 10))]:
    ax.plot([0, bmax], [fmax, 0], "k", lw=LW)
    dotted(ax, pt[0], pt[1]); ax.plot(*pt, "ko", ms=5)
    ax.set_xlim(0, 65); ax.set_ylim(0, 65); ax.set_xticks(range(0, 61, 10)); ax.set_yticks(range(0, 61, 10))
    ax.set_title(name, fontsize=10, fontweight="bold"); ax.set_xlabel("Bread (loaves)"); ax.set_ylabel("Fish (lbs)")
save(fig, "q38")

# Q39: price ceiling areas
fig, ax = plt.subplots(figsize=(4.2, 3.4))
q = np.linspace(0, 10, 10)
ax.plot(q, 10 - q, "k", lw=LW); ax.text(9.6, 0.6, "D")
ax.plot(q[q <= 9], 1 + q[q <= 9], "k", lw=LW); ax.text(9, 10.1, "S")
Qs, Pc, Pstar, Qstar = 2, 3, 5.5, 4.5
ax.plot([0, 8], [Pc, Pc], "k", lw=1.2); ax.text(8.1, Pc, "Price ceiling", va="center", fontsize=8)
ax.plot([0, Qstar], [Pstar, Pstar], "--", color="gray", lw=0.9)
ax.plot([Qs, Qs], [0, 10 - Qs], "--", color="gray", lw=0.9)
ax.plot([Qstar, Qstar], [0, Pstar], ":", color="gray", lw=0.9)
for lab, xy in {"A": (0.7, 7.0), "B": (1.0, 4.2), "C": (2.8, 6.3), "D": (2.8, 4.6), "E": (1.0, 2.2)}.items():
    ax.text(*xy, lab, fontweight="bold", ha="center", va="center")
ax.set_xlim(0, 10); ax.set_ylim(0, 11)
ax.set_xticks([Qs, Qstar]); ax.set_xticklabels(["Q$_s$", "Q*"])
ax.set_yticks([Pc, Pstar]); ax.set_yticklabels(["P$_c$", "P*"])
ax.set_xlabel("Quantity"); ax.set_ylabel("Price")
save(fig, "q39")

# Q40: subsidy
fig, ax = plt.subplots(figsize=(4, 3.2))
q = np.linspace(0, 10, 10)
ax.plot(q, 8 - 0.7*q, "k", lw=LW); ax.text(10.1, 1, "D$_1$")
ax.plot(q, 9.5 - 0.7*q, "k", lw=LW); ax.text(10.1, 2.5, "D$_2$")
ax.plot(q[q <= 8], 0.3 + q[q <= 8], "k", lw=LW); ax.text(7.6, 8.6, "S$_2$")
ax.plot(q[q <= 8]+1.5, 0.3 + q[q <= 8], "k", lw=LW); ax.text(9.2, 8.6, "S$_1$")
ax.set_xlim(0, 11); ax.set_ylim(0, 10); ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("Quantity"); ax.set_ylabel("Price")
save(fig, "q40")

# Q41: rent control
fig, ax = plt.subplots(figsize=(4.3, 3.4))
q = np.linspace(0, 10, 10)
ax.plot(q, 10 - q, "k", lw=LW); ax.text(9.6, 0.6, "D", fontweight="bold")
ax.plot(q, 2.5 + 0.5*q, "k", lw=LW); ax.text(9.6, 7.6, "S$_1$", fontweight="bold")
qs = np.linspace(2.4, 6.6, 10); ax.plot(qs, 5 + 2.5*(qs - 5), "k", lw=LW); ax.text(6.4, 10.3, "S$_2$", fontweight="bold")
Pc = 3.5
ax.plot([0, 10], [Pc, Pc], "k", lw=1.2); ax.text(0.1, Pc + 0.25, "Controlled rent", fontsize=8)
for xv, lab in [(2, "Q$_a$"), (4.4, "Q$_b$"), (5, "Q$_c$"), (6.5, "Q$_d$")]:
    ax.plot([xv, xv], [0, 9.5], "--", color="gray", lw=0.9)
ax.set_xticks([2, 4.4, 5, 6.5]); ax.set_xticklabels(["Q$_a$", "Q$_b$", "Q$_c$", "Q$_d$"])
ax.set_xlim(0, 10.5); ax.set_ylim(0, 11); ax.set_yticks([])
ax.set_xlabel("Quantity of apartments"); ax.set_ylabel("Rent ($)")
save(fig, "q41")

# Q42: hyperbolic demand
fig, ax = plt.subplots(figsize=(4.2, 3.2))
qq = np.linspace(6, 55, 100)
ax.plot(qq, 120/qq, "k", lw=LW); ax.text(55.5, 120/55, "D")
for xx in (10, 15, 30, 40):
    dotted(ax, xx, 120/xx); ax.plot(xx, 120/xx, "ko", ms=4)
ax.set_xlim(0, 60); ax.set_ylim(0, 22)
ax.set_xticks([10, 15, 30, 40]); ax.set_yticks(range(0, 21, 2))
ax.set_xlabel("Quantity of good Y"); ax.set_ylabel("Price ($)")
save(fig, "q42")

# Q43: housing supply elastic vs inelastic
fig, ax = plt.subplots(figsize=(4.2, 3.4))
q = np.linspace(0, 10, 10)
ax.plot(q, 7 - 0.9*q, "k", lw=LW); ax.text(7.3, 0.3, "D$_1$")
ax.plot(q, 9.5 - 0.9*q, "k", lw=LW); ax.text(10.1, 0.5, "D$_2$")
QA = (7 - 3)/0.9
ax.plot([0, 10], [3, 3], "k", lw=1.5); ax.text(10.1, 3, "S$_X$", va="center")
xs = np.linspace(QA - 1.2, QA + 2.6, 10); ax.plot(xs, 3 + 2*(xs - QA), "k", lw=1.5); ax.text(QA + 2.6, 3 + 2*2.6 + 0.2, "S$_Y$")
QB = QA + 2.5/2.9; PB = 3 + 2*(QB - QA)
QC = (9.5 - 3)/0.9
for lab, (xx, yy) in {"A": (QA, 3), "B": (QB, PB), "C": (QC, 3)}.items():
    ax.plot(xx, yy, "ko"); dotted(ax, xx, yy); ax.text(xx + 0.2, yy + 0.3, lab, fontweight="bold")
ax.set_xlim(0, 11); ax.set_ylim(0, 10)
ax.set_yticks([3, PB]); ax.set_yticklabels(["P$_1$", "P$_2$"])
ax.set_xticks([QA, QB, QC]); ax.set_xticklabels(["Q$_1$", "Q$_2$", "Q$_3$"])
ax.set_xlabel("Quantity of housing"); ax.set_ylabel("Price")
save(fig, "q43")

# Q45: prohibition
fig, ax = plt.subplots(figsize=(4.4, 3.5))
q = np.linspace(36, 54, 10); ax.plot(q, 270 - 5*q, "k", lw=LW); ax.text(35, 92, "D")
q = np.linspace(5, 90, 10); ax.plot(q, q + 30, "k", lw=LW); ax.text(70, 102, "S$_2$")
q = np.linspace(32, 110, 10); ax.plot(q, q - 30, "k", lw=LW); ax.text(111, 80, "S$_1$")
ax.plot([0, 40], [70, 70], ":", color="gray"); ax.plot([40, 40], [0, 70], ":", color="gray")
ax.plot([0, 50], [20, 20], ":", color="gray"); ax.plot([50, 50], [0, 20], ":", color="gray")
for lab, xy in {"A": (20, 45), "C": (20, 10), "D": (45, 10)}.items():
    ax.text(*xy, lab, fontweight="bold", ha="center", va="center")
ax.set_xlim(0, 120); ax.set_ylim(0, 110)
ax.set_xticks([0, 20, 40, 50, 60, 80, 100]); ax.set_yticks([20, 40, 70, 100])
ax.set_xlabel("Quantity"); ax.set_ylabel("Price ($)")
save(fig, "q45")

# Q48-50: tax areas
fig, ax = plt.subplots(figsize=(4.6, 3.8))
q = np.linspace(0, 90, 10)
ax.plot(q, 100 - q, "k", lw=LW); ax.text(88, 6, "D", fontweight="bold")
q = np.linspace(0, 70, 10)
ax.plot(q, 20 + q, "k", lw=LW); ax.text(71, 88, "S (no tax)", fontsize=8)
q = np.linspace(0, 55, 10)
ax.plot(q, 40 + q, "k", lw=LW); ax.text(52, 98, "S (with tax)", fontsize=8)
for y, xe in [(70, 30), (60, 40), (50, 30)]:
    ax.plot([0, xe], [y, y], "--", color="gray", lw=0.9)
ax.plot([30, 30], [0, 70], "--", color="gray", lw=0.9); ax.plot([40, 40], [0, 60], "--", color="gray", lw=0.9)
for lab, xy in {"A": (8, 80), "B": (8, 65), "C": (33, 63), "F": (5, 55), "G": (33, 56.5), "H": (5, 37)}.items():
    ax.text(*xy, lab, fontweight="bold", ha="center", va="center")
ax.set_xlim(0, 100); ax.set_ylim(0, 105)
ax.set_xticks([30, 40]); ax.set_yticks([20, 40, 50, 60, 70, 100])
ax.set_xlabel("Quantity"); ax.set_ylabel("Price ($)")
save(fig, "q48")
print("ok")
