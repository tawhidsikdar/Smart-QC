"""Minimal STEP AP214 reader: per-product bounding boxes in assembly coordinates."""
import re, sys
import numpy as np

path = sys.argv[1]
txt = open(path, encoding="latin-1").read()
data = txt.split("DATA;",1)[1]
ents = {}
for m in re.finditer(r"#(\d+)\s*=\s*(.*?);\s*(?=#\d+\s*=|ENDSEC)", data, re.S):
    ents[int(m.group(1))] = " ".join(m.group(2).split())

def refs(s): return [int(x) for x in re.findall(r"#(\d+)", s)]
def typ(s): return s.split("(",1)[0].strip()

pts = {}
for k,v in ents.items():
    if v.startswith("CARTESIAN_POINT"):
        nums = re.findall(r"[-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?", v.split("(",2)[2])
        pts[k] = np.array([float(x) for x in nums[:3]])
def direction(k):
    v = ents[k]; nums = re.findall(r"[-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?", v.split("(",2)[2]); a=np.array([float(x) for x in nums[:3]]); return a/np.linalg.norm(a)
def axis2(k):
    r = refs(ents[k]); o = pts[r[0]]
    z = direction(r[1]) if len(r)>1 else np.array([0,0,1.])
    x = direction(r[2]) if len(r)>2 else np.array([1,0,0.])
    x = x - z*np.dot(x,z); x/=np.linalg.norm(x); y=np.cross(z,x)
    T=np.eye(4); T[:3,0]=x;T[:3,1]=y;T[:3,2]=z;T[:3,3]=o; return T

# collect all points reachable from each shape representation (geometry)
import functools
sys.setrecursionlimit(100000)
reach_cache={}
def collect(k, seen):
    stack=[k]; out=[]
    while stack:
        n=stack.pop()
        if n in seen: continue
        seen.add(n)
        v=ents.get(n,"")
        t=typ(v)
        if t=="CARTESIAN_POINT":
            if len(pts[n])==3: out.append(pts[n])
            continue
        if t in ("AXIS2_PLACEMENT_3D","DIRECTION","GEOMETRIC_REPRESENTATION_CONTEXT") or v.startswith("("): 
            if t=="AXIS2_PLACEMENT_3D" : continue
            if v.startswith("("): continue
        stack.extend(refs(v))
    return out

# product -> product_definition
pd_of_prod={}
name_of_pd={}
for k,v in ents.items():
    if v.startswith("PRODUCT_DEFINITION("):
        form=refs(v)[0]; prod=refs(ents[form])[0]
        nm=re.match(r"PRODUCT\('([^']*)'",ents[prod]).group(1)
        name_of_pd[k]=nm
# product_definition_shape -> pd ; SDR -> shape rep
shape_of_pd={}
for k,v in ents.items():
    if v.startswith("SHAPE_DEFINITION_REPRESENTATION"):
        pds,rep=refs(v)[:2]
        r=refs(ents[pds])
        if r and r[0] in name_of_pd: shape_of_pd[r[0]]=rep
# SHAPE_REPRESENTATION_RELATIONSHIP to link to brep reps
srr={}
for k,v in ents.items():
    if "SHAPE_REPRESENTATION_RELATIONSHIP" in v and "REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION" not in v:
        r=refs(v); srr.setdefault(r[0],[]).append(r[1]); srr.setdefault(r[1],[]).append(r[0])
# NAUO: parent pd, child pd
children={}
for k,v in ents.items():
    if v.startswith("NEXT_ASSEMBLY_USAGE_OCCURRENCE"):
        r=refs(v); children.setdefault(r[0],[]).append((k,r[1]))
# transforms: CONTEXT_DEPENDENT_SHAPE_REPRESENTATION(rrwt, pds(nauo))
trans_of_nauo={}
for k,v in ents.items():
    if v.startswith("CONTEXT_DEPENDENT_SHAPE_REPRESENTATION"):
        rr,pds=refs(v)[:2]
        nauo=refs(ents[pds])[0]
        rv=ents[rr]
        m=re.search(r"REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION\(\s*#(\d+)",rv)
        idt=ents[int(m.group(1))]
        a,b=refs(idt)[:2]
        trans_of_nauo[nauo]=(a,b)
def geom_points(pd):
    rep=shape_of_pd.get(pd)
    if rep is None: return []
    reps=[rep]+srr.get(rep,[])
    allp=[]
    for r in reps:
        items=refs(ents[r])
        for it in items:
            if typ(ents[it])=="AXIS2_PLACEMENT_3D": continue
            if typ(ents[it]).startswith("GEOMETRIC_REPRESENTATION_CONTEXT") or ents[it].startswith("("): continue
            allp+=collect(it,set())
    return allp
results=[]
def walk(pd,T,depth):
    p=geom_points(pd)
    if p:
        P=np.array(p); P=(T[:3,:3]@P.T).T+T[:3,3]
        results.append((depth,name_of_pd[pd],P.min(0),P.max(0)))
    else:
        results.append((depth,name_of_pd[pd],None,None))
    for nauo,ch in children.get(pd,[]):
        a,b=trans_of_nauo.get(nauo,(None,None))
        if a is None: M=np.eye(4)
        else: M=axis2(b)@np.linalg.inv(axis2(a))
        walk(ch,T@M,depth+1)
roots=[pd for pd in name_of_pd if not any(pd==c for v in children.values() for _,c in v)]
for r in roots: walk(r,np.eye(4),0)
for d,n,lo,hi in results:
    if lo is None: print("  "*d+n); continue
    sz=hi-lo
    print(f"{'  '*d}{n:45s} min({lo[0]:8.1f},{lo[1]:8.1f},{lo[2]:8.1f}) max({hi[0]:8.1f},{hi[1]:8.1f},{hi[2]:8.1f}) size({sz[0]:7.1f},{sz[1]:7.1f},{sz[2]:7.1f})")
