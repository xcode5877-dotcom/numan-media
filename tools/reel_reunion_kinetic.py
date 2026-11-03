"""Kinetic-typography reel / ad: لمّ الشمل؟ احكي معنا. Punchy line-by-line motion graphics, a different
transition per line, a retention progress bar, SFX on every cut. 1080x1920, 30fps, 15s.
Output: ads/reunion-whatsapp/video-9x16.mp4 (also used as the campaign reel)."""
import shutil, subprocess
from playwright.sync_api import sync_playwright
from common import *

OUT = REPO / "ads" / "reunion-whatsapp"; OUT.mkdir(parents=True, exist_ok=True)
FR = ROOT / "out" / "reunion-kinetic-frames"; shutil.rmtree(FR, ignore_errors=True); FR.mkdir(parents=True)
FPS, DUR = 30, 15.0

# (start, end, arabic, hebrew, style)
SCENES = [
    (0.00, 1.40, "زوجك<br>من <span class='hl'>برّا</span> البلاد؟", "בן או בת הזוג מחו״ל?", "punch"),
    (1.40, 2.65, "الملف<br><span class='hl'>واقف؟</span>", "התיק תקוע?", "slideL"),
    (2.65, 3.90, "رسالة من<br><span class='hl'>الداخلية؟</span>", "מכתב ממשרד הפנים?", "drop"),
    (3.90, 5.15, "التصريح<br><span class='hl'>قرّب يخلص؟</span>", "ההיתר עומד לפוג?", "slideR"),
    (5.15, 6.25, "استنّى.", "רגע.", "gold"),
    (6.25, 7.70, "لا تقدّم<br><span class='hl'>لحالك.</span>", "אל תגישו לבד.", "circle"),
    (7.70, 9.30, "<span id='cnt'>0</span>+ سنة<br>خبرة", "20+ שנות ניסיון", "count"),
    (9.30, 10.90, "لمّ الشمل؟<br><span class='hl'>احكي معنا.</span>", "איחוד משפחות? דברו איתנו.", "slam"),
]
END_AT = 10.9

CSS = f"""
#bg{{position:absolute;inset:0;background:{NAVY};overflow:hidden}}
.ln{{position:absolute;left:-10%;width:120%;height:2px;background:linear-gradient(90deg,transparent,{GOLD},transparent);opacity:.18}}
.sc{{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 90px 160px;opacity:0}}
.ar{{font-weight:900;font-size:150px;line-height:1.08;color:{CREAM}}}
.he{{font-family:Heebo;font-weight:700;font-size:58px;color:{GOLD};margin-top:40px}}
.gold{{background:{GOLD}}} .gold .ar{{color:{NAVY};font-size:230px}} .gold .he{{color:{NAVY}}}
#bar{{position:absolute;top:0;right:0;height:12px;background:{GOLD};z-index:9}}
#logo{{position:absolute;top:120px;right:90px;z-index:8}}
#end{{position:absolute;inset:0;background:{NAVY};opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding-bottom:120px;z-index:7}}
#wa{{display:inline-flex;align-items:center;gap:26px;background:{GOLD};color:{NAVY};border-radius:36px;padding:34px 56px;margin-top:80px}}
#flash{{position:absolute;inset:0;background:#fff;opacity:0;z-index:10;pointer-events:none}}
"""
WA = """<svg viewBox="0 0 32 32" width="92" height="92"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-3.9-.5-5.6-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.8 5.1 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.1-.3-.2-.6-.3z"/></svg>"""
scenes_html = "".join(
    f"<div class='sc {'gold' if st=='gold' else ''}' id='s{k}'><div class='ar'>{a}</div><div class='he'>{h}</div></div>"
    for k, (_, _, a, h, st) in enumerate(SCENES))
lines = "".join(f"<div class='ln' style='top:{y}px' data-sp='{sp}'></div>" for y, sp in ((340, 1.0), (760, -1.4), (1180, 0.8), (1560, -1.1)))

