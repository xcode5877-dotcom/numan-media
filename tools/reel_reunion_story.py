"""Story reel: a couple's WhatsApp chat about the reunification file -> they message the office -> the office replies.
Smooth, phone-native motion (ease-in-out slides, soft message pops), Hebrew subtitles under each message.
1080x1920, 30fps, 25s. Output: ads/reunion-whatsapp/video-9x16.mp4"""
import json, shutil, subprocess
from playwright.sync_api import sync_playwright
from common import *

OUT = REPO / "ads" / "reunion-whatsapp"; OUT.mkdir(parents=True, exist_ok=True)
FR = ROOT / "out" / "reunion-story-frames"; shutil.rmtree(FR, ignore_errors=True); FR.mkdir(parents=True)
FPS, DUR = 30, 25.0
GREEN, WA_BG = "#0B5C4E", "#EFE7DB"

# chat, who, text, hebrew subtitle, typing_start, appear, clock
MSGS = [
    ("A", "her", "شفت رسالة الداخلية؟", "ראית את המכתב ממשרד הפנים?", 3.5, 4.1, "22:48"),
    ("A", "her", "بدهم مستندات كمان…", "הם רוצים עוד מסמכים…", 4.5, 5.3, "22:48"),
    ("A", "me", "عادي، بنقدّم لحالنا", "זה בסדר, נגיש לבד", 5.9, 7.5, "22:49"),
    ("A", "her", "آخر مرة رجّعوا الملف لأنه كان ناقص", "בפעם הקודמת החזירו את התיק כי היה חסר", 8.0, 9.4, "22:49"),
    ("A", "her", "خلينا نسأل حدا بفهم", "בוא נשאל מישהו שמבין", 10.0, 10.9, "22:50"),
    ("A", "me", "معك حق ♥", "את צודקת ♥", 11.5, 12.6, "22:50"),
    ("B", "me", "مرحبا، عندي ملف لمّ شمل وبدي استشارة", "שלום, יש לי תיק איחוד משפחות ואני צריך ייעוץ", 14.3, 16.1, "22:52"),
    ("B", "her", "أهلاً وسهلاً، ابعتلنا صورة الرسالة ومنحكي معك بكرا الصبح.", "שלחו לנו צילום של המכתב ונדבר מחר בבוקר.", 16.7, 18.4, "22:53"),
]
UNLOCK, SWITCH, END = (2.7, 3.3), (13.0, 13.7), (19.6, 20.4)

CSS = f"""
.scr{{position:absolute;inset:0;overflow:hidden}}
#lock{{background:linear-gradient(180deg,#24344F 0%,#0C1424 100%);z-index:5}}
#clock{{position:absolute;top:330px;width:100%;text-align:center;font-family:Heebo;font-weight:300;font-size:220px;color:#fff;direction:ltr}}
#date{{position:absolute;top:300px;width:100%;text-align:center;font-family:Heebo;font-size:44px;color:#C8D0DD}}
#nt{{position:absolute;left:50px;right:50px;top:620px;background:rgba(245,245,247,.95);border-radius:44px;padding:34px 40px;color:#111;box-shadow:0 20px 50px rgba(0,0,0,.35)}}
#nt .a{{display:flex;justify-content:space-between;font-size:32px;color:#666}} #nt .t{{font-weight:700;font-size:46px;margin-top:10px}} #nt .b{{font-size:40px;margin-top:6px;color:#333}}
#hook{{position:absolute;top:1080px;left:70px;right:70px;text-align:center}}
.tag{{display:inline-block;background:{GOLD};color:{NAVY};font-weight:800;font-size:72px;line-height:1.25;padding:24px 46px;border-radius:26px;box-shadow:0 20px 40px rgba(0,0,0,.3)}}
.tagh{{font-family:Heebo;font-weight:700;font-size:48px;color:#fff;margin-top:30px}}
.chat{{background:{WA_BG}}}
.bar{{position:absolute;top:0;left:0;right:0;height:250px;background:{GREEN};color:#fff;display:flex;align-items:flex-end;gap:28px;padding:0 50px 38px}}
.av{{width:110px;height:110px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none}}
.bar b{{display:block;font-size:48px;font-weight:600;color:#fff}} .st{{font-size:34px;opacity:.85}}
.msgs{{position:absolute;top:250px;bottom:560px;left:44px;right:44px;display:flex;flex-direction:column;justify-content:flex-end;gap:22px;overflow:hidden}}
.m{{color:#1A2B29;max-width:840px;padding:26px 36px 16px;font-size:50px;line-height:1.38;border-radius:36px;box-shadow:0 2px 0 rgba(0,0,0,.06)}}
.her{{align-self:flex-start;background:#fff;border-top-right-radius:8px;transform-origin:top right}}
.me{{align-self:flex-end;background:#D3F3C4;border-top-left-radius:8px;transform-origin:top left}}
.m i{{display:block;font-style:normal;font-size:27px;color:#7A8784;text-align:left;margin-top:4px;direction:ltr}}
.tick{{color:#3BA0E6;font-weight:700}}
.typing{{align-self:flex-start;background:#fff;border-radius:36px;padding:30px 40px;display:flex;gap:14px}}
.typing span{{width:20px;height:20px;border-radius:50%;background:#9AA5A3}}
.inp{{position:absolute;bottom:400px;left:36px;right:36px;height:124px;background:#fff;border-radius:62px;display:flex;align-items:center;padding:0 48px;font-size:44px;color:#9AA5A3;box-shadow:0 4px 10px rgba(0,0,0,.08)}}
.inp.on{{color:#1A2B29}}
.sub{{position:absolute;bottom:250px;left:60px;right:60px;text-align:center}}
.sub span{{display:inline-block;background:rgba(11,26,46,.88);color:#fff;font-family:Heebo;font-weight:500;font-size:40px;line-height:1.35;padding:14px 30px;border-radius:18px}}
#end{{background:{NAVY};z-index:6;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding-bottom:140px}}
#wa{{display:inline-flex;align-items:center;gap:24px;background:{GOLD};color:{NAVY};border-radius:36px;padding:32px 56px;margin-top:70px}}
"""
WA = """<svg viewBox="0 0 32 32" width="86" height="86"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-3.9-.5-5.6-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.8 5.1 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.1-.3-.2-.6-.3z"/></svg>"""

