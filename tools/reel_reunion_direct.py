"""Direct ad reel: لمّ الشمل؟ احكي معنا. Message from second one, animated icons (not text-only), smooth eased scene changes.
1080x1920, 30fps, 14s. Output: ads/reunion-whatsapp/video-direct-9x16.mp4"""
import json, shutil, subprocess
from playwright.sync_api import sync_playwright
from common import *

OUT = REPO / "ads" / "reunion-whatsapp"; OUT.mkdir(parents=True, exist_ok=True)
FR = ROOT / "out" / "reunion-direct-frames"; shutil.rmtree(FR, ignore_errors=True); FR.mkdir(parents=True)
FPS, DUR = 30, 14.0
SC = [(0.0, 3.4), (3.4, 8.2), (8.2, 10.2), (10.2, 14.0)]  # scene windows

ICON = {  # stroke icons, 48x48 grid
    "doc": "<path d='M14 6h14l10 10v26H14z'/><path d='M28 6v10h10M19 25h14M19 31h14M19 37h9'/>",
    "renew": "<path d='M38 20a14 14 0 0 0-26-4M10 28a14 14 0 0 0 26 4'/><path d='M12 8v8h8M36 40v-8h-8'/>",
    "mail": "<rect x='6' y='12' width='36' height='26' rx='3'/><path d='M6 15l18 13 18-13'/>",
    "shield": "<path d='M24 5l15 6v11c0 10-6.5 17-15 21C15.5 39 9 32 9 22V11z'/><path d='M17 24l5 5 9-10'/>",
}
def icon(k, s=74):
    return f"<svg viewBox='0 0 48 48' width='{s}' height='{s}' fill='none' stroke='{GOLD}' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'>{ICON[k]}</svg>"
ITEMS = [("doc", "تقديم ملف جديد", "הגשת בקשה חדשה"), ("renew", "تجديد التصاريح", "חידוש היתרים"),
         ("mail", "الرد على رسائل الداخلية", "מענה למשרד הפנים"), ("shield", "تنظيم الوضع القانوني", "הסדרת מעמד")]
WA = """<svg viewBox="0 0 32 32" width="{s}" height="{s}"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-3.9-.5-5.6-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.8 5.1 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.1-.3-.2-.6-.3z"/></svg>"""

CSS = f"""
#root{{position:fixed;inset:0;overflow:hidden;background:{NAVY}}}
.blob{{position:absolute;border-radius:50%;filter:blur(40px)}}
.sc{{position:absolute;inset:0;opacity:0;display:flex;flex-direction:column;align-items:center;text-align:center;padding:0 80px}}
.big{{font-weight:900;font-size:170px;line-height:1.05;color:{CREAM}}}
.heb{{font-family:Heebo;font-weight:700;font-size:56px;color:{GOLD}}}
.row{{display:flex;align-items:center;gap:34px;width:100%;background:rgba(255,255,255,.04);border:1.5px solid rgba(201,164,92,.35);border-radius:30px;padding:30px 40px;margin-top:26px;text-align:right}}
.ra{{font-weight:800;font-size:58px;line-height:1.15}} .rh{{font-family:Heebo;font-size:38px;color:#AFB8C8;margin-top:4px}}
#logo{{position:absolute;top:150px;left:0;right:0;display:flex;justify-content:center;z-index:5}}
#wa{{display:inline-flex;align-items:center;gap:26px;background:{GOLD};color:{NAVY};border-radius:40px;padding:36px 60px}}
"""
rows = "".join(f"<div class='row' id='r{k}'>{icon(i)}<div><div class='ra'>{a}</div><div class='rh'>{h}</div></div></div>" for k, (i, a, h) in enumerate(ITEMS))

