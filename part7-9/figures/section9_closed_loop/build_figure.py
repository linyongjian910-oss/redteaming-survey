"""Editable scientific illustration. Standard-library SVG and draw.io authoring.

Run with Python 3; export SVG with rsvg-convert for PNG and PDF.
All coordinates are in a 2560 x 1810 design space.
"""
from pathlib import Path
import argparse
import base64
import html
import math
import xml.etree.ElementTree as ET
from math_renderer import render_math
try:
    from PIL import ImageFont
except ImportError:
    ImageFont = None

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--hub-style',choices=['ellipse','band','chamfer','loop','rounded'],default='rounded')
parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
args=parser.parse_args()
OUT=args.output_dir.resolve()
OUT.mkdir(parents=True,exist_ok=True)
W, H = 2560, 1810
INK, MUTED, LINE = '#203349', '#53677C', '#B8C6D4'
BLUE, RED, PURPLE = '#247CB5', '#C34F61', '#8760A7'
GREEN, AMBER = '#348368', '#AF802A'
svg = []
root = ET.Element('mxfile', host='app.diagrams.net', version='26.0.0')
diagram = ET.SubElement(root, 'diagram', id='closed-loop-assurance', name='Closed-loop research agenda')
model = ET.SubElement(diagram, 'mxGraphModel', dx=str(W), dy=str(H), grid='1', gridSize='10', page='1', pageWidth=str(W), pageHeight=str(H), background='#FFFFFF')
cells = ET.SubElement(model, 'root')
ET.SubElement(cells, 'mxCell', id='0')
ET.SubElement(cells, 'mxCell', id='1', parent='0')
counter = 0
group = '1'
offset = (0, 0)

def cell(style, x, y, w, h, value='', ident=None):
    global counter
    counter += 1
    ident = ident or f'element-{counter:03d}'
    c = ET.SubElement(cells, 'mxCell', id=ident, value=value, style=style, vertex='1', parent=group)
    ET.SubElement(c, 'mxGeometry', x=str(x-offset[0]), y=str(y-offset[1]), width=str(w), height=str(h), **{'as':'geometry'})
    return ident

def box(x,y,w,h,fill='#FFFFFF',stroke=LINE,r=12,sw=2,ident=None,container=False):
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    return cell(f'rounded={int(bool(r))};absoluteArcSize=1;arcSize={r*2};html=1;fillColor={fill};strokeColor={stroke};strokeWidth={sw};'+('container=1;pointerEvents=0;' if container else ''),x,y,w,h,ident=ident)

def oval(x,y,w,h,fill='#FFFFFF',stroke=LINE,sw=2):
    svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    cell(f'ellipse;html=1;fillColor={fill};strokeColor={stroke};strokeWidth={sw};',x,y,w,h)

def text(x,y,s,size=25,color=INK,bold=False,align='left',width=None,font='Helvetica',rotate=0):
    # y is baseline, shared between SVG and the native draw.io text cell.
    anchor = {'left':'start','center':'middle','right':'end'}[align]
    transform = f' transform="rotate({rotate} {x} {y})"' if rotate else ''
    svg.append(f'<text x="{x}" y="{y}" font-family="{font},Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" text-anchor="{anchor}"{transform}>{html.escape(s)}</text>')
    if width is None and ImageFont and font=='Helvetica':
        width = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',size,index=int(bold)).getlength(s)+10
    width = width or max(40, len(s)*size*.57+12)
    xx = x if align=='left' else x-width/2 if align=='center' else x-width
    cell(f'text;html=1;whiteSpace=nowrap;overflow=visible;align={align};verticalAlign=middle;spacing=0;fontFamily={font};fontSize={size};fontColor={color};fontStyle={int(bold)};rotation={rotate};',xx,y-size*.88,width,size*1.22,html.escape(s))

