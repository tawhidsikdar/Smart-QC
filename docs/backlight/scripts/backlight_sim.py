"""Irradiance on the diffuser plane from a grid of Lambertian LEDs inside a box.
Walls modelled as specular mirrors (method of images) with reflectance R.
Box inner footprint W (Z, across cloth) x Lx (X, along travel)."""
import numpy as np
def grid(L, p):
    n = int(round(L / p)); p_eff = L / n
    return (np.arange(n) + 0.5) * p_eff - L / 2, p_eff   # edge LED at p/2 from wall
def irradiance(H, px, pz, Lx, Lz, R=0.0, m=1.0, nimg=6, res=1.0, win=None):
    xs, pxe = grid(Lx, px); zs, pze = grid(Lz, pz)
    X, Z = np.meshgrid(xs, zs); led = np.c_[X.ravel(), Z.ravel()]
    # image sources: reflect across walls x=+-Lx/2, z=+-Lz/2
    srcs, wts = [], []
    for i in range(-nimg, nimg + 1):
        for j in range(-nimg, nimg + 1):
            sx = (-1) ** i; sz = (-1) ** j
            xo = i * Lx; zo = j * Lz
            pts = np.c_[sx * led[:, 0] + xo, sz * led[:, 1] + zo]
            srcs.append(pts); wts.append(np.full(len(pts), R ** (abs(i) + abs(j))))
    S = np.vstack(srcs); Wt = np.concatenate(wts)
    keep = Wt > 1e-4; S = S[keep]; Wt = Wt[keep]
    gx = np.arange(-Lx / 2, Lx / 2 + 1e-9, res); gz = np.arange(-Lz / 2, Lz / 2 + 1e-9, res)
    GX, GZ = np.meshgrid(gx, gz)
    E = np.zeros_like(GX)
    for k in range(0, len(S), 200):
        s = S[k:k + 200]; w = Wt[k:k + 200]
        dx = GX[..., None] - s[:, 0]; dz = GZ[..., None] - s[:, 1]
        r2 = dx * dx + dz * dz + H * H
        E += (w * H ** (m + 1) / r2 ** ((m + 3) / 2)).sum(-1)
    return gx, gz, E, len(led), pxe, pze
def stats(gx, gz, E, win):
    wx, wz = win
    m = (np.abs(gx)[None, :] <= wx / 2) & (np.abs(gz)[:, None] <= wz / 2)
    v = E[m]; return v.min() / v.max(), (v.max() - v.min()) / (v.max() + v.min())
if __name__ == "__main__":
    Lx, Lz = 250.0, 309.0          # light-box inner footprint (mm): floor length x unobstructed width
    win = (230.0, 290.0)            # region that matters: camera view along X ~ 190-215, cloth window 290
    print(f"Box {Lx}x{Lz} mm, evaluation window {win[0]}x{win[1]} mm, Lambertian LEDs (2835, 120 deg)")
    print(f"{'config':38s} {'H':>4s} {'nLED':>5s} {'P/H':>5s} | {'black walls':>18s} | {'white/mirror walls R=0.9':>26s}")
    configs = [("strip 60/m, rows 30.9 mm", 16.67, 30.9), ("strip 60/m, rows 38.6 mm", 16.67, 38.6),
               ("PCB grid 25 x 25.75", 25.0, 25.75), ("PCB grid 31.25 x 30.9", 31.25, 30.9),
               ("PCB grid 41.7 x 44.1", 41.7, 44.1), ("PCB grid 50 x 51.5", 50.0, 51.5)]
    for H in (20.0, 30.0, 40.0, 53.5, 70.0):
        for name, px, pz in configs:
            gx, gz, E0, n, pxe, pze = irradiance(H, px, pz, Lx, Lz, R=0.0, res=2.0)
            u0 = stats(gx, gz, E0, win)
            gx, gz, E1, n, pxe, pze = irradiance(H, px, pz, Lx, Lz, R=0.9, res=2.0)
            u1 = stats(gx, gz, E1, win)
            print(f"{name:38s} {H:4.0f} {n:5d} {max(pxe,pze)/H:5.2f} | min/max {u0[0]*100:5.1f}%       | min/max {u1[0]*100:5.1f}%  ripple +-{u1[1]*100:4.1f}%")
        print()
