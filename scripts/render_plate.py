#!/usr/bin/env python3
"""Render the Rosettes EVA-Placa plate from this dataset alone.

Usage:  python3 render_plate.py [--scan page.jpg] [--scale 2]
Background: --scan (your own copy of the Beinecke scan or a UV plate made with
gen_uv_plate.py) or plain black. Labels: black capsules + fonts/eva-placa.ttf
(gallows replaced by ductus-variant glyphs at PUA base+1/2/3), one colour per
ductus variant. Requires Pillow.
"""
import json, os, argparse, re, colorsys
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
ap=argparse.ArgumentParser(); ap.add_argument('--scan'); ap.add_argument('--scale',type=int,default=2)
A=ap.parse_args(); S=A.scale
PUA={'k':0xE010,'t':0xE020,'p':0xE030,'f':0xE040}
VC={'k-1':'#1aa850','k-2':'#fd7f26','k-3':'#15ada0','t-1':'#9b5cf6','t-2':'#c25a08','t-3':'#ec4899',
    'p-1':'#e63946','p-2':'#0b7a33','p-3':'#1e6ef0','f-1':'#c79102','f-2':'#0a8fe0','f-3':'#733d17'}
FAM={'k':'#63c374','t':'#d9a3ff','p':'#7fb2ff','f':'#e0b060'}
def hx(c): c=c.lstrip('#'); return tuple(int(c[i:i+2],16) for i in (0,2,4))
def punch(c):
    r,g,b=[v/255 for v in hx(c)]; h,l,s=colorsys.rgb_to_hls(r,g,b)
    r,g,b=colorsys.hls_to_rgb(h,l,min(1,s*1.45)); return tuple(int(v*255) for v in (r,g,b))
def light(rgb,f): return tuple(int(c+(255-c)*f) for c in rgb)
ov=json.load(open(os.path.join(HERE,"..","rosettes","overlay_f85v_86r.json")))
W,H=ov['imageWH']
base=(Image.open(A.scan).convert('RGB').resize((W*S,H*S),Image.LANCZOS)
      if A.scan else Image.new('RGB',(W*S,H*S),(10,10,12)))
FONT=os.path.join(HERE,"..","fonts","eva-placa.ttf")
def disp(tok,fam,var):
    s=tok.replace('?','*')
    if fam and var and '-' in var:
        n=int(var.split('-')[1]); i=s.find(fam)
        if n in(1,2,3) and i>=0: s=s[:i]+chr(PUA[fam]+n)+s[i+1:]
    return s
for t in ov['tokens']:
    tok=t.get('token') or ''
    if not tok: continue
    po=(ov.get('polys') or {}).get(str(t['p'])) or {}
    x=(t['x']+po.get('dx',0))*S; y=(t['y']+po.get('dy',0))*S
    fs=max(6,t.get('fs',12))*S
    fam,var=t.get('fam'),t.get('variant')
    text=disp(tok,fam,var)
    col=light(punch(VC[var]),0.35) if var in VC else (hx(FAM[fam]) if fam else (232,228,216))
    f=ImageFont.truetype(FONT,int(fs)); tw=f.getlength(text)
    capw=(t.get('mw') or 0)*S or tw+fs*0.5; caph=(t.get('mh') or 0)*S or fs*1.42
    while tw>capw*0.97 and fs>6:
        fs*=0.94; f=ImageFont.truetype(FONT,int(fs)); tw=f.getlength(text)
    pad=int(fs*0.6)
    tile=Image.new('RGBA',(int(max(capw,tw)+2*pad),int(caph+2*pad)),(0,0,0,0))
    d=ImageDraw.Draw(tile)
    d.rounded_rectangle([pad,pad,pad+capw,pad+caph],radius=caph/2,fill=(0,0,0,255))
    asc,desc=f.getmetrics()
    d.text((pad+(capw-tw)/2,pad+caph/2-(asc+desc)/2),text,font=f,fill=col)
    tile=tile.rotate(-t.get('angle',0),resample=Image.BICUBIC,expand=True)
    base.paste(tile,(int(x-tile.width/2),int(y-tile.height/2)),tile)
out=os.path.join(HERE,"plate_eva_placa.png"); base.save(out)
print("saved",out,base.size)