def vector_asset(source,x,y,w,h,description='',math_asset=False):
    node=ET.fromstring(source)
    # Each placement has its own glyph IDs, including repeated math symbols.
    prefix=f'asset-{counter+1}-'
    ids={n.get('id'):prefix+n.get('id') for n in node.iter() if n.get('id')}
    for n in node.iter():
        for k,v in list(n.attrib.items()):
            if k=='id': n.set(k,ids[v])
            elif v.startswith('#') and v[1:] in ids: n.set(k,'#'+ids[v[1:]])
            elif 'url(#' in v:
                for before,after in ids.items(): v=v.replace(f'url(#{before})',f'url(#{after})')
                n.set(k,v)
    standalone=ET.tostring(node,encoding='utf-8')
    encoded=base64.b64encode(standalone).decode()
    native_id=cell(f'shape=image;html=1;aspect=fixed;imageAspect=0;image=data:image/svg+xml,{encoded};',x,y,w,h)
    native=cells.find(f"mxCell[@id='{native_id}']")
    native.set('data-source',description)
    native.set('data-kind','math' if math_asset else 'icon')
    node.set('x',str(x));node.set('y',str(y));node.set('width',str(w));node.set('height',str(h))
    node.set('aria-label',description)
    node.set('data-kind','math' if math_asset else 'icon')
    svg.append(ET.tostring(node,encoding='unicode'))

def math_text(x,y,expression,size=27,color=INK,bold=False,align='left'):
    source,ww,hh,dd=render_math(expression,bold)
    scale=size/10
    w,h=ww*scale,(hh+dd)*scale
    node=ET.fromstring(source);node.set('fill',color)
    xx=x if align=='left' else x-w/2 if align=='center' else x-w
    vector_asset(ET.tostring(node,encoding='unicode'),xx,y-hh*scale,w,h,expression,math_asset=True)
    return w

def label_math(x,y,label,expression,size=24,color=INK,bold=True,align='left',suffix=''):
    f=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',size,index=int(bold)) if ImageFont else None
    label_width=f.getlength(label) if f else len(label)*size*.54
    suffix_width=f.getlength(suffix) if f else len(suffix)*size*.54
    _,ww,_,_=render_math(expression,bold)
    width=label_width+8+ww*size/10+(8+suffix_width if suffix else 0)
    start=x if align=='left' else x-width/2 if align=='center' else x-width
    text(start,y,label,size,color,bold)
    formula_end=start+label_width+8+math_text(start+label_width+8,y,expression,size,color,bold)
    if suffix: text(formula_end+8,y,suffix,size,color,bold)

def path(points,color=LINE,sw=2.5,dash=False,arrow=False,arrow_size=None,role=None):
    p = ' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
    marker_name='red' if color==RED else 'blue' if color==BLUE else 'green' if color==GREEN else 'gray'
    if arrow_size: marker_name+='-large'
    marker = f' marker-end="url(#{marker_name})"' if arrow else ''
    semantic = f' data-role="{role}"' if role else ''
    svg.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'+(' stroke-dasharray="10 8"' if dash else '')+marker+semantic+'/>')
    global counter
    counter += 1
    c=ET.SubElement(cells,'mxCell',id=f'edge-{counter:03d}',value='',edge='1',parent=group,style=f'edgeStyle=none;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={color};strokeWidth={sw};endArrow={"blockThin" if arrow else "none"};endFill=1;endSize={arrow_size or 10};'+('dashed=1;dashPattern=5 4;' if dash else ''))
    if role: c.set('data-role',role)
    g=ET.SubElement(c,'mxGeometry',relative='1',**{'as':'geometry'})
    ET.SubElement(g,'mxPoint',x=str(points[0][0]-offset[0]),y=str(points[0][1]-offset[1]),**{'as':'sourcePoint'})
    ET.SubElement(g,'mxPoint',x=str(points[-1][0]-offset[0]),y=str(points[-1][1]-offset[1]),**{'as':'targetPoint'})
    if len(points)>2:
        a=ET.SubElement(g,'Array',**{'as':'points'})
        for x,y in points[1:-1]: ET.SubElement(a,'mxPoint',x=str(x-offset[0]),y=str(y-offset[1]))