# Scene 1 visual: two people on either side of a dashed border move together and a home draws around them.
REUNION_SVG = f"""<svg viewBox='0 0 600 420' width='640' height='448' fill='none' stroke-linecap='round' stroke-linejoin='round'>
 <path id='border' d='M300 30 V400' stroke='{GOLD}' stroke-width='4' stroke-dasharray='14 16' opacity='.7'/>
 <path id='house' d='M120 380 V200 L300 70 L480 200 V380 Z' stroke='{GOLD}' stroke-width='8' pathLength='1' stroke-dasharray='1' stroke-dashoffset='1'/>
 <g id='pA'><circle cx='0' cy='-70' r='34' fill='{CREAM}'/><path d='M-52 40 a52 60 0 0 1 104 0 Z' fill='{CREAM}'/></g>
 <g id='pB'><circle cx='0' cy='-70' r='34' fill='{GOLD}'/><path d='M-52 40 a52 60 0 0 1 104 0 Z' fill='{GOLD}'/></g>
</svg>"""

BODY = f"""<div id='root'>
<div class='blob' id='b1' style='width:700px;height:700px;background:#173A6E;opacity:.55'></div>
<div class='blob' id='b2' style='width:520px;height:520px;background:#5A4520;opacity:.35'></div>
<div id='logo'>{lockup(1.25)}</div>
<div class='sc' id='s0' style='justify-content:center;padding-bottom:160px'>
  <div id='vis'>{REUNION_SVG}</div>
  <div class='big' id='t0' style='margin-top:40px'>لمّ الشمل؟</div>
  <div class='heb' id='h0' style='margin-top:26px'>איחוד משפחות?</div>
</div>
<div class='sc' id='s1' style='justify-content:center;padding-bottom:120px'>
  <div style='font-weight:900;font-size:96px;line-height:1.15' id='t1'>منرافقك<br><span class='hl'>بكل خطوة</span></div>
  <div class='heb' style='font-size:48px;margin:24px 0 30px' id='h1'>מלווים אתכם בכל שלב</div>
  {rows}
</div>
<div class='sc' id='s2' style='justify-content:center;padding-bottom:160px'>
  <div style='font-weight:900;font-size:300px;line-height:1;color:{GOLD};direction:ltr'><span id='cnt'>0</span>+</div>
  <div style='font-weight:800;font-size:90px;margin-top:10px'>سنة خبرة</div>
  <div style='width:0;height:4px;background:{GOLD};margin-top:40px' id='ln'></div>
  <div class='heb' style='margin-top:30px'>שנות ניסיון</div>
</div>
<div class='sc' id='s3' style='justify-content:center;padding-bottom:180px'>
  <div style='font-weight:900;font-size:120px;line-height:1.12' id='t3'>احكي معنا<br><span class='hl'>اليوم.</span></div>
  <div class='heb' style='margin-top:30px' id='h3'>דברו איתנו היום.</div>
  <div style='font-size:46px;color:#D9D3C6;margin:70px 0 30px' id='p3'>اكتبلنا «لمّ شمل» عالواتساب · כתבו לנו בוואטסאפ</div>
  <div id='wa'>{WA.format(s=96)}<span style='font-weight:900;font-size:80px;direction:ltr;white-space:nowrap'>{PHONE}</span></div>
</div>
</div>
<script>
const SC={json.dumps(SC)};
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)); const io=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2; const eo=x=>1-Math.pow(1-x,3);
const fade=(t,a,b,d=0.6)=>Math.min(a===0?1:io(cl((t-a+0.3)/d)), io(cl((b+0.3-t)/d)));   // soft in/out per scene
const up=(el,p,dy=50)=>{{el.style.opacity=p;el.style.transform=`translateY(${{(1-p)*dy}}px)`;}};
window.render=function(t){{
  const b1=document.getElementById('b1'),b2=document.getElementById('b2');
  b1.style.left=(-200+Math.sin(t*0.4)*120)+'px'; b1.style.top=(300+Math.cos(t*0.3)*160)+'px';
  b2.style.right=(-150+Math.cos(t*0.35)*100)+'px'; b2.style.top=(1250+Math.sin(t*0.45)*140)+'px';
  SC.forEach(([a,b],k)=>{{const e=document.getElementById('s'+k); const f=(k===SC.length-1)?io(cl((t-a+0.3)/0.6)):fade(t,a,b);
    e.style.opacity=f; e.style.transform=`scale(${{0.97+0.03*f}})`;}});
  // scene 0: people glide together, border fades, home draws around them
  const m=io(cl((t-0.2)/1.4)); document.getElementById('pA').setAttribute('transform',`translate(${{150+m*90}},300)`);
  document.getElementById('pB').setAttribute('transform',`translate(${{450-m*90}},300)`);
  document.getElementById('border').style.opacity=0.7*(1-io(cl((t-0.8)/0.8)));
  document.getElementById('house').style.strokeDashoffset=1-io(cl((t-1.0)/1.2));
  up(document.getElementById('t0'),eo(cl((t-0.3)/0.7))); up(document.getElementById('h0'),eo(cl((t-0.7)/0.7)));
  // scene 1: title, then each service row rises in turn
  up(document.getElementById('t1'),eo(cl((t-3.6)/0.7))); up(document.getElementById('h1'),eo(cl((t-3.9)/0.7)));
  for(let k=0;k<4;k++) up(document.getElementById('r'+k),eo(cl((t-4.4-k*0.65)/0.7)),70);
  // scene 2: years count up smoothly, gold line draws
  document.getElementById('cnt').textContent=Math.round(20*io(cl((t-8.4)/1.1)));
  document.getElementById('ln').style.width=(io(cl((t-8.6)/1.0))*520)+'px';
  // scene 3: call to action, WhatsApp button breathes; logo steps aside
  up(document.getElementById('t3'),eo(cl((t-10.4)/0.7))); up(document.getElementById('h3'),eo(cl((t-10.7)/0.7)));
  up(document.getElementById('p3'),eo(cl((t-11.0)/0.7)));
  const w=document.getElementById('wa'); const pw=eo(cl((t-11.3)/0.7)); w.style.opacity=pw;
  w.style.transform=`scale(${{(0.9+0.1*pw)*(t>12?1+0.035*Math.sin((t-12)*5):1)}})`;
}};
</script>"""
HTML = page(BODY, 1080, 1920, CSS)

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(HTML, wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    for i in range(int(DUR * FPS)):
        pg.evaluate(f"render({i/FPS})"); pg.screenshot(path=str(FR / f"f{i:04d}.jpg"), type="jpeg", quality=90)
    b.close()

# Sound: confident steady pulse + warm pad, soft swells on scene changes, gentle ticks under the counter, resolving chord at the CTA.
parts, labels = [], []
def add(expr, ms):
    lab = f"s{len(labels)}"; parts.append(f"{expr},adelay={ms}|{ms}[{lab}]"); labels.append(f"[{lab}]")
t = 0.0
while t < 13.5:
    add("sine=f=58:d=0.2,afade=t=out:d=0.2,volume=0.9", int(t * 1000)); t += 0.5
for f in (196.0, 246.9, 293.7):
    add(f"sine=f={f}:d=10.2,afade=t=in:d=1.2,afade=t=out:st=9:d=1.2,volume=0.06", 0)
for a, _ in SC[1:]:
    add("anoisesrc=d=0.6:c=pink:a=0.25,lowpass=f=2500,afade=t=in:d=0.3,afade=t=out:st=0.3:d=0.3,volume=0.35", int((a - 0.3) * 1000))
for k in range(4): add("sine=f=784:d=0.12,afade=t=out:d=0.12,volume=0.25", int((4.4 + k * 0.65) * 1000))
for k in range(12): add("sine=f=1200:d=0.03,afade=t=out:d=0.03,volume=0.18", int((8.4 + 1.1 * k / 12) * 1000))
for f, d in ((392, 0), (494, 80), (587, 160), (784, 240)): add(f"sine=f={f}:d=3.2,afade=t=out:d=3.2,volume=0.2", 10200 + d)
filt = ";".join(parts) + ";" + "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.9,apad=whole_dur={DUR},atrim=0:{DUR}"
A = ROOT / "out" / "reunion-direct.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-filter_complex", filt, "-ar", "44100", "-ac", "2", str(A)], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FR / "f%04d.jpg"), "-i", str(A),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                "-shortest", "-movflags", "+faststart", str(OUT / "video-direct-9x16.mp4")], check=True)
print(OUT / "video-direct-9x16.mp4")
