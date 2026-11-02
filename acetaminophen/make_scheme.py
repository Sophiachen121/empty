"""Draw the acetaminophen synthesis reaction scheme (full Lewis structures)
and the yield calculations. Outputs SVG, PNG and PDF.

Run:  python3 make_scheme.py
"""
import math
import os

# ---------------- experimental data ----------------
MASS_AMINOPHENOL = 1.029          # g
MW_AMINOPHENOL = 109.13           # g/mol
MW_ACETAMINOPHEN = 151.16         # g/mol
CRUDE = (1.694, 0.238)            # (filter paper + solid, filter paper)
RECRYST = (0.816, 0.236)
REACTION_TIME = "45 min"          # <-- edit to your own notebook time
SOLVENT = "H<tspan baseline-shift='sub' font-size='70%'>2</tspan>O"

mol = MASS_AMINOPHENOL / MW_AMINOPHENOL
theo = mol * MW_ACETAMINOPHEN
crude_g = CRUDE[0] - CRUDE[1]
rec_g = RECRYST[0] - RECRYST[1]
crude_pct = crude_g / theo * 100
rec_pct = rec_g / theo * 100

# ---------------- drawing helpers ----------------
S = 46            # px per bond-length unit
FONT = "Arial, Helvetica, sans-serif"
BLACK, RED, BLUE, GREEN = "#000000", "#C62828", "#1565C0", "#2E7D32"
LABEL_R = 0.27    # bond trimmed this far from a labelled atom centre
out = []


def P(x, y, ox, oy):
    return ox + x * S, oy - y * S


class Mol:
    def __init__(self, ox, oy):
        self.ox, self.oy = ox, oy
        self.atoms = {}

    def atom(self, name, x, y, el, color=BLACK, lp=()):
        self.atoms[name] = (x, y, el, color, lp)

    def at(self, base, ang, dist=1.0):
        x, y = self.atoms[base][:2]
        a = math.radians(ang)
        return x + dist * math.cos(a), y + dist * math.sin(a)

    def bond(self, a, b, order=1, color=BLACK, side=0):
        x1, y1 = self.atoms[a][:2]
        x2, y2 = self.atoms[b][:2]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        px, py = -uy, ux
        sx, sy = x1 + ux * LABEL_R, y1 + uy * LABEL_R
        ex, ey = x2 - ux * LABEL_R, y2 - uy * LABEL_R
        offs = [0] if order == 1 else [-0.075, 0.075]
        for o in offs:
            X1, Y1 = P(sx + px * o, sy + py * o, self.ox, self.oy)
            X2, Y2 = P(ex + px * o, ey + py * o, self.ox, self.oy)
            out.append(f'<line x1="{X1:.1f}" y1="{Y1:.1f}" x2="{X2:.1f}" '
                       f'y2="{Y2:.1f}" stroke="{color}" stroke-width="1.8" '
                       f'stroke-linecap="round"/>')

    def draw_atoms(self):
        for x, y, el, color, lp in self.atoms.values():
            X, Y = P(x, y, self.ox, self.oy)
            out.append(f'<text x="{X:.1f}" y="{Y + 6:.1f}" font-family="{FONT}" '
                       f'font-size="17" text-anchor="middle" fill="{color}">{el}</text>')
            for ang in lp:  # lone pairs: two dots
                a = math.radians(ang)
                cx, cy = x + 0.36 * math.cos(a), y + 0.36 * math.sin(a)
                px, py = -math.sin(a) * 0.075, math.cos(a) * 0.075
                for s in (-1, 1):
                    DX, DY = P(cx + s * px, cy + s * py, self.ox, self.oy)
                    out.append(f'<circle cx="{DX:.1f}" cy="{DY:.1f}" r="2" fill="{color}"/>')


def text(x, y, s, size=17, anchor="middle", color=BLACK, weight="normal", style="normal"):
    out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
               f'text-anchor="{anchor}" fill="{color}" font-weight="{weight}" '
               f'font-style="{style}">{s}</text>')


def methyl(m, c, cname, bond_dir, hs, color, hcolor=None):
    """Add CH3 carbon `cname` attached to `c` and its three H atoms."""
    hcolor = hcolor or color
    x, y = m.at(c, bond_dir)
    m.atom(cname, x, y, "C", color)
    m.bond(c, cname, 1, color)
    for i, a in enumerate(hs):
        hx, hy = m.at(cname, a)
        m.atom(f"{cname}H{i}", hx, hy, "H", hcolor)
        m.bond(cname, f"{cname}H{i}", 1, hcolor)


def benzene_ring(m, n_color=BLACK, o_color=BLACK):
    """para-substituted ring, C0 (right) bears N, C3 (left) bears O."""
    for k in range(6):
        a = math.radians(60 * k)
        m.atom(f"C{k}", math.cos(a), math.sin(a), "C")
    for k in range(6):
        m.bond(f"C{k}", f"C{(k + 1) % 6}", 2 if k % 2 == 0 else 1)
    for k in (1, 2, 4, 5):
        hx, hy = m.at(f"C{k}", 60 * k)
        m.atom(f"H{k}", hx, hy, "H")
        m.bond(f"C{k}", f"H{k}")
    # phenol O-H
    ox_, oy_ = m.at("C3", 180)
    m.atom("O", ox_, oy_, "O", o_color, lp=(105, 195))
    m.bond("C3", "O")
    hx, hy = m.at("O", 240)
    m.atom("HO", hx, hy, "H", o_color)
    m.bond("O", "HO", 1, o_color)