def line(x1,y1,x2,y2,**kw): path([(x1,y1),(x2,y2)],**kw)

def rounded_path(points,radius=18,**kw):
    """Round routing corners while preserving the explicit obstacle-free lanes."""
    rounded=[points[0]]
    for previous,corner,following in zip(points,points[1:],points[2:]):
        before=math.dist(previous,corner);after=math.dist(corner,following)
        r=min(radius,before/2,after/2)
        a=tuple(corner[k]+(previous[k]-corner[k])*r/before for k in (0,1))
        b=tuple(corner[k]+(following[k]-corner[k])*r/after for k in (0,1))
        rounded.append(a)
        for i in range(1,9):
            t=i/8;u=1-t
            rounded.append(tuple(u*u*a[k]+2*u*t*corner[k]+t*t*b[k] for k in (0,1)))
    rounded.append(points[-1])
    path(rounded,**kw)

def bezier(a,b,c,d,n=50,**kw):
    points=[]
    for i in range(n+1):
        t=i/n; u=1-t
        points.append((u**3*a[0]+3*u*u*t*b[0]+3*u*t*t*c[0]+t**3*d[0],u**3*a[1]+3*u*u*t*b[1]+3*u*t*t*c[1]+t**3*d[1]))
    path(points,**kw)

def panel(x,y,title,sec,tag,tint,accent,ident):
    global group,offset
    group='1'; offset=(0,0)
    panel_id=box(x,y,720,580,stroke=accent,sw=1.8,r=18,ident=ident,container=True)
    group=panel_id;offset=(x,y)
    box(x+2,y+2,716,96,fill=tint,stroke='none',r=16,sw=0)
    # White lower edge makes the header band square at its foot.
    box(x+2,y+80,716,20,fill=tint,stroke='none',r=0,sw=0)
    text(x+26,y+45,title,32,bold=True)
    text(x+26,y+79,tag,22,color=MUTED)
    text(x+692,y+43,sec,25,color=accent,bold=True,align='right')
    line(x+26,y+462,x+694,y+462,color=LINE,sw=1.2)

def notes(x,y,l1,l2,anchor):
    text(x+26,y+499,l1,23)
    text(x+26,y+531,l2,23)
    text(x+26,y+562,anchor,22,color=MUTED)

# Shared title and runtime connectors.
text(100,69,'Closed-Loop Research Agenda for Automated Red Teaming',45,bold=True)
text(100,111,'Six open frontiers connect failure discovery to reproducible safety evidence and governed remediation.',27,color=MUTED)

for x,label,y in [(820,'Probes',435),(1640,'Verdicts',435),(820,'Vectors',1320),(1640,'Traces',1320)]:
    line(x+4,y,x+94,y,color=MUTED,sw=3,arrow=True)
    text(x+50,y-22,label,22,bold=True,align='center')

# Solid gray-blue coordinator links remain visible at paper scale.
hub_routes={
    'ellipse': [[(460,740),(460,800),(970,853)],[(1280,740),(1280,790)],[(2100,740),(2100,800),(1590,853)],[(460,1040),(460,980),(970,927)],[(1280,1040),(1280,990)],[(2100,1040),(2100,980),(1590,927)]],
    'band': [[(460,740),(460,780),(980,780),(980,816)],[(1280,740),(1280,816)],[(2100,740),(2100,780),(1580,780),(1580,816)],[(460,1040),(460,1000),(980,1000),(980,964)],[(1280,1040),(1280,964)],[(2100,1040),(2100,1000),(1580,1000),(1580,964)]],
    'chamfer': [[(460,740),(460,790),(850,850)],[(1280,740),(1280,785)],[(2100,740),(2100,790),(1710,850)],[(460,1040),(460,990),(850,930)],[(1280,1040),(1280,995)],[(2100,1040),(2100,990),(1710,930)]],
    'loop': [[(460,740),(460,770),(980,770),(980,790)],[(1280,740),(1280,790)],[(2100,740),(2100,770),(1580,770),(1580,790)],[(460,1040),(460,1010),(980,1010),(980,990)],[(1280,1040),(1280,990)],[(2100,1040),(2100,1010),(1580,1010),(1580,990)]]
}
hub_routes['rounded']=hub_routes['loop']
for i,points in enumerate(hub_routes[args.hub_style]):
    path(points,color='#69849C',sw=3.2,role=f'coordinator-spoke-{i}')

