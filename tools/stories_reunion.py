"""Stories for the family-reunification week — 1080x1920. Sticker areas left empty for poll / question stickers added in the app."""
from common import *

W, H = 1080, 1920
D = REPO / "stories"
CSS = f"""
.s{{position:absolute;inset:0;background:{NAVY};overflow:hidden}}
.glow{{position:absolute;width:1200px;height:1200px;border-radius:50%;background:radial-gradient(circle,{NAVY2} 0%,transparent 70%);top:-300px;right:-400px}}
.logo{{position:absolute;top:250px;right:80px}}
.q{{font-weight:900;font-size:118px;line-height:1.12;color:{CREAM}}}
.he{{font-family:Heebo;font-weight:700;font-size:56px;color:{GOLD};line-height:1.3}}
.slot{{border:3px dashed rgba(201,164,92,.35);border-radius:40px;height:330px}}
"""
def st(body):
    return page(f"<div class='s'><div class='glow'></div><div class='logo'>{lockup(1.1)}</div>{body}</div>", W, H, CSS)

poll = st(f"""
<div style='position:absolute;top:520px;right:80px;left:80px'>
  <div style='display:inline-block;background:{GOLD};color:{NAVY};font-weight:800;font-size:46px;padding:12px 30px;border-radius:14px;transform:rotate(-2deg)'>سؤال سريع · שאלה קצרה</div>
  <div class='q' style='margin-top:50px'>زوجك أو زوجتك<br><span class='hl'>من برّا البلاد</span>؟</div>
  <div class='he' style='margin-top:40px'>בן או בת הזוג מחו״ל?</div>
  <div class='slot' style='margin-top:90px'></div>
</div>""")

ask = st(f"""
<div style='position:absolute;top:520px;right:80px;left:80px'>
  {mark(220)}
  <div class='q' style='margin-top:40px'>عندك سؤال عن<br><span class='hl'>لمّ الشمل</span>؟</div>
  <div style='font-size:52px;line-height:1.5;color:#D9D3C6;margin-top:36px'>اسألوا هون، والمحامي بجاوب بالستوري.</div>
  <div class='he' style='margin-top:30px;font-size:48px'>שאלה על איחוד משפחות? שאלו כאן.</div>
  <div class='slot' style='margin-top:70px'></div>
</div>""")

cover = (REPO / "posts/2026-11-05-reunion-mistakes/slide-1.png")
import base64
c64 = base64.b64encode(cover.read_bytes()).decode()
new = st(f"""
<div style='position:absolute;top:470px;right:80px;left:80px;text-align:center'>
  <div style='display:inline-block;background:{RED};color:#fff;font-weight:800;font-size:48px;padding:12px 34px;border-radius:999px'>بوست جديد · פוסט חדש</div>
  <img src='data:image/png;base64,{c64}' style='display:block;margin:70px auto 0;width:680px;border-radius:28px;transform:rotate(3deg);box-shadow:0 40px 80px rgba(0,0,0,.5);border:4px solid {GOLD}'>
  <div style='font-weight:800;font-size:64px;margin-top:90px;color:{CREAM}'>اضغطوا وشوفوا قبل ما تقدّموا</div>
</div>""")

render_all([(poll, D / "2026-11-04-poll-spouse-abroad.png"),
            (ask, D / "2026-11-04-ask-reunion.png"),
            (new, D / "2026-11-05-new-reunion-mistakes.png")], W, H)
print("ok")
