"""Direct ad reel (Hotza'ah LaPoal / debts). Contrarian hook that sets us apart from lawyers who promise "100% debt erasure":
a flashy "100% guaranteed" promo gets stamped "اهرب" -> what an honest lawyer actually does (4 icon rows) -> +20 years -> WhatsApp CTA.
1080x1920, 30fps, 15s. Output: ads/debt-whatsapp/video-direct-9x16.mp4"""
import json, shutil, subprocess
from playwright.sync_api import sync_playwright
from common import *

OUT = REPO / "ads" / "debt-whatsapp"; OUT.mkdir(parents=True, exist_ok=True)
FR = ROOT / "out" / "debt-direct-frames"; shutil.rmtree(FR, ignore_errors=True); FR.mkdir(parents=True)
FPS, DUR = 30, 15.0
SC = [(0.0, 3.8), (3.8, 8.6), (8.6, 10.6), (10.6, 15.0)]  # scene windows

ICON = {  # stroke icons, 48x48 grid
    "doc": "<path d='M14 6h14l10 10v26H14z'/><path d='M28 6v10h10M19 25h14M19 31h14M19 37h9'/>",
    "search": "<circle cx='21' cy='21' r='13'/><path d='M31 31l11 11'/>",
    "scale": "<path d='M24 6v34M10 14h28M16 40h16'/><path d='M10 14l-6 14a6 6 0 0 0 12 0zM38 14l-6 14a6 6 0 0 0 12 0z'/>",
    "renew": "<path d='M38 20a14 14 0 0 0-26-4M10 28a14 14 0 0 0 26 4'/><path d='M12 8v8h8M36 40v-8h-8'/>",
    "mail": "<rect x='6' y='12' width='36' height='26' rx='3'/><path d='M6 15l18 13 18-13'/>",
    "shield": "<path d='M24 5l15 6v11c0 10-6.5 17-15 21C15.5 39 9 32 9 22V11z'/><path d='M17 24l5 5 9-10'/>",
}
def icon(k, s=74):
    return f"<svg viewBox='0 0 48 48' width='{s}' height='{s}' fill='none' stroke='{GOLD}' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'>{ICON[k]}</svg>"
ITEMS = [("search", "بنفحص ملفك كامل", "בודקים את כל התיק"), ("scale", "بنشوف إذا في مجال للاعتراض", "בודקים אפשרות להתנגדות"),
         ("doc", "تسوية ودفعات بتقدر عليها", "הסדר ותשלומים שאפשר לעמוד בהם"), ("shield", "حماية الراتب والحساب", "הגנה על משכורת וחשבון")]
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

# Scene 0 visual: a flashy generic "100% guaranteed" promo card, then a red stamp slams on it.
PROMO = f"""<div id='promo' style='position:relative;width:820px;margin:0 auto;background:linear-gradient(135deg,#FFD84D,#FF9F1C);color:#2A1A00;border-radius:36px;padding:50px 40px;box-shadow:0 30px 70px rgba(0,0,0,.5);transform:rotate(-3deg)'>
  <div style='font-weight:900;font-size:120px;line-height:1'>محو ديون</div>
  <div style='font-weight:900;font-size:150px;line-height:1.05;direction:ltr'>100%</div>
  <div style='font-weight:800;font-size:70px'>مضمون ✅✅</div>
  <div id='stamp' style='position:absolute;top:50%;left:50%;width:680px;margin:-130px 0 0 -340px;border:14px solid {RED};color:{RED};background:rgba(242,236,224,.92);border-radius:24px;font-weight:900;font-size:190px;line-height:230px;text-align:center;opacity:0'>اهرب</div>
</div>"""

