"""Reel: وصلتك رسالة من الداخلية؟ — lock-screen notification, then 3 things to know, end card. 1080x1920, 30fps, ~15.5s."""
import shutil, subprocess
from playwright.sync_api import sync_playwright
from common import *

OUT = REPO / "posts" / "2026-11-06-interior-letter"
FR = ROOT / "out" / "interior-letter-frames"
shutil.rmtree(FR, ignore_errors=True); FR.mkdir(parents=True)
FPS, DUR = 30, 15.5
ITEMS = [  # (arabic, hebrew, appear)
    ("شو <span class='hl'>المطلوب</span> بالزبط", "מה בדיוק נדרש", 5.0),
    ("قديش عندك <span class='hl'>وقت</span> للرد", "כמה זמן יש לכם להגיב", 6.9),
    ("شو بصير إذا <span class='hl'>تأخّرت</span>", "מה קורה אם מאחרים", 8.8),
]

CSS = f"""
#lock{{position:absolute;inset:0;background:linear-gradient(180deg,#1B2B44 0%,#0A1220 100%)}}
#clock{{position:absolute;top:330px;width:100%;text-align:center;font-family:Heebo;font-weight:300;font-size:220px;color:#fff;direction:ltr;letter-spacing:-4px}}
#date{{position:absolute;top:300px;width:100%;text-align:center;font-family:Heebo;font-size:44px;color:#C8D0DD}}
.nt{{position:absolute;left:50px;right:50px;background:rgba(245,245,247,.94);border-radius:44px;padding:34px 40px;font-family:Heebo;color:#111;direction:rtl;box-shadow:0 20px 50px rgba(0,0,0,.35)}}
.nt .a{{display:flex;justify-content:space-between;font-size:32px;color:#555}}
.nt .t{{font-weight:700;font-size:44px;margin-top:10px}}
.nt .b{{font-size:40px;line-height:1.35;margin-top:6px;color:#222}}
#hook{{position:absolute;top:1150px;left:60px;right:60px;text-align:center}}
.tag{{display:inline-block;background:{GOLD};color:{NAVY};font-weight:900;font-size:84px;line-height:1.2;padding:22px 48px;border-radius:26px;transform:rotate(-2deg);box-shadow:0 20px 40px rgba(0,0,0,.35)}}
.tagh{{font-family:Heebo;font-weight:700;font-size:52px;color:#fff;margin-top:34px;text-shadow:0 4px 12px rgba(0,0,0,.6)}}
#list{{position:absolute;inset:0;background:{NAVY};opacity:0}}
#ttl{{position:absolute;top:330px;right:80px;left:80px;font-weight:900;font-size:100px;line-height:1.15}}
#ttlh{{position:absolute;top:600px;right:80px;font-family:Heebo;font-weight:700;font-size:50px;color:{GOLD}}}
.it{{position:absolute;right:80px;left:80px;display:flex;gap:36px;align-items:flex-start;transform-origin:right center}}
.n{{flex:none;width:130px;height:130px;border-radius:50%;border:4px solid {GOLD};color:{GOLD};font-weight:900;font-size:78px;display:flex;align-items:center;justify-content:center}}
.ia{{font-weight:800;font-size:76px;line-height:1.2}}
.ih{{font-family:Heebo;font-weight:500;font-size:44px;color:#AFB8C8;margin-top:10px}}
#end{{position:absolute;inset:0;background:{NAVY};opacity:0;text-align:center}}
"""
items_html = "".join(
    f"<div class='it' id='i{k}' style='top:{790+k*300}px;opacity:0'><div class='n'>{k+1}</div><div><div class='ia'>{a}</div><div class='ih'>{h}</div></div></div>"
    for k, (a, h, _) in enumerate(ITEMS))