# 1. Discovery engine.
x,y=100,160
panel(x,y,'Discovery Engine','§9.1','Adaptive search estimates mechanism coverage.','#E0F2FE',BLUE,'discovery')
label_math(x+40,y+142,'Harms',r'S(N)',24)
line(x+86,y+385,x+86,y+174,color=MUTED,sw=2,arrow=True)
line(x+86,y+385,x+657,y+385,color=MUTED,sw=2,arrow=True)
for yy in [y+290]: line(x+87,yy,x+648,yy,color='#E7EDF3',sw=1)
line(x+88,y+298,x+648,y+298,color=RED,dash=True,sw=3)
text(x+397,y+331,'Static discovery saturates.',24,color=RED)
bezier((x+88,y+377),(x+250,y+265),(x+370,y+211),(x+648,y+208),color=BLUE,sw=4)
# Direct annotation in the empty upper-left plot region; no legend swatch.
label_math(x+130,y+228,'Adaptive tail',r'S_0',25,color=BLUE)
line(x+414,y+201,x+652,y+201,color=BLUE,dash=True,sw=1.5)
label_math(x+370,y+428,'Query Budget',r'N',24,bold=False,align='center')
text(x+106,y+171,'Chao1 lower bound',24,color=BLUE,bold=True)
math_text(x+375,y+170,r'S_0 = S_{\mathrm{obs}} + \frac{f_1^2}{2f_2}',25)
notes(x,y,'Quality-diversity search clusters failure mechanisms.','Singleton and doubleton counts estimate unseen risk.','Coverage anchors include HarmBench and JailbreakBench.')

# 2. Decision oracles.
x,y=920,160
panel(x,y,'Decision Oracles','§9.2','Search and reporting use separate judgments.','#F3E8FF',PURPLE,'oracles')
box(x+24,y+142,222,92,fill='#F4F9FD',stroke='#BCD5E7')
text(x+135,y+181,'Attack Optimizer',24,bold=True,align='center')
text(x+135,y+214,'Search uses feedback.',20,color=MUTED,align='center')
box(x+24,y+300,222,96,fill='#E0F2FE',stroke=BLUE)
label_math(x+135,y+339,'Search Judge',r'J_s',24,align='center')
text(x+135,y+374,'Scores guide search.',20,align='center')
line(x+82,y+237,x+82,y+296,color=BLUE,arrow=True)
line(x+189,y+298,x+189,y+239,color=BLUE,arrow=True)
# A flat brick-wall symbol replaces the firewall text and dashed divider.
wall_width,wall_height=48,240
wall_parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 240">']
wall_parts.append('<rect x="0.8" y="0.8" width="46.4" height="238.4" rx="2" fill="#FFE4E6" stroke="#C34F61" stroke-width="1.6"/>')
for row in range(20):
    breaks=[0,24,48] if row%2==0 else [0,12,36,48]
    for left,right in zip(breaks,breaks[1:]):
        wall_parts.append(f'<rect x="{left+1.5}" y="{row*12+1.5}" width="{right-left-3}" height="9" rx="0.7" fill="#D794A0"/>')
wall_parts.append('</svg>')
wall_source=''.join(wall_parts)
(OUT/'assets').mkdir(exist_ok=True)
(OUT/'assets'/'brick_wall.svg').write_text(wall_source)
vector_asset(wall_source,x+295,y+156,wall_width,wall_height,'Brick-wall isolation boundary')
oracle_route=[(x+250,y+214),(x+273,y+214),(x+273,y+255),(x+366,y+255)]
# The white underlay creates a clear passage through the brick pattern.
path(oracle_route,color='#FFFFFF',sw=11)
path(oracle_route,color=BLUE,sw=3.8,arrow=True,arrow_size=18)
label_math(x+367,y+178,'Reporting Oracle Panel',r'J_r',24)
for yy,hdr,sub in [(240,'Classifiers assess safety.','LlamaGuard · WildGuard'),(300,'Assertions check compliance.','Rules and regular expressions'),(360,'Experts resolve disagreements.','Human review')]:
    box(x+370,y+yy-14,324,58,fill='#FAF7FD',stroke='#DBCCE8',r=8,sw=1.2)
    text(x+382,y+yy+8,hdr,20,bold=True)
    text(x+382,y+yy+31,sub,20)
