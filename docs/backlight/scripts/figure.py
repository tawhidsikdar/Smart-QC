import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle, Polygon
from tess_load import load
C = load("tess.txt")
def section(tris, axis, val):
    d = tris[:, :, axis] - val; segs = []
    for t, dd in zip(tris, d):
        pts = []
        for i in range(3):
            j = (i + 1) % 3
            if (dd[i] < 0) != (dd[j] < 0):
                a = dd[i] / (dd[i] - dd[j]); pts.append(t[i] + a * (t[j] - t[i]))
        if len(pts) == 2: segs.append(pts)
    return np.array(segs)

fig, ax = plt.subplots(figsize=(13, 11))
X0 = -56.4
for n, c in C.items():
    w = c["world"]; m = (w[:, :, 0].min(1) <= X0) & (w[:, :, 0].max(1) >= X0)
    if not m.any(): continue
    s = section(w[m], 0, X0)
    if not len(s): continue
    if "acrylic_side1" in n: col, lw = "black", 2.5
    elif "acrylic bottom" in n: col, lw = "#c9a227", 1.6
    elif "enclosure" in n: col, lw = "tab:green", 1.0
    else: col, lw = "0.55", 0.8
    ax.add_collection(LineCollection(s[:, :, [2, 1]], colors=col, linewidths=lw))
# proposed parts ----------------------------------------------------------
ax.add_patch(Rectangle((-131.6, 28.5), 390, 2.0, color="0.35"))                       # base plate
ax.add_patch(Rectangle((-86.6, 30.5), 2.0, 54.5, color="#bbbbbb", ec="0.3", lw=.5))    # white walls
ax.add_patch(Rectangle((211.4, 30.5), 2.0, 54.5, color="#bbbbbb", ec="0.3", lw=.5))
zs = -84.6 + 18.5 + 37.0 * np.arange(8)
for z in zs: ax.add_patch(Rectangle((z - 5, 30.5), 10, 1.2, color="gold", ec="orange"))
ax.add_patch(Rectangle((-91.6, 85), 310, 5, color="#fff3c4", alpha=.9, ec="#c9a227"))  # opal floor (lit part)
ax.plot([-96.6, 223.4], [90.6, 90.6], color="tab:blue", lw=2.5)                          # cloth 320 mm
# example camera
cy = 90 + 235
ax.add_patch(Rectangle((63.4 - 47, cy), 94, 24, fill=False, ls="--", ec="tab:purple", lw=1.2))
hf = np.tan(np.radians(35.2)) * 235
ax.plot([63.4, 63.4 - hf], [cy, 90], ls=":", color="tab:purple"); ax.plot([63.4, 63.4 + hf], [cy, 90], ls=":", color="tab:purple")
for z in zs[:1]:
    pass
# light rays sketch
for z in zs[[2, 3]]:
    for a in (-50, -25, 0, 25, 50):
        ax.plot([z, z + np.tan(np.radians(a)) * 53.5], [31.7, 85], color="orange", lw=.4, alpha=.6)
# annotations ---------------------------------------------------------------
def dim_v(z, y0, y1, txt, side=1):
    ax.annotate("", (z, y0), (z, y1), arrowprops=dict(arrowstyle="<->", lw=1))
    ax.text(z + 3 * side, (y0 + y1) / 2, txt, va="center", ha="left" if side > 0 else "right", fontsize=9)
def dim_h(y, z0, z1, txt, dy=3):
    ax.annotate("", (z0, y), (z1, y), arrowprops=dict(arrowstyle="<->", lw=1))
    ax.text((z0 + z1) / 2, y + dy, txt, ha="center", va="bottom" if dy > 0 else "top", fontsize=9)
