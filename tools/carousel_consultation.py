"""Carousel (how we work): كيف بتصير الاستشارة عنا؟ — 6 slides 1080x1350, Arabic + Hebrew."""
from common import *

W, H = 1080, 1350
OUT = REPO / "posts" / "2026-11-15-how-consultation-works"
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
    ("رسالة <span class='hl'>واتساب</span>", "بتبعتلنا شو صاير معك بكم كلمة، وإذا في رسالة أو إشعار، صوّره وابعته.",
     "הודעת וואטסאפ", "כותבים לנו בכמה מילים מה קרה, ושולחים צילום של המכתב אם יש."),
    ("<span class='hl'>موعد</span> يناسبك", "بمكتب حيفا، بمكتب العفولة، أو مكالمة تلفون إذا أريح إلك.",
     "פגישה שנוחה לכם", "במשרד בחיפה, בעפולה, או בשיחת טלפון."),
    ("<span class='hl'>فحص</span> الملف", "بنقرأ الأوراق معك، وبنفهم وين واقف الملف بالزبط، بسرّية تامة.",
     "בדיקת התיק", "עוברים איתכם על המסמכים ומבינים איפה התיק עומד, בדיסקרטיות מלאה."),
    ("الخيارات <span class='hl'>بوضوح</span>", "بتطلع وانت عارف شو خياراتك، وشو الخطوة الجاية، وقديش بتاخد.",
     "האפשרויות, בבהירות", "יוצאים עם תמונה ברורה: מה האפשרויות, מה הצעד הבא וכמה זמן זה לוקח."),
]

slides = []
# 1 — cover: a phone with a WhatsApp chat bubble from the office
cover = f"""
<div style='position:absolute;top:340px;left:80px;width:340px;height:660px;background:#111C2E;border:10px solid #2A3A55;border-radius:56px;box-shadow:0 30px 60px rgba(0,0,0,.5);transform:rotate(-6deg);overflow:hidden'>
  <div style='height:96px;background:#0B5C4E;display:flex;align-items:center;gap:14px;padding:0 20px'>
    <div style='width:54px;height:54px;border-radius:50%;background:{NAVY};display:flex;align-items:center;justify-content:center'>{mark(38)}</div>
    <div style='color:#fff;font-size:22px;font-weight:600'>مكتب المحامي</div></div>
  <div style='background:#EFE7DB;position:absolute;top:96px;bottom:0;left:0;right:0;padding:26px 18px;display:flex;flex-direction:column;gap:16px'>
    <div style='align-self:flex-end;background:#D3F3C4;color:#1A2B29;font-size:24px;line-height:1.35;padding:14px 18px;border-radius:20px'>مرحبا، بدي استشارة</div>
    <div style='align-self:flex-start;background:#fff;color:#1A2B29;font-size:24px;line-height:1.35;padding:14px 18px;border-radius:20px'>أهلاً، احكيلنا شو صاير ومنحدد موعد 🤝</div>
  </div>
</div>
<div style='position:absolute;top:210px;right:72px;left:72px'>
  <div style='display:inline-block;background:{GOLD};color:{NAVY};font-weight:800;font-size:44px;padding:14px 30px;border-radius:14px;transform:rotate(-2deg)'>أول مرة بتحكي مع محامي؟</div>
</div>
<div style='position:absolute;top:380px;right:72px;width:540px'>
  <div style='font-weight:900;font-size:112px;line-height:1.08;color:{CREAM}'>كيف بتصير<br><span class='hl'>الاستشارة</span><br>عنا؟</div>
</div>
<div class='hebox' style='position:absolute;top:1010px;right:72px;left:72px'>
  <div class='heh' style='font-size:48px'>איך נראית פגישת ייעוץ אצלנו?</div>
  <div class='hep'>4 צעדים פשוטים, בדיסקרטיות מלאה</div>
</div>
<div style='position:absolute;top:1170px;right:72px;font-size:36px;font-weight:600;color:{CREAM}'>4 خطوات بسيطة، بسرّية تامة</div>
"""
slides.append(frame(1, cover))

for k, (h, p, heh, hep) in enumerate(MISTAKES, start=1):
    inner = f"""
<div style='position:absolute;top:210px;right:72px'><div class='num'>0{k}</div></div>
<div style='position:absolute;top:500px;right:72px;left:72px'>
  <div style='font-size:34px;font-weight:600;color:{GOLD};margin-bottom:18px'>خطوة {k}</div>
  <div class='h'>{h}</div>
  <div class='p' style='margin-top:34px'>{p}</div>
  <div class='hebox' style='margin-top:56px'><div class='heh'>{heh}</div><div class='hep'>{hep}</div></div>
</div>"""
    slides.append(frame(k + 1, inner))

cta = f"""
<div style='position:absolute;top:240px;right:72px;left:72px;text-align:center'>
  <div style='display:flex;justify-content:center'>{mark(220)}</div>
  <div class='h' style='margin-top:60px;font-size:88px'>جاهز <span class='hl'>للخطوة الأولى</span>؟</div>
  <div class='p' style='margin-top:26px;font-size:46px'>ديون ودائرة الإجراء، منع سفر، لمّ شمل وإقامة. ابعتلنا رسالة.</div>
  <div class='heh' style='margin-top:44px;font-size:42px'>הוצאה לפועל, עיכוב יציאה, איחוד משפחות. שלחו הודעה.</div>
  <div style='margin:70px auto 0;display:inline-flex;align-items:center;gap:22px;background:{GOLD};color:{NAVY};border-radius:999px;padding:24px 56px'>
    <span style='font-weight:700;font-size:36px'>واتساب · וואטסאפ</span>
    <span style='font-weight:900;font-size:56px;direction:ltr'>{PHONE}</span>
  </div>
  <div style='margin-top:40px;font-size:30px;color:#AFB8C8'>خبرة +20 سنة · חיפה · עפולה</div>
</div>"""
slides.append(frame(N, cta, swipe=False))

render_all([(html, OUT / f"slide-{i+1}.png") for i, html in enumerate(slides)], W, H)
print(OUT)