box(x+24,y+412,670,38,fill='#F3E8FF',stroke=PURPLE,r=6,sw=1.8)
text(x+359,y+439,'Calibration sets the decision boundary τ.',24,color=PURPLE,bold=True,align='center')
notes(x,y,'The search judge guides the optimizer.','Independent oracles arbitrate reported verdicts.','CoinFlip probes evaluator reliability.')

# 3. Remediation and retention.
x,y=1740,160
panel(x,y,'Remediation & Retention','§9.5','Four factors separate sources of score changes.','#DCFCE7',GREEN,'remediation')
for xx,yy,hdr,var,sub in [(26,146,'Target','m','Weights and PEFT'),(194,146,'Attacker','a','Mutations'),(26,258,'Judge','j','Rubrics'),(194,258,'Protocol','p','Budget and rules')]:
    box(x+xx,y+yy,154,90,fill='#F3FBF6',stroke='#A3CCB6',r=9)
    label_math(x+xx+77,y+yy+35,hdr,var,24,align='center')
    text(x+xx+77,y+yy+67,sub,18,align='center')
line(x+354,y+250,x+393,y+250,color=GREEN,arrow=True)
box(x+405,y+140,288,217,fill='#FFFFFF',stroke=GREEN,r=10)
text(x+549,y+174,'Regression Replay',25,bold=True,align='center')
text(x+549,y+205,'Suite',25,bold=True,align='center')
for i in range(3):
    yy=y+222+i*31
    box(x+425,yy,16,16,fill='#DCFCE7',stroke=GREEN,r=2,sw=1)
    path([(x+428,yy+8),(x+432,yy+12),(x+438,yy+4)],color=GREEN,sw=1.6)
text(x+453,y+238,'Versions are recorded.',20)
text(x+453,y+269,'Traces are replayed.',20)
text(x+453,y+300,'Drift is measured.',20)
text(x+549,y+337,'Utility Guard',24,color=GREEN,bold=True,align='center')
text(x+26,y+394,'Benign MMLU tasks probe over-refusal.',24)
box(x+26,y+411,668,39,fill='#DCFCE7',stroke=GREEN,r=6)
label_math(x+360,y+440,'Invariant:',r'\delta_{\mathrm{drift}} < \epsilon',28,color=GREEN,align='center')
notes(x,y,'Remediation uses DPO, Safe-RLHF and unlearning.','Factor-wise comparisons retain versioned evidence.','BeaverTails and OR-Bench anchor evaluation.')

# 4. Threat transfer: 3-D wireframe slices expose the fourth attack axis.
x,y=100,1040
panel(x,y,'Threat Transfer','§9.4','Transfer varies across four threat-space axes.','#FEF3C7',AMBER,'transfer')
label_math(x+360,y+144,'Threat Space:',r'\mathcal{S} = \mathcal{A} \times \mathcal{M} \times \mathcal{D} \times \mathcal{E}',27,align='center')
front=[(x+154,y+260),(x+398,y+260),(x+398,y+391),(x+154,y+391)]
back=[(xx+92,yy-70) for xx,yy in front]
path(front+[front[0]],color=AMBER,sw=2)
path(back+[back[0]],color=AMBER,sw=2)
for i,(a,b) in enumerate(zip(front,back)): path([a,b],color=AMBER,sw=2,role=f'transfer-depth-{i}')
for k in [1/3,2/3]:
    dx,dy=92*k,-70*k
    path([(xx+dx,yy+dy) for xx,yy in front]+[(front[0][0]+dx,front[0][1]+dy)],color='#DCC690',sw=1.4)