BODY = f"""<div id='root'>
<div class='blob' id='b1' style='width:700px;height:700px;background:#173A6E;opacity:.55'></div>
<div class='blob' id='b2' style='width:520px;height:520px;background:#5A4520;opacity:.35'></div>
<div id='logo'>{lockup(1.25)}</div>
<div class='sc' id='s0' style='justify-content:center;padding-bottom:160px'>
  <div style='font-weight:800;font-size:76px;line-height:1.2;margin-bottom:60px' id='t0'>محامي وعدك يمحي<br>ديون الإجراء <span class='hl'>100%</span>؟</div>
  <div id='vis'>{PROMO}</div>
  <div class='heb' id='h0' style='margin-top:70px'>הבטיחו לכם מחיקת חובות 100%? ברחו.</div>
</div>
<div class='sc' id='s1' style='justify-content:center;padding-bottom:120px'>
  <div style='font-weight:900;font-size:96px;line-height:1.15' id='t1'>المحامي الصح<br><span class='hl'>بيحكيلك الحقيقة</span></div>
  <div class='heb' style='font-size:48px;margin:24px 0 30px' id='h1'>עורך דין אמיתי אומר לכם את האמת</div>
  {rows}
</div>
<div class='sc' id='s2' style='justify-content:center;padding-bottom:160px'>
  <div style='font-weight:900;font-size:300px;line-height:1;color:{GOLD};direction:ltr'><span id='cnt'>0</span>+</div>
  <div style='font-weight:800;font-size:90px;margin-top:10px'>سنة خبرة</div>
  <div style='width:0;height:4px;background:{GOLD};margin-top:40px' id='ln'></div>
  <div class='heb' style='margin-top:30px'>שנות ניסיון</div>
</div>
<div class='sc' id='s3' style='justify-content:center;padding-bottom:180px'>
  <div style='font-weight:900;font-size:120px;line-height:1.12' id='t3'>بدك الحقيقة<br><span class='hl'>عن ملفك؟</span></div>
  <div class='heb' style='margin-top:30px' id='h3'>רוצים לדעת את האמת על התיק? דברו איתנו.</div>
  <div style='font-size:46px;color:#D9D3C6;margin:70px 0 30px' id='p3'>ابعتلنا رقم الملف عالواتساب · בסודיות מלאה</div>
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
  // scene 0: question rises, promo pops in shiny, then the stamp slams down with a small shake
  up(document.getElementById('t0'),eo(cl((t-0.1)/0.6)));
  const pr=document.getElementById('promo'); const pp=eo(cl((t-0.5)/0.5));
  const sh=(t>1.9&&t<2.3)?Math.sin(t*90)*10*(2.3-t):0;
  pr.style.opacity=pp; pr.style.transform=`rotate(-3deg) scale(${{0.85+0.15*pp}}) translateX(${{sh}}px)`;
  const st=document.getElementById('stamp'); const ps=cl((t-1.8)/0.18);
  st.style.opacity=ps; st.style.transform=`rotate(-14deg) scale(${{2.2-1.2*eo(ps)}})`;
  up(document.getElementById('h0'),eo(cl((t-2.3)/0.6)));
  // scene 1: title, then each service row rises in turn
  up(document.getElementById('t1'),eo(cl((t-4.0)/0.7))); up(document.getElementById('h1'),eo(cl((t-4.3)/0.7)));
  for(let k=0;k<4;k++) up(document.getElementById('r'+k),eo(cl((t-4.8-k*0.65)/0.7)),70);
  // scene 2: years count up smoothly, gold line draws
  document.getElementById('cnt').textContent=Math.round(20*io(cl((t-8.8)/1.1)));
  document.getElementById('ln').style.width=(io(cl((t-9.0)/1.0))*520)+'px';
  // scene 3: call to action, WhatsApp button breathes; logo steps aside
  up(document.getElementById('t3'),eo(cl((t-10.8)/0.7))); up(document.getElementById('h3'),eo(cl((t-11.1)/0.7)));
  up(document.getElementById('p3'),eo(cl((t-11.4)/0.7)));
  const w=document.getElementById('wa'); const pw=eo(cl((t-11.7)/0.7)); w.style.opacity=pw;
  w.style.transform=`scale(${{(0.9+0.1*pw)*(t>12.4?1+0.035*Math.sin((t-12.4)*5):1)}})`;
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
while t < 14.5:
    add("sine=f=58:d=0.2,afade=t=out:d=0.2,volume=0.9", int(t * 1000)); t += 0.5
for f in (196.0, 246.9, 293.7):
    add(f"sine=f={f}:d=10.2,afade=t=in:d=1.2,afade=t=out:st=9:d=1.2,volume=0.06", 0)
for a, _ in SC[1:]:
    add("anoisesrc=d=0.6:c=pink:a=0.25,lowpass=f=2500,afade=t=in:d=0.3,afade=t=out:st=0.3:d=0.3,volume=0.35", int((a - 0.3) * 1000))
for k in range(4): add("sine=f=784:d=0.12,afade=t=out:d=0.12,volume=0.25", int((4.8 + k * 0.65) * 1000))
add("anoisesrc=d=0.25:c=brown:a=0.9,lowpass=f=400,afade=t=out:d=0.25,volume=1.2", 1800); add("sine=f=70:d=0.35,afade=t=out:d=0.35,volume=1.0", 1800)
for k in range(12): add("sine=f=1200:d=0.03,afade=t=out:d=0.03,volume=0.18", int((8.8 + 1.1 * k / 12) * 1000))
for f, d in ((392, 0), (494, 80), (587, 160), (784, 240)): add(f"sine=f={f}:d=3.2,afade=t=out:d=3.2,volume=0.2", 10600 + d)
filt = ";".join(parts) + ";" + "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.9,apad=whole_dur={DUR},atrim=0:{DUR}"
A = ROOT / "out" / "debt-direct.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-filter_complex", filt, "-ar", "44100", "-ac", "2", str(A)], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FR / "f%04d.jpg"), "-i", str(A),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                "-shortest", "-movflags", "+faststart", str(OUT / "video-direct-9x16.mp4")], check=True)
print(OUT / "video-direct-9x16.mp4")
