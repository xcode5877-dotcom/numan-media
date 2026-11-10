"""Carousel (debts axis): وصلتك رسالة من הוצאה לפועל؟ — 6 slides 1080x1350, Arabic + Hebrew."""
from common import *

W, H = 1080, 1350
OUT = REPO / "posts" / "2026-11-12-debt-letter"
N = 6

CSS = f"""
.s{{position:absolute;inset:0;background:{NAVY};overflow:hidden}}
.glow{{position:absolute;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,{NAVY2} 0%,transparent 70%);top:-250px;left:-300px}}
.top{{position:absolute;top:64px;right:72px;left:72px;display:flex;justify-content:space-between;align-items:center}}
.cnt{{font-family:Rubik;font-weight:500;font-size:28px;color:{GOLD};direction:ltr;letter-spacing:2px}}
.swipe{{position:absolute;bottom:70px;left:72px;font-size:30px;font-weight:600;color:{GOLD};display:flex;gap:14px;align-items:center}}
.num{{font-family:Rubik;font-weight:900;font-size:300px;line-height:.8;color:transparent;-webkit-text-stroke:3px {GOLD};direction:ltr}}
.h{{font-weight:800;font-size:92px;line-height:1.18;color:{CREAM}}}
.p{{font-weight:400;font-size:47px;line-height:1.5;color:#D9D3C6}}
.hebox{{border-right:5px solid {GOLD};padding:6px 26px 6px 0}}
.heh{{font-family:Heebo;font-weight:700;font-size:44px;color:{GOLD};line-height:1.3}}
.hep{{font-family:Heebo;font-weight:400;font-size:35px;color:#AFB8C8;line-height:1.45;margin-top:6px}}
"""

def frame(i, inner, swipe=True):
    sw = "<div class='swipe'><span>اسحب</span><span class='he' style='font-weight:500'>החליקו</span><span style='font-size:40px'>←</span></div>" if swipe else ""
    return page(f"<div class='s'><div class='glow'></div><div class='top'>{lockup(1.0)}<div class='cnt'>{i}/{N}</div></div>{inner}{sw}</div>", W, H, CSS)

MISTAKES = [
    ("شو هي <span class='hl'>الرسالة</span>؟", "رسالة بتبلّغك إنه انفتح ملف ضدك بدائرة الإجراء على دين.",
     "מה זה המכתב?", "הודעה על פתיחת תיק נגדכם בהוצאה לפועל בגלל חוב."),
    ("ليش <span class='hl'>ما تتجاهلها</span>؟", "الملف بيكمل حتى لو ما رديت، وممكن يوصل لحجز حساب أو راتب أو منع سفر.",
     "למה לא להתעלם?", "התיק ממשיך גם בלי תגובה, ועלול להגיע לעיקול חשבון, משכורת או עיכוב יציאה."),
    ("شو <span class='hl'>خياراتك</span>؟", "حسب وضعك: فحص الملف، فحص إذا في مجال للاعتراض، أو ترتيب تسوية ودفعات.",
     "מה האפשרויות?", "לפי המצב: בדיקת התיק, בדיקת אפשרות להתנגדות, או הסדר ותשלומים."),
    ("<span class='hl'>أول خطوة</span>", "صوّر الرسالة وابعتها قبل ما تعمل أي إشي.",
     "הצעד הראשון", "צלמו את המכתב ושלחו לנו לפני שעושים משהו."),
]

