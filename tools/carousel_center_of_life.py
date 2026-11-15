"""Carousel (reunification): مركز الحياة — شو هو وكيف بتثبته؟ — 6 slides 1080x1350, Arabic + Hebrew."""
from common import *

W, H = 1080, 1350
OUT = REPO / "posts" / "2026-11-19-center-of-life"
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
    ("شو يعني <span class='hl'>مركز الحياة</span>؟", "الداخلية بدها تتأكد إنه البيت والشغل والعيلة هون فعلاً، مش بس عنوان على الورق.",
     "מה זה מרכז חיים?", "משרד הפנים רוצה לראות שהבית, העבודה והמשפחה באמת כאן."),
    ("<span class='hl'>البيت</span>", "عقد إيجار أو ملكية، أرنونا، فواتير كهربا وميّ باسمكم.",
     "הבית", "חוזה שכירות או בעלות, ארנונה, חשבונות חשמל ומים."),
    ("<span class='hl'>الشغل</span> والدخل", "قسائم راتب، كشوفات بنك، أو تقارير شغل مستقل.",
     "עבודה והכנסה", "תלושי שכר, דפי בנק, או דוחות עצמאי."),
    ("<span class='hl'>العيلة</span> والحياة اليومية", "مدارس وروضات الأولاد، صندوق المرضى، والتأمين الوطني.",
     "המשפחה והחיים", "בתי ספר וגנים, קופת חולים, ביטוח לאומי."),
]

slides = []
# 1 — cover: a house with a family-file folder and a check stamp
cover = f"""
<div style='position:absolute;top:360px;left:80px;width:380px;height:560px'>
  <svg viewBox="0 0 200 200" width="380" height="380" style='color:{GOLD};display:block'>
    <path fill="currentColor" d="M100 20 L190 95 H165 V180 H35 V95 H10 Z"/>
    <rect x="82" y="120" width="36" height="60" fill="{NAVY}"/><rect x="50" y="110" width="22" height="22" fill="{NAVY}"/><rect x="128" y="110" width="22" height="22" fill="{NAVY}"/>
  </svg>
  <div style='position:absolute;top:300px;left:60px;width:280px;height:200px;background:{CREAM};border-radius:12px;transform:rotate(-6deg);box-shadow:0 20px 40px rgba(0,0,0,.45);padding:28px'>
    {''.join(f"<div style='height:12px;width:{w}%;background:#D5CDBD;border-radius:6px;margin-top:18px'></div>" for w in (80,92,70,85))}
    <div style='position:absolute;top:40px;left:150px;width:100px;height:100px;border-radius:50%;border:7px solid #2E8B57;color:#2E8B57;font-size:64px;font-weight:900;display:flex;align-items:center;justify-content:center;transform:rotate(-12deg)'>✓</div>
  </div>
</div>
<div style='position:absolute;top:210px;right:72px;left:72px'>
  <div style='display:inline-block;background:{GOLD};color:{NAVY};font-weight:800;font-size:44px;padding:14px 30px;border-radius:14px;transform:rotate(-2deg)'>عندك ملف لمّ شمل؟</div>
</div>
<div style='position:absolute;top:360px;right:72px;width:560px'>
  <div style='font-weight:900;font-size:96px;line-height:1.12;color:{CREAM}'><span class='hl'>مركز الحياة</span><br>شو هو، وكيف<br>بتثبته؟</div>
</div>
<div class='hebox' style='position:absolute;top:1000px;right:72px;left:72px'>
  <div class='heh' style='font-size:48px'>מרכז חיים: מה זה ואיך מוכיחים?</div>
  <div class='hep'>שמרו לפני שמגישים חידוש</div>
</div>
<div style='position:absolute;top:1170px;right:72px;font-size:36px;font-weight:600;color:{CREAM}'>احفظ البوست قبل التجديد 🔖</div>
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
  <div class='h' style='margin-top:60px;font-size:88px'>ملفك <span class='hl'>جاهز</span>؟</div>
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
