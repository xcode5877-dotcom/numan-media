"""Q&A reel (Saturday slot): a question arrives in an Instagram question sticker -> 3 animated answer steps with icons -> end card.
Topic: travel ban from Hotza'ah LaPoal before Umrah / holidays. Smooth ease-in-out motion, Hebrew subtitle line per step.
1080x1920, 30fps, 20s. Output: posts/2026-11-14-qa-travel-ban/reel.mp4"""
import json, shutil, subprocess
from playwright.sync_api import sync_playwright
from common import *

OUT = REPO / "posts" / "2026-11-14-qa-travel-ban"; OUT.mkdir(parents=True, exist_ok=True)
FR = ROOT / "out" / "qa-travel-frames"; shutil.rmtree(FR, ignore_errors=True); FR.mkdir(parents=True)
FPS, DUR = 30, 20.0

PLANE = """<svg viewBox="0 0 24 24" width="120" height="120"><path fill="currentColor" d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z"/></svg>"""
SEARCH = """<svg viewBox="0 0 24 24" width="120" height="120"><path fill="currentColor" d="M10 2a8 8 0 0 1 6.3 12.9l5.4 5.4-1.4 1.4-5.4-5.4A8 8 0 1 1 10 2zm0 2a6 6 0 1 0 0 12 6 6 0 0 0 0-12z"/></svg>"""
DOC = """<svg viewBox="0 0 24 24" width="120" height="120"><path fill="currentColor" d="M6 2h9l5 5v15H6zm8 1.5V8h4.5zM8 12v2h10v-2zm0 4v2h7v-2z"/></svg>"""

STEPS = [  # icon, arabic, hebrew, start
    (PLANE, "إذا في <span class='hl'>منع سفر</span> فعّال، بيوقّفوك بالمطار حتى لو التذكرة محجوزة.", "עיכוב יציאה פעיל = עוצרים אותך בשדה, גם עם כרטיס.", 5.6),
    (SEARCH, "<span class='hl'>افحص قبل</span> ما تحجز: في ملف بالإجراء؟ في منع سفر؟", "בדקו לפני שמזמינים: יש תיק? יש עיכוב יציאה?", 9.0),
    (DOC, "حسب الملف، في حالات بنقدر <span class='hl'>نقدّم طلب</span> لإلغاء المنع أو للسماح بالسفر.", "לפי התיק, לעיתים אפשר להגיש בקשה לביטול או להיתר יציאה.", 12.4),
]
END = (15.6, 16.4)

CSS = f"""
#bg{{position:absolute;inset:0;background:radial-gradient(circle at 70% 20%,{NAVY2} 0%,{NAVY} 60%)}}
#top{{position:absolute;top:110px;right:70px;left:70px;display:flex;justify-content:space-between;align-items:center}}
#lbl{{font-weight:800;font-size:40px;color:{GOLD};letter-spacing:1px}}
#q{{position:absolute;top:330px;left:90px;right:90px;border-radius:44px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.45);transform-origin:center top}}
#q .h{{background:linear-gradient(90deg,#F58529,#DD2A7B,#8134AF);color:#fff;font-weight:700;font-size:44px;text-align:center;padding:30px}}
#q .b{{background:#fff;color:#111;font-weight:700;font-size:62px;line-height:1.35;text-align:center;padding:50px 50px 56px;min-height:220px}}
#qhe{{position:absolute;top:840px;left:90px;right:90px;text-align:center;font-family:Heebo;font-weight:500;font-size:42px;color:#C8D0DD}}
.st{{position:absolute;left:80px;right:80px;display:flex;gap:40px;align-items:flex-start}}
.ic{{flex:none;width:170px;height:170px;border-radius:44px;background:{GOLD};color:{NAVY};display:flex;align-items:center;justify-content:center}}
.tx{{font-weight:800;font-size:60px;line-height:1.35;color:{CREAM}}}
.he2{{font-family:Heebo;font-weight:500;font-size:38px;color:#AFB8C8;margin-top:14px;line-height:1.35}}
#warn{{position:absolute;bottom:110px;left:80px;right:80px;text-align:center;font-size:34px;color:#AFB8C8}}
#end{{position:absolute;inset:0;background:{NAVY};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding-bottom:140px}}
#wa{{display:inline-flex;align-items:center;gap:24px;background:{GOLD};color:{NAVY};border-radius:36px;padding:32px 56px;margin-top:70px}}
"""
WA = """<svg viewBox="0 0 32 32" width="86" height="86"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-3.9-.5-5.6-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.8 5.1 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.1-.3-.2-.6-.3z"/></svg>"""
Q = "عليّ ملف بالإجراء… بقدر أسافر عالعمرة؟"
QHE = "יש לי תיק בהוצאה לפועל… אני יכול לטוס?"

steps_html = "".join(
    f"<div class='st' id='s{i}' style='top:{600 + i*400}px'><div class='ic'>{ic}</div><div><div class='tx'>{ar}</div><div class='he2'>{he}</div></div></div>"
    for i, (ic, ar, he, _) in enumerate(STEPS))

