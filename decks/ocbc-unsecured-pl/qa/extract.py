import re, csv, glob
from pptx import Presentation
p = Presentation("deck.pptx")
vals=set()
for f in glob.glob("data/*.csv"):
    for row in csv.reader(open(f)):
        for c in row:
            for n in re.findall(r"\d[\d,]*\.?\d*", c): vals.add(n.replace(",",""))
out=open("qa/deck_text.md","w"); notes=open("qa/notes.txt","w")
for i,s in enumerate(p.slides):
    texts=[]
    for sh in s.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip(): texts.append((sh.name, sh.text_frame.text.replace("\n"," / ")))
        if sh.has_table:
            for r in sh.table.rows:
                texts.append((sh.name, " | ".join(c.text for c in r.cells)))
    out.write(f"\n## S{i:02d}\n"); [out.write(f"- [{n}] {t}\n") for n,t in texts]
    nt=s.notes_slide.notes_text_frame.text; out.write(f"- [NOTES] {nt}\n"); notes.write(nt+"\n\n")
    title=next((t for n,t in texts if n=="Title"),"")
    print(f"S{i:02d} | {title}")
    for n,t in texts+[("NOTES",nt)]:
        if n in("Source","Tracker","DummyTag"): continue
        for num in re.findall(r"(?<![A-Za-z\-])\d[\d,]*\.?\d*", t):
            k=num.replace(",","").rstrip(".")
            if k not in vals: print(f"    UNMATCHED S{i:02d} [{n}] '{num}'  …{t[max(0,t.find(num)-40):t.find(num)+30]}…")
