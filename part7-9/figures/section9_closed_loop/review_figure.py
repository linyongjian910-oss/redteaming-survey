"""Inspect exported SVG geometry, including arrowheads and the shared 3-D origin.

This checks figure relationships independently of the generator's coordinates.
Visual inspection of the final PDF remains required.
"""
from pathlib import Path
import argparse
import math
import xml.etree.ElementTree as ET
from PIL import ImageFont

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('svg',nargs='?',type=Path,default=Path(__file__).resolve().parent/'closed_loop_research_agenda.svg')
SVG=parser.parse_args().svg
NS = {'s': 'http://www.w3.org/2000/svg'}
root = ET.parse(SVG).getroot()

def points(line):
    return [tuple(map(float,p.split(','))) for p in line.get('points').split()]

def segment_hits_rect(a,b,rect):
    x0,y0,x1,y1=rect
    lo,hi=0.,1.
    dx,dy=b[0]-a[0],b[1]-a[1]
    for p,q in [(-dx,a[0]-x0),(dx,x1-a[0]),(-dy,a[1]-y0),(dy,y1-a[1])]:
        if p==0:
            if q<0:return False
        elif p<0:lo=max(lo,q/p)
        else:hi=min(hi,q/p)
        if lo>hi:return False
    return True

def padded(rect,amount):
    a,b,c,d=rect
    return a-amount,b-amount,c+amount,d+amount

labels=[]
for t in root.findall('s:text',NS):
    if not t.text:continue
    size=int(t.get('font-size'))
    font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',size,index=int(t.get('font-weight')=='700'))
    left,top,right,bottom=font.getbbox(t.text,anchor='ls')
    x,y=float(t.get('x')),float(t.get('y'))
    width=font.getlength(t.text)
    if t.get('text-anchor')=='middle':x-=width/2
    elif t.get('text-anchor')=='end':x-=width
    labels.append((t.text,(x+left,y+top,x+right,y+bottom)))
for t in root.findall('s:svg[@data-kind="math"]',NS):
    x,y,w,h=map(float,[t.get(k) for k in ['x','y','width','height']])
    labels.append((t.get('aria-label'),(x,y,x+w,y+h)))

issues=[]
for line in root.findall('s:polyline',NS):
    ps=points(line)
    clearance=2+float(line.get('stroke-width','1'))/2
    for label,rect in labels:
        if any(segment_hits_rect(a,b,padded(rect,clearance)) for a,b in zip(ps,ps[1:])):
            issues.append(('line',label,line.get('data-role',line.get('stroke'))))
    marker_ref=line.get('marker-end')
    if not marker_ref:continue
    marker_id=marker_ref[5:-1]
    marker=root.find(f"s:defs/s:marker[@id='{marker_id}']",NS)
    if marker is None:raise ValueError(f'Missing arrowhead {marker_id}')
    width,height=map(float,[marker.get('markerWidth'),marker.get('markerHeight')])
    rx,ry=float(marker.get('refX')),float(marker.get('refY'))
    start,end=ps[-2:]
    distance=math.dist(start,end)
    ux,uy=(end[0]-start[0])/distance,(end[1]-start[1])/distance
    triangle=[(end[0]+ux*(x-rx)-uy*(y-ry),end[1]+uy*(x-rx)+ux*(y-ry)) for x,y in [(0,0),(width,height/2),(0,height)]]
    for label,rect in labels:
        if any(segment_hits_rect(a,b,padded(rect,2)) for a,b in zip(triangle,triangle[1:]+triangle[:1])):
            issues.append(('arrowhead',label,line.get('data-role',line.get('stroke'))))

roles={line.get('data-role'):points(line) for line in root.findall('s:polyline[@data-role]',NS)}
defense=roles['transfer-axis-defense']
runtime=roles['transfer-axis-runtime']
modality=roles['transfer-axis-modality']
vector=roles['transfer-vector']
origin=defense[0]
assert all(math.dist(origin,p[0])<.01 for p in [runtime,modality,vector]),'Transfer arrows do not share the origin'
assert defense[1][0]>origin[0] and defense[1][1]==origin[1]
assert runtime[1][1]<origin[1] and runtime[1][0]==origin[0]
depth=roles['transfer-depth-0']
dx,dy=depth[1][0]-depth[0][0],depth[1][1]-depth[0][1]
mx,my=modality[1][0]-origin[0],modality[1][1]-origin[1]
assert abs(dx*my-dy*mx)/(math.hypot(dx,dy)*math.hypot(mx,my))<.001,'Modality axis is not parallel to projected depth'
assert dx*mx+dy*my>0,'Modality axis points against depth'
assert vector[1][0]>origin[0] and vector[1][1]<origin[1]
visible=' '.join(label for label,_ in labels)
assert not any(s in visible for s in ['Evidence flow','Governed feedback','Judge A','Judge B','Judge C','FIREWALL'])
assert not issues,issues
print(f'PASS: {len(labels)} text/math bounds clear lines and arrowheads.')
print(f'PASS: D, E, M and transfer vector share origin {origin}; M follows projected depth.')