BODY = f"""<div style='position:fixed;inset:0;overflow:hidden'>
<div id='bg'></div>
<div id='top'>{lockup(0.9)}<div id='lbl'>سألتونا · שאלתם</div></div>
<div id='q'><div class='h'>اسأل المحامي · שאלו את עורך הדין</div><div class='b' id='qt'></div></div>
<div id='qhe'>{QHE}</div>
{steps_html}
<div id='warn'>كل ملف إله وضعه، والجواب الدقيق بعد فحص الملف.</div>
<div id='end'>
  {mark(230)}
  <div style='font-family:FRL;font-weight:500;font-size:90px;margin-top:40px'>נעמאן עבדאללה</div>
  <div style='font-family:Heebo;font-size:32px;letter-spacing:.4em;color:{GOLD};margin-top:12px'>משרד עורכי דין</div>
  <div style='font-weight:900;font-size:84px;line-height:1.2;margin-top:90px'>مسافر قريب؟<br><span class='hl'>افحص معنا قبل.</span></div>
  <div style='font-family:Heebo;font-weight:700;font-size:46px;color:{GOLD};margin-top:28px'>טסים בקרוב? בדקו איתנו קודם.</div>
  <div id='wa'>{WA}<span style='font-weight:900;font-size:72px;direction:ltr;white-space:nowrap'>{PHONE}</span></div>
</div>
</div>
<script>
const Q={json.dumps(Q, ensure_ascii=False)}; const S={json.dumps([s[3] for s in STEPS])}; const EN={list(END)};
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)); const io=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2; const eo=x=>1-Math.pow(1-x,3);
window.render=function(t){{
  const pq=eo(cl((t-0.3)/0.7)); const q=document.getElementById('q');
  // sticker pops in, question types itself, then the sticker lifts and shrinks to the top to make room
  const lift=io(cl((t-4.6)/0.9));
  q.style.opacity=pq; q.style.transform=`translateY(${{(1-pq)*80 - lift*100}}px) scale(${{(0.9+0.1*pq)*(1-0.32*lift)}})`;
  const n=Math.floor(Q.length*cl((t-1.0)/2.2)); document.getElementById('qt').textContent=Q.slice(0,n)+(t<3.4&&(Math.floor(t*3)%2)?'|':'');
  const qh=document.getElementById('qhe'); const ph=eo(cl((t-3.3)/0.6)); qh.style.opacity=ph*(1-lift); qh.style.transform=`translateY(${{(1-ph)*30}}px)`;
  S.forEach((s,i)=>{{ const e=document.getElementById('s'+i); const k=eo(cl((t-s)/0.6));
    e.style.opacity=k; e.style.transform=`translateX(${{(1-k)*-120}}px)`;
    e.querySelector('.ic').style.transform=`scale(${{0.6+0.4*eo(cl((t-s-0.1)/0.5))}}) rotate(${{(1-k)*-12}}deg)`; }});
  const w=document.getElementById('warn'); w.style.opacity=eo(cl((t-14.0)/0.6));
  const pe=io(cl((t-EN[0])/(EN[1]-EN[0]))); const en=document.getElementById('end'); en.style.opacity=pe; en.style.transform=`scale(${{1.04-0.04*pe}})`;
  document.getElementById('wa').style.transform=`scale(${{t>EN[1]?1+0.03*Math.sin((t-EN[1])*4):1}})`;
}};
</script>"""
HTML = page(BODY, 1080, 1920, CSS)

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(HTML, wait_until="load"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    for i in range(int(DUR * FPS)):
        pg.evaluate(f"render({i/FPS})"); pg.screenshot(path=str(FR / f"f{i:04d}.jpg"), type="jpeg", quality=90)
    b.close()

# Sound: soft pad (minor -> major at the end card), sticker pop, key clicks while the question types, a soft chime per step.
parts, labels = [], []
def add(expr, ms):
    lab = f"s{len(labels)}"; parts.append(f"{expr},adelay={ms}|{ms}[{lab}]"); labels.append(f"[{lab}]")
for f in (220.0, 261.6, 329.6): add(f"sine=f={f}:d=16,afade=t=in:d=1.5,afade=t=out:st=14.5:d=1.5,volume=0.07", 0)
for f in (261.6, 329.6, 392.0): add(f"sine=f={f}:d=4.6,afade=t=in:d=1,afade=t=out:st=3.4:d=1.2,volume=0.08", int(END[0]*1000))
add("sine=f=880:d=0.1,afade=t=out:d=0.1,volume=0.4", 300); add("sine=f=1320:d=0.08,afade=t=out:d=0.08,volume=0.25", 360)
k = 1.0
while k < 3.2: add("anoisesrc=d=0.025:c=white:a=0.25,highpass=f=2500,afade=t=out:d=0.025,volume=0.22", int(k*1000)); k += 0.14
for s in [st[3] for st in STEPS]: add("sine=f=1046:d=0.5,afade=t=out:d=0.5,volume=0.18", int(s*1000)); add("sine=f=1568:d=0.4,afade=t=out:d=0.4,volume=0.12", int(s*1000)+70)
for f, d in ((523, 0), (659, 100), (784, 200)): add(f"sine=f={f}:d=2.2,afade=t=out:d=2.2,volume=0.2", int(END[0]*1000) + d)
filt = ";".join(parts) + ";" + "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.9,apad=whole_dur={DUR},atrim=0:{DUR}"
A = ROOT / "out" / "qa-travel.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-filter_complex", filt, "-ar", "44100", "-ac", "2", str(A)], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FR / "f%04d.jpg"), "-i", str(A),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                "-shortest", "-movflags", "+faststart", str(OUT / "reel.mp4")], check=True)
print(OUT / "reel.mp4")