# ---------------- canvas ----------------
W, H = 1450, 430
BASE = 180  # vertical centre line of the molecules (px)

# 1) 4-aminophenol
m = Mol(140, BASE)
benzene_ring(m)
nx, ny = m.at("C0", 0)
m.atom("N", nx, ny, "N", BLUE, lp=(0,))
m.bond("C0", "N", 1, BLUE)
for name, ang, col in (("HNa", 60, BLUE), ("HNb", 300, GREEN)):
    hx, hy = m.at("N", ang)
    m.atom(name, hx, hy, "H", col)
    m.bond("N", name, 1, col)
m.draw_atoms()
text(140, 335, "4-aminophenol")

text(300, BASE + 6, "+", size=26)

# 2) acetic anhydride
m = Mol(430, BASE + 20)
m.atom("Ob", 0, 0, "O", BLACK, lp=(90, 270))
for side, sgn, col in (("L", -1, RED), ("R", 1, BLACK)):
    cx, cy = m.at("Ob", 90 - sgn * 60)
    m.atom(f"C{side}", cx, cy, "C", col)
    m.bond("Ob", f"C{side}", 1, BLACK)
    m.atom(f"O{side}", cx, cy + 1, "O", col, lp=(30, 150))
    m.bond(f"C{side}", f"O{side}", 2, col)
    d = 270 + sgn * 60  # 210 (left) / 330 (right)
    hs = (135, 225, 290) if sgn < 0 else (45, 315, 250)
    methyl(m, f"C{side}", f"M{side}", d, hs, col)
m.draw_atoms()
text(430, 335, "acetic anhydride")

# 3) arrow + conditions
ax1, ax2 = 585, 790
out.append(f'<line x1="{ax1}" y1="{BASE}" x2="{ax2 - 4}" y2="{BASE}" stroke="black" stroke-width="2"/>')
out.append(f'<polygon points="{ax2},{BASE} {ax2 - 14},{BASE - 6} {ax2 - 14},{BASE + 6}" fill="black"/>')
mid = (ax1 + ax2) / 2
text(mid, BASE - 34, SOLVENT, size=18)
text(mid, BASE - 12, REACTION_TIME, size=18)
text(mid, BASE + 26, "60 °C", size=16)

# 4) acetaminophen
m = Mol(915, BASE)
benzene_ring(m)
nx, ny = m.at("C0", 0)
m.atom("N", nx, ny, "N", BLUE, lp=(120,))
m.bond("C0", "N", 1, BLUE)
hx, hy = m.at("N", 300)
m.atom("HNa", hx, hy, "H", BLUE)
m.bond("N", "HNa", 1, BLUE)
cx, cy = m.at("N", 60)
m.atom("Cc", cx, cy, "C", RED)
m.bond("N", "Cc", 1, BLUE)
m.atom("Oc", cx, cy + 1, "O", RED, lp=(30, 150))
m.bond("Cc", "Oc", 2, RED)
methyl(m, "Cc", "Me", 330, (45, 315, 250), RED)
m.draw_atoms()
text(990, 335, "acetaminophen")
text(990, 362, f"crude yield: {crude_pct:.1f}%", size=16)
text(990, 386, f"recrystallized yield: {rec_pct:.1f}%", size=16)

text(1205, BASE + 6, "+", size=26)

# 5) acetic acid
m = Mol(1330, BASE + 10)
m.atom("C", 0, 0, "C")
m.atom("O1", 0, 1, "O", lp=(30, 150))
m.bond("C", "O1", 2)
ox_, oy_ = m.at("C", 330)
m.atom("O2", ox_, oy_, "O", lp=(90, 270))
m.bond("C", "O2")
hx, hy = m.at("O2", 30)
m.atom("HO", hx, hy, "H", GREEN)
m.bond("O2", "HO", 1, GREEN)
methyl(m, "C", "Me", 210, (135, 225, 290), BLACK)
m.draw_atoms()
text(1330, 335, "acetic acid")

# legend
text(40, 415, "Color key: ", size=13, anchor="start")
text(110, 415, "red = acetyl group transferred from acetic anhydride;", size=13, anchor="start", color=RED)
text(445, 415, "blue = amine nitrogen (becomes the amide N);", size=13, anchor="start", color=BLUE)
text(735, 415, "green = N–H hydrogen that ends up on acetic acid.", size=13, anchor="start", color=GREEN)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="white"/>'
       + "\n".join(out) + "</svg>")

here = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(here, "acetaminophen_scheme.svg")
with open(svg_path, "w") as f:
    f.write(svg)

print(f"mol 4-aminophenol = {mol:.5f} mol; theoretical yield = {theo:.3f} g")
print(f"crude {crude_g:.3f} g -> {crude_pct:.1f}%;  recryst {rec_g:.3f} g -> {rec_pct:.1f}%")

# render PNG + PDF with the pre-installed Chromium
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg.set_content(f"<html><body style='margin:0'>{svg}</body></html>")
        pg.screenshot(path=os.path.join(here, "acetaminophen_scheme.png"))
        pg.pdf(path=os.path.join(here, "acetaminophen_scheme.pdf"),
               width=f"{W}px", height=f"{H}px", print_background=True)
        b.close()
except ImportError:
    print("playwright not found; only SVG written")
