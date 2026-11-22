"""Carousel (reunification): تجديد تصريح الإقامة — 4 أشياء قبل التجديد. 6 slides 1080x1350."""
from common import *

W, H = 1080, 1350
OUT = REPO / "posts" / "2026-11-26-permit-renewal"
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
    ("ابلش <span class='hl'>بكّير</span>", "ما تستنى لآخر شهر. التجديد بياخد وقت، والتأخير ممكن يوقّف الملف.",
     "להתחיל מוקדם", "אל תחכו לחודש האחרון. החידוש לוקח זמן."),
    ("جهّز أوراق <span class='hl'>مركز الحياة</span>", "إيجار أو ملكية، أرنونا، قسائم راتب، مدارس الأولاد.",
     "מסמכי מרכז חיים", "חוזה, ארנונה, תלושי שכר, בתי ספר."),
    ("<span class='hl'>ترجم</span> وصدّق المستندات", "أي ورقة من برّا البلاد بدها ترجمة وتصديق حسب المطلوب.",
     "תרגום ואימות", "מסמך מחו״ל צריך תרגום ואימות לפי הדרישה."),
    ("رد على الداخلية <span class='hl'>بالموعد</span>", "كل رسالة إلها موعد. رد كامل من أول مرة بيوفّر عليك أشهر.",
     "לענות במועד", "לכל מכתב יש מועד. תשובה מלאה חוסכת חודשים."),
]

slides = []
# 1 — cover: a permit card with a calendar and an expiry warning
cover = f"""
<div style='position:absolute;top:380px;left:80px;width:380px;height:560px'>
  <div style='width:360px;height:230px;background:{CREAM};border-radius:20px;box-shadow:0 24px 50px rgba(0,0,0,.45);transform:rotate(-7deg);padding:26px;position:relative'>
    <div style='width:90px;height:110px;background:#D5CDBD;border-radius:10px'></div>
    {''.join(f"<div style='position:absolute;left:140px;top:{40+i*34}px;height:12px;width:{w}px;background:#D5CDBD;border-radius:6px'></div>" for i,w in enumerate((180,150,170,120)))}
    <div style='position:absolute;bottom:18px;right:18px;background:{RED};color:#fff;font-weight:900;font-size:30px;padding:6px 16px;border-radius:10px'>ينتهي قريبًا</div>
  </div>
  <div style='position:absolute;top:250px;left:120px;width:220px;height:220px;background:#fff;border-radius:24px;box-shadow:0 20px 40px rgba(0,0,0,.4);overflow:hidden;transform:rotate(5deg)'>
    <div style='height:60px;background:{RED}'></div>
    <div style='font-weight:900;font-size:110px;color:{NAVY};text-align:center;line-height:150px'>30</div>
  </div>
</div>
<div style='position:absolute;top:210px;right:72px;left:72px'>
  <div style='display:inline-block;background:{GOLD};color:{NAVY};font-weight:800;font-size:44px;padding:14px 30px;border-radius:14px;transform:rotate(-2deg)'>تصريح الإقامة قرّب يخلص؟</div>
</div>
<div style='position:absolute;top:360px;right:72px;width:540px'>
  <div style='font-weight:900;font-size:100px;line-height:1.1;color:{CREAM}'>4 أشياء<br><span class='hl'>قبل التجديد</span></div>
</div>
<div class='hebox' style='position:absolute;top:1000px;right:72px;left:72px'>
  <div class='heh' style='font-size:48px'>חידוש היתר שהייה: 4 דברים לפני</div>
  <div class='hep'>שמרו את הפוסט</div>
</div>
<div style='position:absolute;top:1170px;right:72px;font-size:36px;font-weight:600;color:{CREAM}'>احفظ البوست قبل ما تقدّم 🔖</div>
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
  <div class='h' style='margin-top:60px;font-size:88px'>تجديد <span class='hl'>قريب</span>؟</div>
  <div class='p' style='margin-top:26px;font-size:46px'>بنفحص معك الأوراق <b style='color:{CREAM}'>قبل</b> ما تقدّم.</div>
  <div class='heh' style='margin-top:44px;font-size:42px'>נבדוק איתכם את המסמכים לפני ההגשה.</div>
  <div style='margin:70px auto 0;display:inline-flex;align-items:center;gap:22px;background:{GOLD};color:{NAVY};border-radius:999px;padding:24px 56px'>
    <span style='font-weight:700;font-size:36px'>واتساب · וואטסאפ</span>
    <span style='font-weight:900;font-size:56px;direction:ltr'>{PHONE}</span>
  </div>
  <div style='margin-top:40px;font-size:30px;color:#AFB8C8'>خبرة +20 سنة · חיפה · עפולה</div>
</div>"""
slides.append(frame(N, cta, swipe=False))

render_all([(html, OUT / f"slide-{i+1}.png") for i, html in enumerate(slides)], W, H)
print(OUT)
