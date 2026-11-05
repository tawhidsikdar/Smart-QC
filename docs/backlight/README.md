# Backlight (transmitted light) for fabric inspection

Design work from 2026-11-05 for the light under the booth floor. The camera (C920) looks down
through the cloth, like an X-ray. Dimensions come from `ASSEMBLY_main.SLDASM`
(Aluminium_ver). In the assembly, Y is up, X is the direction the cloth travels and Z is across the cloth.

## Design summary

| Item | Choice |
| --- | --- |
| Diffuser | 5 mm opal (milky white) acrylic, 250 x 340 mm. Same size as the clear floor, so no CAD change. Do not use white paint or paper: the camera keeps the floor in sharp focus, so their texture would look like defects. |
| LED to diffuser | 53.5 mm (LED face to floor underside). 45-65 mm works, below ~40 mm LED spots show. |
| LEDs | 12 V SMD 2835 LED strip, 60 LEDs/m, 5000-6500 K, CRI >= 80, IP20 (no coating), all from one reel |
| Layout | 8 rows x 15 LEDs = 120 LEDs (2.0 m). 16.7 mm along a row, 37 mm between rows, outer rows 18.5 mm from the walls. Rows run along the cloth travel (250 mm = 5 strip segments). |
| Light box | White inside. Inner size 250 x 296 mm, 54.5 mm tall. 2 mm aluminium base plate bolted under both 2040 rails (bottom T-slot, M5 T-nuts). Wall outer faces inside Z -86.6 / 213.4 to clear the holder legs. |
| Booth walls | Matte black on the inside face, plus a black lid with a camera hole |
| Cloth width | 320 mm. Covers the 296 mm lit width, edges rest on the holder ledges. Print holders in black, blacken the opal sheet's edges. |
| Power | Separate regulated 12 V supply (5 A), ESP32 switches it on/off with a logic-level MOSFET. No PWM dimming (dark bands in the image); set brightness with camera exposure. |

Brightness and exposure numbers are estimates. Test a sample of opal sheet and your real cloth before the final build.

## Files

| File | What it is |
| --- | --- |
| `figures/backlight_section.png` | Section through the booth centre: real CAD (lines) + proposed backlight (filled) |
| `figures/led_layout_top.png` | Top view of the LED rows inside the light box |
| `figures/sec_Z63_XY.png` | CAD section along the cloth path (Z = 63.4) |
| `figures/sec_Z-100_XY.png` | CAD section through the enclosure holder (Z = -100) |
| `figures/sec_X-56_ZY.png`, `figures/sec_X-56_ZY_zoom.png` | CAD section across the booth centre (X = -56.4) |
| `sim_results.txt` | Uniformity simulation results (layout comparison + chosen layout) |
| `scripts/export_tess.ps1` | Exports the open SolidWorks assembly to `tess.txt` (read-only) |
| `scripts/tess_load.py` | Loads `tess.txt` and places every part in assembly coordinates |
| `scripts/section.py` | Makes the `sec_*.png` CAD sections |
| `scripts/figure.py` | Makes `backlight_section.png` and `led_layout_top.png` |
| `scripts/backlight_sim.py` | LED uniformity simulation (run it to print table 1 in `sim_results.txt`) |
| `scripts/final_layout_sim.py` | Simulation of the chosen layout (table 2) |
| `scripts/step_bbox.py` | Lists part sizes/positions from a STEP file (used on `CAD of smartqc_rig (initial).step`) |

## Re-making the figures

`tess.txt` (about 30 MB) is not in Git: big files go to Google Drive. To make it again, open
`ASSEMBLY_main` in SolidWorks, then in `scripts/`:

```
powershell -ExecutionPolicy Bypass -File export_tess.ps1 -OutFile tess.txt
python section.py
python figure.py
```

The PNGs are written to `scripts/`. Copy them to `figures/`. The simulations do not need `tess.txt`:

```
python final_layout_sim.py
```

Tested with Python 3.7, numpy 1.21, matplotlib 3.5. Not yet tested in the `smartqc` environment
(Python 3.11), and matplotlib is not in `environment.yml`.
