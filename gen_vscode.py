"""Generate profile/header.svg — an animated VS Code-style "about me" card.

Usage: python3 gen_vscode.py [-o profile/header.svg] [--static]
Edit LINES below; token classes: k=keyword t=type p=property s=string
c=comment f=function n=punctuation v=variable.
"""
import argparse, html, os
# Token classes: k=keyword t=type p=property s=string c=comment f=function n=punct v=variable
LINES = [
    [("c", "// hi, I'm Mitch")],
    [],
    [("k","const "),("v","mitch"),("n",": "),("t","Engineer"),("n"," = {")],
    [("n","  "),("p","studying"),("n",": "),("s",'"Computer Science @ Edith Cowan University"'),("n",",")],
    [("n","  "),("p","focus"),("n",": ["),("s",'"distributed systems"'),("n",", "),("s",'"embedded firmware"'),("n","],")],
    [("n","  "),("p","alsoInto"),("n",": ["),("s",'"security research"'),("n",", "),("s",'"game reverse engineering"'),("n","],")],
    [("n","  "),("p","building"),("n",": ["),("s",'"self-hosted streaming"'),("n",", "),("s",'"docker swarm homelab"'),("n","],")],
    [("n","  "),("p","stack"),("n",": ["),("s",'"Python"'),("n",", "),("s",'"C"'),("n",", "),("s",'"TypeScript"'),("n",", "),("s",'"Docker"'),("n","],")],
    [("n","  "),("p","location"),("n",": "),("s",'"Perth, WA"'),("n",",")],
    [("n","};")],
    [],
    [("v","mitch"),("n","."),("f","connect"),("n","(); "),("c","// let's build something")],
]
W, LH, TOP, CODE_X, CW = 860, 24, 92, 64, 8.43
H = TOP + LH*len(LINES) + 46
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="profile/header.svg")
ap.add_argument("--static", action="store_true", help="no typing animation")
args = ap.parse_args()
static = args.static

out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a('''<style>
text{font-family:"JetBrains Mono","Fira Code",Consolas,"SF Mono",Menlo,"DejaVu Sans Mono",monospace;font-size:14px;white-space:pre}
.k{fill:#569cd6}.t{fill:#4ec9b0}.p{fill:#9cdcfe}.s{fill:#ce9178}.c{fill:#6a9955;font-style:italic}.f{fill:#dcdcaa}.n{fill:#d4d4d4}.v{fill:#4fc1ff}
.ln{fill:#858585;text-anchor:end}.ui{fill:#cccccc;font-size:12px}.sb{fill:#ffffff;font-size:12px}
.cover{animation:type .7s steps(48,end) forwards}
@keyframes type{to{transform:translateX(800px)}}
.cursor{opacity:0;animation:show 0s forwards,blink 1s step-end infinite}
@keyframes show{to{opacity:1}}
@keyframes blink{50%{fill:transparent}}
@media (prefers-reduced-motion:reduce){.cover{display:none}.cursor{animation:none;opacity:1}}
</style>''')
a('<defs><clipPath id="ed"><rect x="0" y="0" width="%d" height="%d" rx="10"/></clipPath>' % (W, H))
a(f'<clipPath id="code"><rect x="{CODE_X-4}" y="{TOP-18}" width="{W-CODE_X-10}" height="{LH*len(LINES)+4}"/></clipPath></defs>')
a('<g clip-path="url(#ed)">')
a(f'<rect width="{W}" height="{H}" fill="#1e1e1e"/>')
# title bar
a(f'<rect width="{W}" height="36" fill="#323233"/>')
for i,c in enumerate(["#ff5f57","#febc2e","#28c840"]):
    a(f'<circle cx="{20+i*20}" cy="18" r="6" fill="{c}"/>')
a(f'<text x="{W/2}" y="23" class="ui" text-anchor="middle">about-me.ts — mitchnaake</text>')
# tab bar
a(f'<rect y="36" width="{W}" height="34" fill="#252526"/>')
a('<rect y="36" width="150" height="34" fill="#1e1e1e"/><rect y="36" width="150" height="2" fill="#0078d4"/>')
a('<text x="16" y="58" class="ui"><tspan fill="#3178c6" font-weight="bold">TS</tspan><tspan fill="#ffffff">  about-me.ts</tspan></text>')
a('<text x="166" y="58" class="ui" fill-opacity=".6"><tspan fill="#e8bf6a">{}</tspan>  projects.json</text>')
# code
for i, toks in enumerate(LINES):
    y = TOP + i*LH
    a(f'<text x="{CODE_X-22}" y="{y}" class="ln">{i+1}</text>')
    if toks:
        body = "".join(f'<tspan class="{c}">{html.escape(t)}</tspan>' for c,t in toks)
        a(f'<text x="{CODE_X}" y="{y}">{body}</text>')
# typing covers
delay, cur_end = 0.4, 0
if not static:
    a('<g clip-path="url(#code)">')
    for i, toks in enumerate(LINES):
        y = TOP + i*LH
        n = sum(len(t) for _,t in toks)
        if not n:
            delay += .1; continue
        dur = max(.25, n*0.018)
        a(f'<rect class="cover" x="{CODE_X-2}" y="{y-17}" width="800" height="{LH}" fill="#1e1e1e" style="animation-delay:{delay:.2f}s;animation-duration:{dur:.2f}s"/>')
        delay += dur + .08
    a('</g>')
last = LINES[-1]; n = sum(len(t) for _,t in last)
a(f'<rect class="cursor" x="{CODE_X + n*CW + 2:.1f}" y="{TOP+(len(LINES)-1)*LH-15}" width="2" height="19" fill="#aeafad" style="animation-delay:{delay:.2f}s,{delay:.2f}s"/>')
# status bar
a(f'<rect y="{H-24}" width="{W}" height="24" fill="#007acc"/>')
a(f'<text x="12" y="{H-8}" class="sb">main*   0 problems</text>')
a(f'<text x="{W-12}" y="{H-8}" class="sb" text-anchor="end">Ln {len(LINES)}, Col {n+1}    UTF-8    TypeScript</text>')
a('</g></svg>')
os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
with open(args.output, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
print(f"wrote {args.output}")