dim_v(-40, 31.7, 85, "H = 53.5 mm\nLED face \u2192 floor underside")
dim_v(110, 90.6, cy, "\u2248 235 mm lens \u2192 cloth\n(example, camera not in CAD yet)")
dim_h(10, -84.6, 211.4, "lit width 296 mm (white light-box inner)", dy=-3)
dim_h(97, -96.6, 223.4, "cloth 320 mm (edges rest 5 mm on the opaque holder ledges)")
dim_h(400, -101.6, 228.4, "booth inside 330 mm (black matte walls)")
ax.text(63.4, 140, "transmitted light \u2191 to camera", ha="center", color="tab:purple", fontsize=9)
ax.text(63.4, 66, "white reflective light box (walls + base painted white)", ha="center", fontsize=9)
ax.text(63.4, 36, "8 rows of 12 V 2835 LED strip (60 LED/m), rows 37 mm apart, running along cloth travel", ha="center", fontsize=8.5)
ax.text(63.4, 22.5, "", ha="center")
ax.text(-131, 24, "2 mm aluminium base plate bolted under both 2040 rails (bottom T-slot, M5 T-nuts)", fontsize=8.5, va="top")
ax.text(63.4, 87.5, "5 mm OPAL (milky) acrylic floor = diffuser (replaces clear sheet, same size)", ha="center", fontsize=8.5, va="center")
ax.set_xlim(-160, 300); ax.set_ylim(-8, 420); ax.set_aspect("equal")
ax.set_xlabel("Z (mm) - across the cloth"); ax.set_ylabel("Y (mm) - up")
ax.set_title("Section through booth centre (X = -56.4) - real CAD geometry (lines) + proposed backlight (filled)")
ax.grid(alpha=.2)
fig.savefig("backlight_section.png", dpi=120, bbox_inches="tight"); plt.close(fig)

# ---- top view of LED layout
fig, ax = plt.subplots(figsize=(10, 9))
ax.add_patch(Rectangle((-181.4, -84.6), 250, 296, fill=False, ec="0.3", lw=2))
ax.add_patch(Rectangle((-181.4 - 2, -86.6), 254, 300, fill=False, ec="0.6", lw=1, ls="--"))
for z in zs:
    ax.add_patch(Rectangle((-181.4, z - 5), 250, 10, color="#fff6cc", ec="orange", lw=.6))
    for k in range(15):
        x = -181.4 + 8.333 + 16.667 * k
        ax.add_patch(Rectangle((x - 1.75, z - 1.4), 3.5, 2.8, color="gold", ec="darkorange", lw=.5))
    for c in range(1, 5): ax.plot([-181.4 + 50 * c] * 2, [z - 6, z + 6], color="red", lw=.7)
ax.annotate("", (-181.4, -100), (68.6, -100), arrowprops=dict(arrowstyle="<->"))
ax.text(-56.4, -104, "250 mm = 5 strip segments (cut marks in red), along cloth travel X", ha="center", va="top")
ax.annotate("", (85, -84.6), (85, 211.4), arrowprops=dict(arrowstyle="<->"))
ax.text(88, 63.4, "296 mm inner\n8 rows @ 37 mm\nedge rows 18.5 mm\nfrom the walls", va="center")
ax.annotate("", (-195, zs[0]), (-195, zs[1]), arrowprops=dict(arrowstyle="<->"))
ax.text(-198, (zs[0] + zs[1]) / 2, "37", ha="right", va="center")
ax.annotate("", (-195, -84.6), (-195, zs[0]), arrowprops=dict(arrowstyle="<->"))
ax.text(-198, (zs[0] - 84.6) / 2, "18.5", ha="right", va="center")
ax.text(-56.4, 222, "8 rows x 15 LEDs = 120 LEDs, 2.0 m strip, LED pitch 16.7 mm along the row", ha="center")
ax.set_xlim(-230, 150); ax.set_ylim(-120, 240); ax.set_aspect("equal")
ax.set_xlabel("X (mm) - cloth travel"); ax.set_ylabel("Z (mm) - across cloth")
ax.set_title("Top view of LED plate inside the light box (real assembly coordinates)")
fig.savefig("led_layout_top.png", dpi=120, bbox_inches="tight"); plt.close(fig)
print("ok")