origin=(x+154,y+391)
path([origin,(x+590,y+391)],color=MUTED,arrow=True,sw=2,role='transfer-axis-defense')
path([origin,(x+154,y+197)],color=MUTED,arrow=True,sw=2,role='transfer-axis-runtime')
# The modality axis shares the left-bottom origin and is parallel to cube depth.
depth_scale=(400-154)/92
modality_end=(origin[0]+92*depth_scale,origin[1]-70*depth_scale)
path([origin,modality_end],color=MUTED,arrow=True,sw=2,role='transfer-axis-modality')
label_math(x+590,y+422,'Defense',r'\mathcal{D}',24,bold=False,align='right')
label_math(x+26,y+233,'Runtime',r'\mathcal{E}',23,bold=False)
label_math(x+690,y+177,'Modality',r'\mathcal{M}',19,bold=False,align='right',suffix='(Text · Vision · Audio)')
# The transfer vector starts at exactly the same origin as all three axes.
path([origin,(x+615,y+198)],color=RED,sw=3.5,dash=True,arrow=True,role='transfer-vector')
math_text(x+526,y+300,r'\mathcal{T}(a,m,d,e)',24,color=RED,bold=True)
label_math(x+337,y+448,'Attack representations',r'\mathcal{A}',23,color=AMBER,align='center',suffix='index tensor slices.')
notes(x,y,'Transfer tests cover low-resource dialects','and culturally specific safety contexts.','Transfer anchors include PoEX, MultiJail and Any-to-Any.')

# 5. Agent execution.
x,y=920,1040
panel(x,y,'Agent Execution','§9.3','Sandboxed trajectories support stateful testing.','#E0F2FE',BLUE,'execution')
text(x+360,y+143,'Execution Sandbox',25,bold=True,align='center')
box(x+26,y+166,668,283,fill='#FAFCFE',stroke='#BCD5E7',r=10,sw=1.6)
# Side ports and an outer return lane clear both the circles and their captions.
rounded_path([(x+625,y+292),(x+672,y+292),(x+672,y+397),(x+48,y+397),(x+48,y+292),(x+95,y+292)],color=BLUE,dash=True,arrow=True,sw=2.6)
for xx,st,lbl in [(134,'0','Init Prompt'),(360,'1','Tool Dispatch'),(586,'T','Action Effect')]:
    oval(x+xx-39,y+253,78,78,fill='#FFFFFF',stroke=BLUE,sw=2.5)
    math_text(x+xx,y+303,'s_{'+st+'}',32,bold=True,align='center')
    text(x+xx,y+363,lbl,24,align='center')
