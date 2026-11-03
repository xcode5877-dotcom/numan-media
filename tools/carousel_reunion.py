"""Carousel: 5 أغلاط بتأخّر لمّ الشمل — 7 slides 1080x1350, Arabic + Hebrew."""
from common import *

W, H = 1080, 1350
OUT = REPO / "posts" / "2026-11-05-reunion-mistakes"
N = 7

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
    ("تتأخّروا <span class='hl'>بالتجديد</span>", "قدّموا طلب التجديد بوقت كافي قبل ما يخلص التصريح. تصريح منتهي بيعمل مشاكل بالملف كله.",
     "לא להגיש חידוש בזמן", "מגישים חידוש מבעוד מועד, לפני שהאשרה פגה."),
    ("ما تثبتوا <span class='hl'>مركز الحياة</span>", "عقد بيت أو إيجار، فواتير، شغل، مدارس الأولاد. كلها إثباتات إنكم عايشين هون فعلاً.",
     "לא להוכיח מרכז חיים", "חוזה דירה, חשבונות, עבודה, בית ספר לילדים."),
    ("مستندات <span class='hl'>ناقصة</span>", "شهادة الزواج والوثائق الرسمية لازم تكون كاملة، ومصدّقة ومترجمة حسب المطلوب.",
     "מסמכים חסרים או לא מתורגמים", "תעודת נישואין ומסמכים רשמיים — מלאים, מאומתים ומתורגמים."),
    ("تردّوا على الداخلية <span class='hl'>بدون استشارة</span>", "كل رسالة طلب مستندات أو رفض إلها موعد للرد. الرد الصح بالوقت الصح بيفرق.",
     "להגיב למשרד הפנים בלי ייעוץ", "לכל מכתב יש מועד תגובה. תגובה נכונה בזמן — עושה את ההבדל."),
    ("تقدّموا <span class='hl'>بدون خطة</span>", "كل عيلة إلها مسار مختلف حسب وضع الزوج أو الزوجة. خطة واضحة من الأول بتوفّر وقت ومشاكل.",
     "להגיש בלי תוכנית", "לכל משפחה מסלול אחר. תוכנית ברורה מההתחלה חוסכת זמן ובעיות."),
]

slides = []
# 1 — cover with a "rejected" stamped document as the visual hook
cover = f"""
<div style='position:absolute;top:210px;right:72px;left:72px'>
  <div style='display:inline-block;background:{GOLD};color:{NAVY};font-weight:800;font-size:44px;padding:14px 30px;border-radius:14px;transform:rotate(-2deg)'>زوجك أو زوجتك من برّا البلاد؟</div>
</div>
<div style='position:absolute;top:330px;left:90px;width:330px;height:420px;background:{CREAM};border-radius:14px;transform:rotate(-7deg);box-shadow:0 30px 60px rgba(0,0,0,.45);padding:44px 36px'>
  <div style='height:16px;width:60%;background:#C9C2B3;border-radius:8px'></div>
  {''.join(f"<div style='height:12px;width:{w}%;background:#DDD6C8;border-radius:6px;margin-top:22px'></div>" for w in (95,80,90,70,85,60,88,75))}
  <div style='position:absolute;top:150px;left:20px;border:7px solid {RED};color:{RED};font-family:Heebo;font-weight:900;font-size:70px;padding:4px 26px;transform:rotate(-18deg);border-radius:10px;opacity:.92'>נדחה</div>
</div>
<div style='position:absolute;top:400px;right:72px;width:600px'>
  <div style='font-weight:900;font-size:170px;line-height:1;color:{GOLD};white-space:nowrap'>5 أغلاط</div>
  <div class='h' style='font-size:92px;margin-top:10px'>بتأخّر<br><span class='hl'>لمّ الشمل</span></div>
</div>
<div class='hebox' style='position:absolute;top:1000px;right:72px;left:72px'>
  <div class='heh' style='font-size:48px'>5 טעויות שמעכבות איחוד משפחות</div>
  <div class='hep'>שמרו את הפוסט לפני שמגישים</div>
</div>
<div style='position:absolute;top:1175px;right:72px;font-size:36px;font-weight:600;color:{CREAM}'>احفظوا البوست قبل ما تقدّموا 🔖</div>
"""
slides.append(frame(1, cover))

for k, (h, p, heh, hep) in enumerate(MISTAKES, start=1):
    inner = f"""
<div style='position:absolute;top:210px;right:72px'><div class='num'>0{k}</div></div>
<div style='position:absolute;top:500px;right:72px;left:72px'>
  <div style='font-size:34px;font-weight:600;color:{GOLD};margin-bottom:18px'>غلطة رقم {k}</div>
  <div class='h'>{h}</div>
  <div class='p' style='margin-top:34px'>{p}</div>
  <div class='hebox' style='margin-top:56px'><div class='heh'>{heh}</div><div class='hep'>{hep}</div></div>
</div>"""
    slides.append(frame(k + 1, inner))

cta = f"""
<div style='position:absolute;top:240px;right:72px;left:72px;text-align:center'>
  <div style='display:flex;justify-content:center'>{mark(220)}</div>
  <div class='h' style='margin-top:60px;font-size:88px'>عندك ملف <span class='hl'>لمّ شمل</span>؟</div>
  <div class='p' style='margin-top:26px;font-size:46px'>احكي معنا <b style='color:{CREAM}'>قبل</b> ما تقدّم، مش بعد الرفض.</div>
  <div class='heh' style='margin-top:44px;font-size:42px'>יש לכם תיק איחוד משפחות? דברו איתנו לפני ההגשה.</div>
  <div style='margin:70px auto 0;display:inline-flex;align-items:center;gap:22px;background:{GOLD};color:{NAVY};border-radius:999px;padding:24px 56px'>
    <span style='font-weight:700;font-size:36px'>واتساب · וואטסאפ</span>
    <span style='font-weight:900;font-size:56px;direction:ltr'>{PHONE}</span>
  </div>
  <div style='margin-top:40px;font-size:30px;color:#AFB8C8'>خبرة +20 سنة · חיפה · עפולה</div>
</div>"""
slides.append(frame(N, cta, swipe=False))

render_all([(html, OUT / f"slide-{i+1}.png") for i, html in enumerate(slides)], W, H)
print(OUT)