def chat(cid, name, avatar):
    return f"""<div class='scr chat' id='c{cid}'>
<div class='bar'>{avatar}<div><b>{name}</b><span class='st' id='st{cid}'>متصل الآن</span></div></div>
<div class='msgs' id='m{cid}'></div>
<div class='inp' id='in{cid}'><span id='it{cid}'>اكتب رسالة</span></div>
<div class='sub' id='sb{cid}'></div></div>"""

BODY = f"""<div style='position:fixed;inset:0;overflow:hidden'>
{chat('A', 'زوجتي ♥', "<div class='av' style='background:#F0A04B;color:#fff;font-weight:700;font-size:52px'>ر</div>")}
{chat('B', 'مكتب المحامي نعمان عبدالله', f"<div class='av' style='background:{NAVY}'>{mark(78)}</div>")}
<div class='scr' id='lock'><div id='date'>יום רביעי, 4 בנובמבר</div><div id='clock'>22:47</div>
  <div id='nt'><div class='a'><span>تذكير · תזכורת</span><span>الآن</span></div>
  <div class='t'>تجديد تصريح الإقامة</div><div class='b'>بعد 14 يوم · בעוד 14 יום</div></div>
  <div id='hook'><div class='tag'>تصريح زوجتي<br>قرّب يخلص…</div><div class='tagh'>ההיתר של אשתי עומד לפוג…</div></div>
</div>
<div class='scr' id='end'>
  {mark(230)}
  <div style='font-family:FRL;font-weight:500;font-size:90px;margin-top:40px'>נעמאן עבדאללה</div>
  <div style='font-family:Heebo;font-size:32px;letter-spacing:.4em;color:{GOLD};margin-top:12px'>משרד עורכי דין</div>
  <div style='font-weight:900;font-size:86px;line-height:1.2;margin-top:90px'>ملف لمّ شمل؟<br><span class='hl'>احكي معنا.</span></div>
  <div style='font-family:Heebo;font-weight:700;font-size:46px;color:{GOLD};margin-top:28px'>תיק איחוד משפחות? דברו איתנו.</div>
  <div id='wa'>{WA}<span style='font-weight:900;font-size:72px;direction:ltr;white-space:nowrap'>{PHONE}</span></div>
</div>
</div>
<script>
const M={json.dumps(MSGS, ensure_ascii=False)}; const UN={list(UNLOCK)}, SW={list(SWITCH)}, EN={list(END)};
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)); const io=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2; const eo=x=>1-Math.pow(1-x,3);
window.render=function(t){{
  // lock screen: notification eases in, hook rises softly, unlock slides the screen up
  const nt=document.getElementById('nt'); const pn=eo(cl((t-0.3)/0.6)); nt.style.opacity=pn; nt.style.transform=`translateY(${{(1-pn)*-80}}px)`;
  const hk=document.getElementById('hook'); const ph=eo(cl((t-0.6)/0.7)); hk.style.opacity=ph; hk.style.transform=`translateY(${{(1-ph)*60}}px)`;
  const pu=io(cl((t-UN[0])/(UN[1]-UN[0]))); const lk=document.getElementById('lock'); lk.style.transform=`translateY(${{-pu*100}}%)`; lk.style.opacity=1-pu*0.3;
  // chat switch: A slides out to the right, B slides in from the left (RTL navigation feel)
  const ps=io(cl((t-SW[0])/(SW[1]-SW[0])));
  document.getElementById('cA').style.transform=`translateX(${{ps*35}}%)`; document.getElementById('cA').style.filter=`brightness(${{1-ps*0.35}})`;
  document.getElementById('cB').style.transform=`translateX(${{(1-ps)*-100}}%)`;
  for(const C of ['A','B']){{
    let html='', typing=false, sub='';
    for(const [c,who,txt,he,ts,ta,clk] of M){{ if(c!==C) continue;
      if(t>=ta){{ const k=eo(cl((t-ta)/0.35)); const tick=who==='me'?" <span class='tick'>✓✓</span>":"";
        html+=`<div class='m ${{who}}' style='opacity:${{k}};transform:translateY(${{(1-k)*30}}px) scale(${{0.94+0.06*k}})'>${{txt}}<i>${{clk}}${{tick}}</i></div>`; sub=he; }}
      else if(who==='her' && t>=ts){{ typing=true; const ph2=t*6;
        html+=`<div class='typing'>${{[0,1,2].map(i=>`<span style='transform:translateY(${{-9*Math.max(0,Math.sin(ph2-i*0.9))}}px)'></span>`).join('')}}</div>`; }}
    }}
    document.getElementById('m'+C).innerHTML=html;
    document.getElementById('st'+C).textContent=typing?'يكتب…':'متصل الآن';
    const sb=document.getElementById('sb'+C); sb.innerHTML=sub?`<span>${{sub}}</span>`:'';
    // my own messages get typed into the input bar first
    const mine=M.filter(m=>m[0]===C&&m[1]==='me'&&t>=m[4]&&t<m[5]); const it=document.getElementById('it'+C), inp=document.getElementById('in'+C);
    if(mine.length){{ const m=mine[0]; const n=Math.floor(m[2].length*cl((t-m[4])/(m[5]-m[4]-0.2))); it.textContent=m[2].slice(0,n)+((Math.floor(t*3)%2)?'|':''); inp.classList.add('on'); }}
    else {{ it.textContent='اكتب رسالة'; inp.classList.remove('on'); }}
  }}
  // end card: soft fade + gentle zoom, WhatsApp button breathes
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

# Sound: a warm, quiet pad under everything (minor -> major at the office reply), notification chime, soft pops, key clicks.
parts, labels = [], []
def add(expr, ms):
    lab = f"s{len(labels)}"; parts.append(f"{expr},adelay={ms}|{ms}[{lab}]"); labels.append(f"[{lab}]")
for f in (220.0, 261.6, 329.6):  # A minor pad, 0-16.5s
    add(f"sine=f={f}:d=16.5,afade=t=in:d=1.5,afade=t=out:st=15:d=1.5,volume=0.07", 0)
for f in (261.6, 329.6, 392.0):  # C major pad, from the office reply
    add(f"sine=f={f}:d=8.5,afade=t=in:d=1.2,afade=t=out:st=7:d=1.5,volume=0.08", 16500)
add("sine=f=1046:d=0.12,afade=t=out:d=0.12,volume=0.45", 300); add("sine=f=1568:d=0.2,afade=t=out:d=0.2,volume=0.3", 410)
add("anoisesrc=d=0.4:c=pink:a=0.3,lowpass=f=3000,afade=t=in:d=0.2,afade=t=out:st=0.2:d=0.2,volume=0.35", int(UNLOCK[0] * 1000))
add("anoisesrc=d=0.4:c=pink:a=0.3,lowpass=f=3000,afade=t=in:d=0.2,afade=t=out:st=0.2:d=0.2,volume=0.35", int(SWITCH[0] * 1000))
for c, who, txt, he, ts, ta, clk in MSGS:
    ms = int(ta * 1000)
    if who == "her": add("sine=f=880:d=0.08,afade=t=out:d=0.08,volume=0.35", ms); add("sine=f=1320:d=0.06,afade=t=out:d=0.06,volume=0.22", ms + 55)
    else:
        add("anoisesrc=d=0.18:c=white:a=0.25,highpass=f=1500,afade=t=in:d=0.06,afade=t=out:st=0.06:d=0.12,volume=0.35", ms)
        k = ts
        while k < ta - 0.2:
            add("anoisesrc=d=0.025:c=white:a=0.25,highpass=f=2500,afade=t=out:d=0.025,volume=0.25", int(k * 1000)); k += 0.15
for f, d in ((523, 0), (659, 100), (784, 200)): add(f"sine=f={f}:d=2.2,afade=t=out:d=2.2,volume=0.2", int(END[0] * 1000) + d)
filt = ";".join(parts) + ";" + "".join(labels) + f"amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.9,apad=whole_dur={DUR},atrim=0:{DUR}"
A = ROOT / "out" / "reunion-story.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-filter_complex", filt, "-ar", "44100", "-ac", "2", str(A)], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FR / "f%04d.jpg"), "-i", str(A),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                "-shortest", "-movflags", "+faststart", str(OUT / "video-story-9x16.mp4")], check=True)
print(OUT / "video-story-9x16.mp4")