line(x+176,y+292,x+317,y+292,color=BLUE,arrow=True,sw=3)
line(x+402,y+292,x+543,y+292,color=BLUE,arrow=True,sw=3)
# A compact event badge and a separate pointer replace the intersecting bolt.
box(x+248,y+181,224,36,fill='#FFF1F2',stroke='#DBA3AD',r=7,sw=1.2)
poison_icon='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect x="11" y="1" width="10" height="4" rx="1" fill="#C34F61"/>
<path d="M12 5v6l-6 6v11a3 3 0 0 0 3 3h14a3 3 0 0 0 3-3V17l-6-6V5" fill="#FFFFFF" stroke="#C34F61" stroke-width="1.8" stroke-linejoin="round"/>
<path d="m11 25 10 4m-10 0 10-4" stroke="#C34F61" stroke-width="1.8" stroke-linecap="round"/>
<path d="M11 19a5 5 0 1 1 10 0c0 2-1 3-3 4v2h-4v-2c-2-1-3-2-3-4Z" fill="#C34F61"/>
<circle cx="14" cy="19" r="1" fill="#FFFFFF"/><circle cx="18" cy="19" r="1" fill="#FFFFFF"/>
</svg>'''
(OUT/'assets'/'tool_poisoning.svg').write_text(poison_icon)
vector_asset(poison_icon,x+258,y+184,30,30,'Poison bottle with skull and crossbones')
text(x+296,y+207,'Tool Poisoning',22,color=RED,bold=True)
line(x+360,y+221,x+360,y+244,color=RED,sw=2.4,arrow=True)
text(x+360,y+433,'Deterministic State Rollback',24,color=BLUE,bold=True,align='center')
notes(x,y,'Snapshot reversion restores recorded state.','Containers and API boundaries isolate execution.','AgentDojo, AgentPoison and OSWorld anchor testing.')

# 6. Disclosure.
x,y=1740,1040
panel(x,y,'Governance & Disclosure','§9.6','Disclosure uses tiered access and coordinated triage.','#FFE4E6',RED,'governance')
text(x+360,y+139,'Evidence Access Tiers',25,bold=True,align='center')
for yy,fc,lbl in [(156,'#F6FBF7','Aggregate findings are publicly available.'),(213,'#FEF3C7','Vetted users receive gated artifact access.'),(270,'#FFE4E6','Actionable PoC chains remain withheld.')]:
    box(x+26,y+yy,668,48,fill=fc,stroke='#D1B8BD',r=6,sw=1.2)
    text(x+46,y+yy+32,lbl,24)
text(x+360,y+354,'Coordinated Flaw Disclosure (CVD)',25,bold=True,align='center')
disclosure_icons={
    'proof': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M6 2h14l7 7v21H6Z" fill="#FFF1F2" stroke="#C34F61" stroke-width="1.8" stroke-linejoin="round"/><path d="M20 2v8h7M11 15h11M11 20h11M11 25h8" fill="none" stroke="#C34F61" stroke-width="1.8" stroke-linecap="round"/></svg>',
    'fix': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="m16 2 12 5v9c0 6-5 11-12 15C9 27 4 22 4 16V7Z" fill="#FFF1F2" stroke="#C34F61" stroke-width="1.8" stroke-linejoin="round"/><path d="m10 16 4 5 8-10" fill="none" stroke="#C34F61" stroke-width="2.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'advisory': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M12 20v9h6l-2-9" fill="#FFF1F2" stroke="#C34F61" stroke-width="1.8" stroke-linejoin="round"/><path d="M3 12h9L27 4v22l-15-8H3Z" fill="#FFF1F2" stroke="#C34F61" stroke-width="1.8" stroke-linejoin="round"/><path d="M12 12v6M30 10v10" stroke="#C34F61" stroke-width="1.8" stroke-linecap="round"/></svg>'
}
for center,key,title,sub in [(128,'proof','Proof is documented.','FLARE-AI defines fields.'),(360,'fix','Vendors triage flaws.','Fixes follow quarantine.'),(592,'advisory','Advisories are issued.','Release is coordinated.')]:
    icon=disclosure_icons[key]
    (OUT/'assets'/('disclosure_'+key+'.svg')).write_text(icon)
    vector_asset(icon,x+center-18,y+371,36,36,'Disclosure '+key+' stage')
    text(x+center,y+430,title,20,bold=True,align='center')
    text(x+center,y+455,sub,18,color=MUTED,align='center')
for left,right in [(155,333),(387,565)]: line(x+left,y+389,x+right,y+389,color=RED,arrow=True,sw=2)
notes(x,y,'FLARE-AI and MITRE ATLAS structure reports.','Vendor triage links evidence, fixes and advisories.','Infrastructure includes Inspect AI and CERT/CC.')

# Alternative coordinator treatments retain the same title and six module links.
group='1';offset=(0,0)
if args.hub_style=='ellipse':
    oval(866,790,828,200,fill='#F6F9FC',stroke='#7894AC',sw=2.2)
    text(1280,842,'Continuous Closed-Loop',35,bold=True,align='center')
    text(1280,886,'Assurance Lifecycle',35,bold=True,align='center')
    text(1280,930,'Evidence connects discovery, repair and disclosure.',23,color=MUTED,align='center')
elif args.hub_style=='band':
    box(790,816,980,148,fill='#F6F9FC',stroke='#7894AC',r=6,sw=2.2)
    text(1280,878,'Continuous Closed-Loop Assurance Lifecycle',34,bold=True,align='center')
    text(1280,921,'Evidence connects discovery, repair and disclosure.',23,color=MUTED,align='center')
elif args.hub_style=='chamfer':
    boundary='<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 864 214"><path d="M24 0H836L860 24V186L836 210H24L0 186V24Z" fill="#F6F9FC" stroke="#7894AC" stroke-width="2.2" stroke-linejoin="miter"/></svg>'
    vector_asset(boundary,848,783,864,214,'Chamfered coordinator boundary')
    text(1280,851,'Continuous Closed-Loop',34,bold=True,align='center')
    text(1280,895,'Assurance Lifecycle',34,bold=True,align='center')
    text(1280,940,'Evidence connects discovery, repair and disclosure.',23,color=MUTED,align='center')
else:
    box(820,790,920,200,fill='#FFFFFF',stroke='#69849C',r=22,sw=2.8)
    if args.hub_style=='loop':
        line(1400,790,1460,790,color='#69849C',sw=2.8,arrow=True,arrow_size=18,role='hub-loop-top')
        line(1160,990,1100,990,color='#69849C',sw=2.8,arrow=True,arrow_size=18,role='hub-loop-bottom')
    text(1280,850,'Continuous Closed-Loop',34,bold=True,align='center')
    text(1280,894,'Assurance Lifecycle',34,bold=True,align='center')
    text(1280,939,'Evidence connects discovery, repair and disclosure.',23,color=MUTED,align='center')

# Return bus: governance seeds both transfer tests and discovery.
path([(2100,1624),(2100,1685),(54,1685),(54,450),(96,450)],color=RED,sw=3,dash=True,arrow=True)
line(460,1685,460,1624,color=RED,sw=3,dash=True,arrow=True)
text(1280,1734,'Governed disclosures and regressions renew coverage seeds.',29,color=RED,bold=True,align='center')
text(2375,1785,'Schematics are conceptual.',20,color=MUTED,align='right')

defs='''<defs>
<marker id="gray" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L10,5 L0,10 Z" fill="#53677C"/></marker>
<marker id="gray-large" markerWidth="18" markerHeight="18" refX="16" refY="9" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L18,9 L0,18 Z" fill="#53677C"/></marker>
<marker id="blue" markerWidth="11" markerHeight="11" refX="9" refY="5.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L11,5.5 L0,11 Z" fill="#247CB5"/></marker>
<marker id="blue-large" markerWidth="18" markerHeight="18" refX="16" refY="9" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L18,9 L0,18 Z" fill="#247CB5"/></marker>
<marker id="red" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L12,6 L0,12 Z" fill="#C34F61"/></marker>
<marker id="green" markerWidth="11" markerHeight="11" refX="9" refY="5.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L11,5.5 L0,11 Z" fill="#348368"/></marker>
</defs>'''
svg_doc=f'''<svg xmlns="http://www.w3.org/2000/svg" width="2560" height="1810" viewBox="0 0 2560 1810" role="img" aria-labelledby="title desc">
<title id="title">Closed-Loop Research Agenda for Automated Red Teaming</title>
<desc id="desc">Six detailed research schematics surround a continuous assurance coordinator: discovery, independent decision oracles, remediation, threat transfer, reversible agent execution, and tiered disclosure. Directed evidence flows and governed feedback close the loop. Discovery curves are conceptual; the illustrated Chao1 expression assumes f2 greater than zero.</desc>
{defs}<rect width="2560" height="1810" fill="#FFFFFF"/>
{''.join(svg)}\n</svg>'''
(OUT/'closed_loop_research_agenda.svg').write_text(svg_doc)
ET.indent(root)
ET.ElementTree(root).write(OUT/'closed_loop_research_agenda.drawio',encoding='utf-8',xml_declaration=True)
print(f'Created SVG and native draw.io source ({counter} editable elements).')