BODY = f"""<div id='bg'>{lines}</div><div id='bar'></div><div id='logo'>{lockup(1.2)}</div>{scenes_html}
<div id='end'>
  {mark(240)}
  <div style='font-family:FRL;font-weight:500;font-size:92px;margin-top:40px'>נעמאן עבדאללה</div>
  <div style='font-family:Heebo;font-size:32px;letter-spacing:.4em;color:{GOLD};margin-top:12px'>משרד עורכי דין</div>
  <div style='font-weight:900;font-size:84px;line-height:1.2;margin-top:90px'>اكتبلنا <span class='hl'>«لمّ شمل»</span><br>عالواتساب</div>
  <div style='font-family:Heebo;font-weight:700;font-size:46px;color:{GOLD};margin-top:26px'>כתבו לנו «איחוד משפחות» בוואטסאפ</div>
  <div id='wa'>{WA}<span style='font-weight:900;font-size:74px;direction:ltr;white-space:nowrap'>{PHONE}</span></div>
</div><div id='flash'></div>
<script>
const S={[[a, b, st] for a, b, _, _, st in SCENES]}; const END={END_AT}, DUR={DUR};
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)); const eo=x=>1-Math.pow(1-x,3);
const ob=x=>{{const c1=2.2,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);}};
window.render=function(t){{
  document.getElementById('bar').style.width=(100*cl(t/DUR))+'%';
  document.querySelectorAll('.ln').forEach(l=>{{l.style.transform=`translateX(${{Math.sin(t*parseFloat(l.dataset.sp))*120}}px)`;}});
  let fl=0;
  S.forEach(([a,b,st],k)=>{{
    const e=document.getElementById('s'+k); const on=t>=a&&t<b; e.style.opacity=on?1:0; if(!on)return;
    const p=cl((t-a)/0.32), q=eo(p), o=cl((b-t)/0.12); let tr='', clip='none';
    if(st==='punch') tr=`scale(${{2.2-1.2*ob(p)}})`;
    if(st==='slideL') tr=`translateX(${{(1-q)*-1100}}px) skewX(${{(1-q)*18}}deg)`;
    if(st==='slideR') tr=`translateX(${{(1-q)*1100}}px) skewX(${{(1-q)*-18}}deg)`;
    if(st==='drop') tr=`translateY(${{(1-ob(p))*-900}}px)`;
    if(st==='gold') {{ clip=`inset(0 0 0 ${{(1-q)*100}}%)`; tr=`scale(${{1.15-0.15*q}})`; }}
    if(st==='circle') clip=`circle(${{q*150}}% at 50% 45%)`;
    if(st==='count') {{ tr=`scale(${{0.7+0.3*ob(p)}})`; const c=document.getElementById('cnt'); c.textContent=Math.round(20*eo(cl((t-a)/0.9))); }}
    if(st==='slam') tr=`scale(${{3-2*ob(cl((t-a)/0.28))}}) rotate(${{(1-q)*-6}}deg)`;
    const shake=(t-a<0.25&&(st==='punch'||st==='slam'||st==='drop'))?Math.sin(t*120)*10*(1-(t-a)/0.25):0;
    e.style.transform=tr+` translate(${{shake}}px,0)`; e.style.clipPath=clip; e.style.filter=o<1?`blur(${{(1-o)*14}}px)`:'none';
    if(t-a<0.06) fl=0.18*(1-(t-a)/0.06);
  }});
  const en=document.getElementById('end'); const pe=cl((t-END)/0.3); en.style.opacity=pe;
  en.style.transform=`scale(${{1.08-0.08*eo(pe)}})`;
  const w=document.getElementById('wa'); w.style.transform=`scale(${{t>END+0.6?1+0.05*Math.sin((t-END)*6):eo(cl((t-END-0.3)/0.3))}})`;
  document.getElementById('logo').style.opacity=(t<END&&!(t>=5.15&&t<6.25))?1:0;
  document.getElementById('flash').style.opacity=fl;
}};
</script>"""
HTML = page(BODY, 1080, 1920, CSS)

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(HTML, wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    for i in range(int(DUR * FPS)):
        pg.evaluate(f"render({i/FPS})"); pg.screenshot(path=str(FR / f"f{i:04d}.jpg"), type="jpeg", quality=90)
    b.close()

# Sound: soft pulse bed (tension) until the gold stop, then a lift; a hit/whoosh on every cut; riser into "استنّى"; chord + pings at the end.
parts, labels = [], []
def add(expr, ms):
    lab = f"s{len(labels)}"; parts.append(f"{expr},adelay={ms}|{ms}[{lab}]"); labels.append(f"[{lab}]")
beat = 0.0
while beat < 5.1:
    add("sine=f=55:d=0.22,afade=t=out:d=0.22,volume=1.1", int(beat * 1000)); beat += 0.42
for a, _, _, _, st in SCENES:
    ms = int(a * 1000)
    if st in ("punch", "slam", "drop"): add("sine=f=120:d=0.35,afade=t=out:d=0.35,volume=1.2", ms)
    add("anoisesrc=d=0.28:c=pink:a=0.5,highpass=f=800,afade=t=in:d=0.08,afade=t=out:st=0.08:d=0.2,volume=0.55", max(0, ms - 80))
add("sine=f=300:d=0.9,afade=t=in:d=0.85,volume=0.35", 4250)            # riser into the stop
add("sine=f=1760:d=0.25,afade=t=out:d=0.25,volume=0.35", 5150)          # bright ping on the gold stop
for k in range(20):                                                     # counter ticks
    add("sine=f=1200:d=0.03,afade=t=out:d=0.03,volume=0.22", int((7.7 + 0.9 * (k / 20) ** 0.5) * 1000))
beat = 6.25
while beat < 10.9:
    add("sine=f=65:d=0.18,afade=t=out:d=0.18,volume=1.0", int(beat * 1000)); beat += 0.36
for f, d in ((392, 0), (523, 90), (659, 180), (784, 270)): add(f"sine=f={f}:d=2.6,afade=t=out:d=2.6,volume=0.24", int(END_AT * 1000) + d)
for k in range(3): add("sine=f=1046:d=0.12,afade=t=out:d=0.12,volume=0.3", int((END_AT + 1.2 + k * 1.1) * 1000))
filt = ";".join(parts) + ";" + "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.9,apad=whole_dur={DUR},atrim=0:{DUR}"
A = ROOT / "out" / "reunion-kinetic.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-filter_complex", filt, "-ar", "44100", "-ac", "2", str(A)], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FR / "f%04d.jpg"), "-i", str(A),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                "-shortest", "-movflags", "+faststart", str(OUT / "video-9x16.mp4")], check=True)
print(OUT / "video-9x16.mp4")