BODY = f"""
<div id='lock'><div id='date'>יום רביעי, 4 בנובמבר</div><div id='clock'>21:04</div>
  <div class='nt' id='n1' style='top:-300px'><div class='a'><span>משרד הפנים</span><span>עכשיו</span></div>
    <div class='t'>עדכון בבקשה לאיחוד משפחות</div><div class='b'>נדרשים מסמכים נוספים להמשך הטיפול בבקשתך.</div></div>
  <div class='nt' id='n2' style='top:-300px'><div class='a'><span>משרד הפנים</span><span>עכשיו</span></div>
    <div class='t'>תזכורת</div><div class='b'>יש להגיש את המסמכים עד המועד שנקבע.</div></div>
  <div id='hook'><div class='tag'>وصلتك رسالة<br>من الداخلية؟</div><div class='tagh'>קיבלתם מכתב ממשרד הפנים?</div></div>
</div>
<div id='list'>
  <div id='ttl'>قبل ما تردّ،<br><span class='hl'>اعرف 3 أشياء:</span></div>
  <div id='ttlh'>לפני שעונים — 3 דברים:</div>
  {items_html}
</div>
<div id='end'>
  <div style='margin-top:380px;display:flex;justify-content:center'>{mark(300)}</div>
  <div style='font-family:FRL;font-weight:500;font-size:96px;margin-top:50px'>נעמאן עבדאללה</div>
  <div style='font-family:Heebo;font-size:34px;letter-spacing:.4em;color:{GOLD};margin-top:14px'>משרד עורכי דין</div>
  <div style='font-weight:800;font-size:68px;line-height:1.35;margin-top:110px'>ملف لمّ شمل؟<br>احكي معنا <span class='hl'>قبل</span> ما تردّ.</div>
  <div style='font-family:Heebo;font-weight:700;font-size:44px;color:{GOLD};margin-top:30px'>תיק איחוד משפחות? דברו איתנו לפני שעונים.</div>
  <div style='margin:70px auto 0;display:inline-flex;gap:22px;align-items:center;background:{GOLD};color:{NAVY};border-radius:999px;padding:26px 60px'>
    <span style='font-weight:700;font-size:38px'>واتساب</span><span style='font-weight:900;font-size:66px;direction:ltr'>{PHONE}</span></div>
</div>
<script>
const IT={[t for *_, t in ITEMS]};
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const ob=x=>{{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);}};
const eo=x=>1-Math.pow(1-x,3);
window.render=function(t){{
  const n1=document.getElementById('n1'),n2=document.getElementById('n2');
  n1.style.top=(t<1?-300:-300+(560+300)*eo(cl((t-1)/0.35)))+'px';
  n2.style.top=(t<2.6?-300:-300+(860+300)*eo(cl((t-2.6)/0.35)))+'px';
  const sh=(t>1.35&&t<1.8)?Math.sin(t*90)*8*(1-(t-1.35)/0.45):0; n1.style.transform=`translateX(${{sh}}px)`;
  const hk=document.getElementById('hook'); const hs=t<0.25?0.6:0.6+0.4*ob(cl((t-0.25)/0.3)); hk.style.transform=`scale(${{hs}})`; hk.style.opacity=t<0.25?0:1;
  document.getElementById('lock').style.filter=t>3.9?`blur(${{cl((t-3.9)/0.3)*12}}px)`:'none';
  const L=document.getElementById('list'); L.style.opacity=cl((t-4.0)/0.25);
  IT.forEach((a,k)=>{{const e=document.getElementById('i'+k);const p=cl((t-a)/0.3);e.style.opacity=p>0?1:0;e.style.transform=`translateX(${{(1-eo(p))*-120}}px) scale(${{0.8+0.2*ob(p)}})`;}});
  document.getElementById('end').style.opacity=cl((t-11.3)/0.3);
}};
</script>"""
HTML = page(BODY, 1080, 1920, CSS)

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(HTML, wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    for i in range(int(DUR * FPS)):
        pg.evaluate(f"render({i/FPS})")
        pg.screenshot(path=str(FR / f"f{i:04d}.jpg"), type="jpeg", quality=90)
    b.close()

parts, labels = [], []
def add(expr, ms):
    lab = f"s{len(labels)}"; parts.append(f"{expr},adelay={ms}|{ms}[{lab}]"); labels.append(f"[{lab}]")
for ms in (1000, 2600):  # notification chime
    add("sine=f=1046:d=0.12,afade=t=out:d=0.12,volume=0.5", ms); add("sine=f=1568:d=0.18,afade=t=out:d=0.18,volume=0.35", ms + 110)
add("sine=f=180:d=0.25,afade=t=out:d=0.25,volume=0.9", 300)  # hook thump
add("anoisesrc=d=0.35:c=pink:a=0.5,highpass=f=700,afade=t=in:d=0.15,afade=t=out:st=0.15:d=0.2,volume=0.6", 3950)  # whoosh
for _, _, a in ITEMS:
    add("sine=f=660:d=0.1,afade=t=out:d=0.1,volume=0.45", int(a * 1000)); add("sine=f=990:d=0.08,afade=t=out:d=0.08,volume=0.3", int(a * 1000) + 70)
for f, d in ((392, 0), (494, 90), (587, 180), (784, 270)):
    add(f"sine=f={f}:d=1.8,afade=t=out:d=1.8,volume=0.25", 11300 + d)
filt = ";".join(parts) + ";" + "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,apad=whole_dur={DUR},atrim=0:{DUR}"
OUT.mkdir(parents=True, exist_ok=True)
A = ROOT / "out" / "interior-letter.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-filter_complex", filt, "-ar", "44100", "-ac", "2", str(A)], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FR / "f%04d.jpg"), "-i", str(A),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                "-shortest", "-movflags", "+faststart", str(OUT / "reel.mp4")], check=True)
print(OUT / "reel.mp4")
