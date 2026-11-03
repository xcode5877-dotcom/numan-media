"""Shared brand pieces for Numan Abdallah media: fonts, colors, logo mark, renderer."""
import base64, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
REPO = ROOT.parent
NAVY, NAVY2, GOLD, CREAM, RED = "#0B1A2E", "#12284A", "#C9A45C", "#F2ECE0", "#D2483C"
PHONE = "052-6022027"

def _b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

FONTS = "".join(
    f"@font-face{{font-family:{fam};src:url(data:font/ttf;base64,{_b64(ROOT/'fonts'/f)});font-weight:100 900}}\n"
    for fam, f in (("Rubik", "Rubik.ttf"), ("FRL", "FrankRuhlLibre.ttf"), ("Heebo", "Heebo.ttf"))
)

MARK = """<svg viewBox="0 0 160 143" width="{w}" height="{h}" style="color:{c};display:block">
<g fill="currentColor"><path d="M80 2 L86 9 L80 16 L74 9 Z"/><rect x="77.6" y="16" width="4.8" height="112"/>
<path d="M20 32.2 H140 V35.8 H20 Z"/><circle cx="20" cy="34" r="4.2"/><circle cx="140" cy="34" r="4.2"/>
<circle cx="80" cy="34" r="6.5"/><path d="M2 90 H38 Q20 106 2 90 Z"/><path d="M122 90 H158 Q140 106 122 90 Z"/>
<path d="M62 126 H98 V131 H62 Z"/><path d="M50 133 H110 V141 H50 Z"/></g>
<g stroke="currentColor" stroke-width="1.4" fill="none"><path d="M20 38 L4 90 M20 38 L36 90 M140 38 L124 90 M140 38 L156 90"/></g></svg>"""

def mark(w, c=GOLD):
    return MARK.format(w=w, h=round(w * 143 / 160), c=c)

def lockup(size=1.0, txt=CREAM):
    """Small horizontal logo: mark + name, for corners of designs."""
    return (f"<div style='display:flex;align-items:center;gap:{18*size}px;direction:rtl'>{mark(int(64*size))}"
            f"<div><div style='font-family:FRL;font-weight:500;font-size:{34*size}px;line-height:1;color:{txt}'>נעמאן עבדאללה</div>"
            f"<div style='font-family:Heebo;font-size:{15*size}px;letter-spacing:.35em;color:{GOLD};margin-top:{6*size}px'>משרד עורכי דין</div></div></div>")

BASE_CSS = FONTS + f"""*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:{NAVY};font-family:Rubik;color:{CREAM};direction:rtl}}
.he{{font-family:Heebo}} .hl{{background:{GOLD};color:{NAVY};padding:0 .18em;border-radius:.12em;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
"""

def page(body, w, h, extra_css=""):
    return (f"<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><style>{BASE_CSS}"
            f"html,body{{width:{w}px;height:{h}px;overflow:hidden}}{extra_css}</style></head><body>{body}</body></html>")

def render_all(items, w, h):
    """items: list of (html, out_path). Renders each page to PNG."""
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h})
        for html, out in items:
            out = pathlib.Path(out); out.parent.mkdir(parents=True, exist_ok=True)
            pg.set_content(html, wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
            pg.screenshot(path=str(out))
        b.close()
