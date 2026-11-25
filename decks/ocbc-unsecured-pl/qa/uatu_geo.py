import sys
from itertools import combinations
from pptx import Presentation
from pptx.util import Pt
EMU, TOL = 914400, 0.03
SKIP = ("bg-",)
p = Presentation(sys.argv[1]); W, H = p.slide_width/EMU, p.slide_height/EMU
title_y=[]; footer={}
for i, s in enumerate(p.slides, 1):
    R=[(sh.name,(sh.left/EMU,sh.top/EMU,sh.width/EMU,sh.height/EMU)) for sh in s.shapes if sh.width]
    for n,(x,y,w,h) in R:
        if x<-TOL or y<-TOL or x+w>W+TOL or y+h>H+TOL: print(f"S{i-1:02d} OFF-CANVAS {n}")
    for (n1,a),(n2,b) in combinations(R,2):
        ox=max(0,min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0])); oy=max(0,min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1]))
        if n1.startswith(SKIP) or n2.startswith(SKIP): continue
        if ox*oy>0.05: print(f"S{i-1:02d} OVERLAP {n1} x {n2} ({ox*oy:.2f} sq in)")
    for sh in s.shapes:
        if sh.name=="Title": title_y.append((i-1,round(sh.top/EMU,2),round(sh.height/EMU,2)))
        if sh.name in("Source","Tracker","DummyTag"): footer.setdefault(sh.name,set()).add((round(sh.left/EMU,2),round(sh.top/EMU,2)))
        if sh.has_text_frame:
            for para in sh.text_frame.paragraphs:
                for r in para.runs:
                    if r.font.size and r.font.size<Pt(9): print(f"S{i-1:02d} FONT<9 {sh.name} {r.font.size.pt}")
    names=[sh.name for sh in s.shapes]
    gen=[n for n in names if n.startswith(("TextBox","Rectangle","Chart","Table"))]
    if gen: print(f"S{i-1:02d} UNNAMED {len(gen)}: {gen[:4]}")
print("TITLE positions:", sorted(set((y,h) for _,y,h in title_y)))
print("FOOTER positions:", footer)
