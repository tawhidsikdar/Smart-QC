import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from tess_load import load
C=load("tess.txt")
def section(tris, axis, val):
    d=tris[:,:,axis]-val
    segs=[]
    s=np.sign(d)
    for t,dd in zip(tris,d):
        pts=[]
        for i in range(3):
            j=(i+1)%3
            if (dd[i]<0)!=(dd[j]<0):
                a=dd[i]/(dd[i]-dd[j]); pts.append(t[i]+a*(t[j]-t[i]))
        if len(pts)==2: segs.append(pts)
    return np.array(segs)
def colour(n):
    if "acrylic" in n: return "tab:cyan"
    if "enclosure" in n: return "tab:green"
    if "shaft" in n: return "tab:red"
    if "KFL" in n: return "tab:purple"
    if "bracket" in n: return "tab:orange"
    return "0.4"
def plot(axis,val,h,v,fn,xlim,ylim,title):
    fig,ax=plt.subplots(figsize=(14,9))
    for n,c in C.items():
        w=c["world"]
        m=(w[:,:,axis].min(1)<=val)&(w[:,:,axis].max(1)>=val)
        if not m.any(): continue
        s=section(w[m],axis,val)
        if len(s)==0: continue
        ax.add_collection(LineCollection(s[:,:,[h,v]],colors=colour(n),linewidths=1))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.grid(True,alpha=.3)
    ax.set_title(title); ax.set_xlabel("XYZ"[h]+" (mm)"); ax.set_ylabel("XYZ"[v]+" (mm)")
    ax.minorticks_on(); ax.grid(True,which="minor",alpha=.1)
    fig.savefig(fn,dpi=110,bbox_inches="tight"); plt.close(fig)
plot(2,63.4,0,1,"sec_Z63_XY.png",(-420,300),(-180,460),"Section at Z=63.4 (machine centre, cloth path) - X along travel, Y up")
plot(0,-56.4,2,1,"sec_X-56_ZY.png",(-160,290),(-180,460),"Section at X=-56.4 (booth centre) - Z across, Y up")
plot(2,-100,0,1,"sec_Z-100_XY.png",(-220,100),(20,240),"Section at Z=-100 (through enclosure_holder-1)")
plot(0,-56.4,2,1,"sec_X-56_ZY_zoom.png",(-160,290),(20,240),"Section at X=-56.4 zoom")
