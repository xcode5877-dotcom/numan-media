"""Direct-response ad: لمّ الشمل؟ احكي معنا — feed 1080x1350 + story 1080x1920 (PNG) + 8s video 1080x1920."""
import shutil, subprocess
from playwright.sync_api import sync_playwright
from common import *

OUT = REPO / "ads" / "reunion-whatsapp"
OUT.mkdir(parents=True, exist_ok=True)
ITEMS = [("تقديم ملف جديد", "הגשת בקשה חדשה"), ("تجديد التصاريح", "חידוש היתרים"),
         ("الرد على رسائل الداخلية", "מענה למשרד הפנים"), ("تنظيم الوضع القانوني", "הסדרת מעמד")]
WA = """<svg viewBox="0 0 32 32" width="{s}" height="{s}"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-3.9-.5-5.6-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.8 5.1 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.1-.3-.2-.6-.3z"/></svg>"""

def html(w, h, sc):
    css = f"""
#a{{position:absolute;inset:0;background:{NAVY};overflow:hidden}}
#g{{position:absolute;width:{1300*sc}px;height:{1300*sc}px;border-radius:50%;background:radial-gradient(circle,#173462 0%,transparent 65%);top:{-350*sc}px;left:{-450*sc}px}}
#wrap{{position:absolute;inset:{(260 if h>1500 else 70)}px 76px {(330 if h>1500 else 70)}px 76px;display:flex;flex-direction:column}}
#q{{font-weight:900;font-size:{185*sc}px;line-height:1;color:{GOLD};white-space:nowrap}}
#c{{font-weight:900;font-size:{108*sc}px;line-height:1.1;color:{CREAM};margin-top:{14*sc}px}}
#hq{{font-family:Heebo;font-weight:700;font-size:{50*sc}px;color:{GOLD};margin-top:{22*sc}px}}
.it{{display:flex;align-items:center;gap:{24*sc}px;margin-top:{26*sc}px}}
.ck{{flex:none;width:{62*sc}px;height:{62*sc}px;border-radius:50%;background:{GOLD};color:{NAVY};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:{38*sc}px}}
.ia{{font-weight:700;font-size:{50*sc}px;line-height:1.15}} .ih{{font-family:Heebo;font-size:{32*sc}px;color:#AFB8C8}}
#bd{{display:inline-flex;gap:14px;align-items:center;border:2px solid {GOLD};color:{GOLD};border-radius:999px;padding:{10*sc}px {30*sc}px;font-weight:700;font-size:{32*sc}px;align-self:flex-start}}
#cta{{display:flex;align-items:center;justify-content:center;gap:{26*sc}px;background:{GOLD};color:{NAVY};border-radius:{30*sc}px;padding:{30*sc}px {40*sc}px;box-shadow:0 20px 50px rgba(201,164,92,.25)}}
#cta .l{{font-weight:800;font-size:{44*sc}px;line-height:1.1}} #cta .n{{font-weight:900;font-size:{64*sc}px;direction:ltr;line-height:1;white-space:nowrap}}
"""
    items = "".join(f"<div class='it' id='i{k}'><div class='ck'>✓</div><div><div class='ia'>{a}</div><div class='ih'>{b}</div></div></div>" for k, (a, b) in enumerate(ITEMS))
    body = f"""<div id='a'><div id='g'></div><div id='wrap'>
<div style='display:flex;justify-content:space-between;align-items:center'>{lockup(1.15*sc)}</div>
<div style='flex:1;display:flex;flex-direction:column;justify-content:center'>
  <div id='q'>لمّ الشمل؟</div><div id='c'>احكي معنا.</div><div id='hq'>איחוד משפחות? דברו איתנו.</div>
  <div style='margin-top:{40*sc}px'>{items}</div>
  <div id='bd' style='margin-top:{44*sc}px'>خبرة +20 سنة · 20+ שנות ניסיון</div>
</div>
<div id='cta'><span style='display:flex'>{WA.format(s=int(84*sc))}</span><div><div class='l' style='white-space:nowrap'>واتساب · וואטסאפ</div></div><div class='n'>{PHONE}</div></div>
</div></div>
<script>
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));const ob=x=>{{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);}};
window.render=function(t){{
 const q=document.getElementById('q');const p=cl(t/0.35);q.style.transform=`scale(${{1.6-0.6*ob(p)}})`;q.style.opacity=p>0?1:0;q.style.transformOrigin='right center';
 const c=document.getElementById('c');c.style.opacity=cl((t-0.7)/0.25);c.style.transform=`translateY(${{(1-cl((t-0.7)/0.25))*40}}px)`;
 document.getElementById('hq').style.opacity=cl((t-1.1)/0.3);
 for(let k=0;k<4;k++){{const e=document.getElementById('i'+k);const pk=cl((t-1.8-k*0.55)/0.25);e.style.opacity=pk;e.style.transform=`translateX(${{(1-pk)*-60}}px)`;}}
 document.getElementById('bd').style.opacity=cl((t-4.3)/0.3);
 const ct=document.getElementById('cta');const pc=cl((t-4.9)/0.3);ct.style.opacity=pc;
 const pulse=t>5.4?1+0.035*Math.sin((t-5.4)*7):0.85+0.15*ob(pc);ct.style.transform=`scale(${{pulse}})`;
}};
</script>"""
    return page(body, w, h, css)

FEED, STORY = html(1080, 1350, 0.86), html(1080, 1920, 1.0)
FR = ROOT / "out" / "ad-reunion-frames"; shutil.rmtree(FR, ignore_errors=True); FR.mkdir(parents=True)
FPS, DUR = 30, 8.0
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, H_, doc in (("feed-1080x1350.png", 1350, FEED), ("story-1080x1920.png", 1920, STORY)):
        pg = b.new_page(viewport={"width": 1080, "height": H_})
        pg.set_content(doc, wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
        pg.evaluate("render(5.4)"); pg.screenshot(path=str(OUT / name))
    b.close()

print(OUT)