slides = []
# 1 — cover: a sealed envelope sliding into a drawer
cover = f"""
<div style='position:absolute;top:470px;left:70px;width:420px;height:300px;background:#5A4632;border-radius:16px;box-shadow:0 30px 60px rgba(0,0,0,.5)'>
  <div style='position:absolute;inset:26px 26px auto 26px;height:60px;background:#3E2F21;border-radius:10px'></div>
  <div style='position:absolute;top:44px;left:50%;width:90px;height:14px;margin-left:-45px;background:{GOLD};border-radius:7px'></div>
</div>
<div style='position:absolute;top:330px;left:110px;width:340px;height:220px;background:{CREAM};border-radius:12px;transform:rotate(-9deg);box-shadow:0 20px 40px rgba(0,0,0,.4)'>
  <div style='position:absolute;inset:0;clip-path:polygon(0 0,50% 55%,100% 0);background:#E2DACA;border-radius:12px'></div>
  <div style='position:absolute;bottom:26px;left:22px;border:6px solid {RED};color:{RED};font-family:Heebo;font-weight:900;font-size:40px;padding:2px 16px;transform:rotate(-8deg);border-radius:8px'>הוצאה לפועל</div>
</div>
<div style='position:absolute;top:210px;right:72px;left:72px'>
  <div style='display:inline-block;background:{GOLD};color:{NAVY};font-weight:800;font-size:44px;padding:14px 30px;border-radius:14px;transform:rotate(-2deg)'>وصلتك رسالة من הוצאה לפועל؟</div>
</div>
<div style='position:absolute;top:360px;right:72px;width:520px'>
  <div style='font-weight:900;font-size:120px;line-height:1.05;color:{CREAM}'>لا تخبّيها<br><span class='hl'>بالجارور</span></div>
</div>
<div class='hebox' style='position:absolute;top:900px;right:72px;left:72px'>
  <div class='heh' style='font-size:48px'>קיבלתם מכתב מההוצאה לפועל? אל תשאירו אותו במגירה</div>
  <div class='hep'>4 דברים שחשוב לדעת לפני שפועלים</div>
</div>
<div style='position:absolute;top:1130px;right:72px;font-size:36px;font-weight:600;color:{CREAM}'>4 أشياء لازم تعرفها · احفظ البوست 🔖</div>
"""
slides.append(frame(1, cover))

for k, (h, p, heh, hep) in enumerate(MISTAKES, start=1):
    inner = f"""
<div style='position:absolute;top:210px;right:72px'><div class='num'>0{k}</div></div>
<div style='position:absolute;top:500px;right:72px;left:72px'>
  <div style='font-size:34px;font-weight:600;color:{GOLD};margin-bottom:18px'>{k} من 4</div>
  <div class='h'>{h}</div>
  <div class='p' style='margin-top:34px'>{p}</div>
  <div class='hebox' style='margin-top:56px'><div class='heh'>{heh}</div><div class='hep'>{hep}</div></div>
</div>"""
    slides.append(frame(k + 1, inner))

cta = f"""
<div style='position:absolute;top:240px;right:72px;left:72px;text-align:center'>
  <div style='display:flex;justify-content:center'>{mark(220)}</div>
  <div class='h' style='margin-top:60px;font-size:88px'>عليك <span class='hl'>ملف إجراء</span>؟</div>
  <div class='p' style='margin-top:26px;font-size:46px'>احكي معنا بسرّية تامة، <b style='color:{CREAM}'>قبل</b> ما يكبر الملف.</div>
  <div class='heh' style='margin-top:44px;font-size:42px'>יש לכם תיק בהוצאה לפועל? דברו איתנו בדיסקרטיות.</div>
  <div style='margin:70px auto 0;display:inline-flex;align-items:center;gap:22px;background:{GOLD};color:{NAVY};border-radius:999px;padding:24px 56px'>
    <span style='font-weight:700;font-size:36px'>واتساب · וואטסאפ</span>
    <span style='font-weight:900;font-size:56px;direction:ltr'>{PHONE}</span>
  </div>
  <div style='margin-top:40px;font-size:30px;color:#AFB8C8'>خبرة +20 سنة · חיפה · עפולה</div>
</div>"""
slides.append(frame(N, cta, swipe=False))

render_all([(html, OUT / f"slide-{i+1}.png") for i, html in enumerate(slides)], W, H)
print(OUT)
