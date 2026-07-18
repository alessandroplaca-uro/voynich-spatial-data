#!/usr/bin/env python3
"""Rebuild default token placements from the raw tracings - the exact pipeline
used to seed the published overlay (hand fine-tuning then adjusted x/y/angle/fs).

Input:  ../rosettes/gallows/f85v_86r_P*.json  (word vectors in crop frame)
        ../rosettes/polygons_f85v_86r.json    (region shapes)
Output: rebuilt_overlay_defaults.json         (same schema as the overlay)

Crop->folio mapping: folio = origin + crop/scale, where origin = region bbox
minus PAD(39px) and scale = 3600/(bbox_width + 2*PAD); ring regions use an
empirical fit (mean token radius / mean ring radius) when >=6 vectors exist.
Token orientation = atan2 of the traced word-baseline vector a->e.
"""
import json, glob, math, re, os
HERE=os.path.dirname(os.path.abspath(__file__))
ROS=os.path.join(HERE,"..","rosettes")
PAD=39.0
poly=json.load(open(os.path.join(ROS,"polygons_f85v_86r.json")))
W,H=poly['imageWH']; pgs={p['id']:p for p in poly['polygons']}
out_polys={}; out_tokens=[]
for f in sorted(glob.glob(os.path.join(ROS,"gallows","f85v_86r_P*.json")),
                key=lambda p:int(re.search(r'_P(\d+)',p).group(1))):
    d=json.load(open(f)); pid=d['paraNum']; pg=pgs.get(pid)
    if pg is None: continue
    tv=[t for t in d.get('tokenVecs',[]) if t.get('a') and t.get('e') and t.get('token')]
    pts=pg.get('points') or []
    if not pts and pg.get('shape')=='ring':
        pts=[[pg['cx']-pg['rxOuter'],pg['cy']-pg['ryOuter']],[pg['cx']+pg['rxOuter'],pg['cy']+pg['ryOuter']]]
    if not pts: continue
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    bx,by,bw=min(xs),min(ys),max(xs)-min(xs)
    s=3600.0/(bw+2*PAD)
    if pg.get('shape')=='ring' and len(tv)>=6:
        mids=[((t['a'][0]+t['e'][0])/2,(t['a'][1]+t['e'][1])/2) for t in tv]
        cx=sum(m[0] for m in mids)/len(mids); cy=sum(m[1] for m in mids)/len(mids)
        rc=sum(math.hypot(m[0]-cx,m[1]-cy) for m in mids)/len(mids)
        rx=((pg.get('rxOuter') or 0)+(pg.get('ryOuter') or 0)+
            (pg.get('rxInner') or pg.get('rxOuter') or 0)+(pg.get('ryInner') or pg.get('ryOuter') or 0))/4
        if rx>0 and rc>0: s=rc/rx
    ox,oy=bx-PAD,by-PAD
    out_polys[str(pid)]=dict(ox=round(ox,2),oy=round(oy,2),s=round(s,5),dx=0,dy=0)
    gvar={g.get('id'):(g.get('attribute') or [None])[0] for g in d.get('gallows',[])}
    for t in tv:
        a,e=t['a'],t['e']
        mx=ox+(a[0]+e[0])/2/s; my=oy+(a[1]+e[1])/2/s
        ang=math.degrees(math.atan2(e[1]-a[1],e[0]-a[0]))
        L=math.hypot(e[0]-a[0],e[1]-a[1])/s
        var=gvar.get(t.get('gallowId')) if t.get('source')=='gallow' else None
        out_tokens.append(dict(id=f"{pid}:{t.get('tokenIdx')}",p=pid,idx=t.get('tokenIdx'),
            token=t['token'],x=round(mx,1),y=round(my,1),angle=round(ang,1),
            fs=round(max(7,min(24,1.7*L/max(len(t['token']),1))),1),
            source=t.get('source'),variant=var,
            fam=var.split('-')[0] if var and '-' in var else None,len=round(L,1)))
json.dump(dict(folio="f85v_86r",imageWH=[W,H],version=3,polys=out_polys,tokens=out_tokens),
          open(os.path.join(HERE,"rebuilt_overlay_defaults.json"),'w'),indent=1)
print("rebuilt:",len(out_tokens),"tokens,",len(out_polys),"regions -> rebuilt_overlay_defaults.json")
