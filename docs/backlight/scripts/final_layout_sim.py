"""Uniformity check of the chosen layout: 8 rows of 60 LED/m strip in a 250 x 296 mm light box.
Run from this folder:  python final_layout_sim.py
Prints min/max over the camera window and the LED ripple at the centre, for several
LED-to-diffuser distances H and wall reflectances R (R=0 = black walls)."""
from backlight_sim import irradiance, stats

Lx, Lz = 250.0, 296.0          # light-box inner size (mm): along cloth travel x across cloth
win_cam = (190.0, 286.0)       # camera view along X x lit width minus 5 mm each side
print("Strip 60 LED/m (16.67 mm) along X, 8 rows across Z (37 mm), box 250 x 296; window 190 x 286")
for R in (0.0, 0.85, 0.95):
    for H in (25, 35, 45, 53.5, 65):
        gx, gz, E, n, pxe, pze = irradiance(H, 16.67, 37.0, Lx, Lz, R=R, res=2.0, nimg=2)
        u = stats(gx, gz, E, win_cam)
        uc = stats(gx, gz, E, (100, 100))
        print(f"R={R:4.2f} H={H:5.1f} nLED={n} P/H={pze/H:4.2f}  window min/max={u[0]*100:5.1f}%"
              f"  centre ripple +-{uc[1]*100:5.2f}%", flush=True)
