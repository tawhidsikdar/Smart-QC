import numpy as np
def load(path):
    comps={}; cur=None
    for line in open(path):
        if line.startswith("COMP|"):
            _,name,arr=line.rstrip("\n").split("|",2)
            a=np.array([float(x) for x in arr.split(",")])
            cur=name; comps[cur]={"xf":a,"tris":[]}
        elif line.startswith("T|"):
            v=np.array([float(x) for x in line[2:].split(",")]).reshape(-1,3,3)
            comps[cur]["tris"].append(v)
    for k,c in comps.items():
        t=np.concatenate(c["tris"]) if c["tris"] else np.zeros((0,3,3))
        a=c["xf"]; R=a[:9].reshape(3,3); T=a[9:12]; s=a[12]
        # SolidWorks: p' = s * p @ R + T  (row-vector convention)
        c["world"]=(s*(t.reshape(-1,3)@R)+T).reshape(-1,3,3)*1000.0
    return comps
