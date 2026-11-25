"""Carousel (how we work): 4 أسئلة اسألها لأي محامي قبل ما توكّله. 6 slides 1080x1350."""
from common import *

W, H = 1080, 1350
OUT = REPO / "posts" / "2026-11-29-questions-for-lawyer"
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
    ("فحصت <span class='hl'>ملفي</span> قبل ما تحكيلي النتيجة؟", "المحامي الجدّي بيقرأ الأوراق أول، وبعدين بيحكي.",
     "בדקת את התיק לפני שאמרת תוצאה?", "עורך דין רציני קורא קודם, מדבר אחר כך."),
    ("شو <span class='hl'>الخيارات</span> عندي؟", "مش طريق واحد. اسأل عن كل الخيارات ومخاطر كل وحدة.",
     "מה האפשרויות שלי?", "לא דרך אחת. שאלו על כל האפשרויות והסיכונים."),
    ("قديش <span class='hl'>بتاخد</span> وقت؟", "جواب صريح عن المدة بيوفّر عليك قلق وخيبة أمل.",
     "כמה זמן זה לוקח?", "תשובה כנה על הזמן חוסכת אכזבה."),
    ("قديش <span class='hl'>التكلفة</span>، ومكتوبة؟", "اتفاق أتعاب واضح ومكتوب من الأول.",
     "כמה זה עולה, ובכתב?", "הסכם שכר טרחה ברור וכתוב מההתחלה."),
]

slides = []
# 1 — cover: a big question mark with a checklist
cover = f"""
<div style='position:absolute;top:360px;left:70px;width:400px;height:600px'>
  <div style='font-weight:900;font-size:520px;line-height:1;color:{GOLD};opacity:.9;text-align:center'>؟</div>
  <div style='position:absolute;bottom:20px;left:30px;width:330px;background:{CREAM};border-radius:20px;padding:26px 28px;box-shadow:0 20px 40px rgba(0,0,0,.45);transform:rotate(-5deg)'>
    {''.join(f"<div style='display:flex;align-items:center;gap:16px;margin:12px 0'><div style='width:34px;height:34px;border:5px solid {NAVY};border-radius:8px;color:#2E8B57;font-size:30px;font-weight:900;line-height:24px;text-align:center'>✓</div><div style='height:12px;flex:1;background:#D5CDBD;border-radius:6px'></div></div>" for _ in range(4))}
  </div>
</div>
<div style='position:absolute;top:210px;right:72px;left:72px'>
  <div style='display:inline-block;background:{GOLD};color:{NAVY};font-weight:800;font-size:44px;padding:14px 30px;border-radius:14px;transform:rotate(-2deg)'>قبل ما توكّل محامي</div>
</div>
<div style='position:absolute;top:360px;right:72px;width:540px'>
  <div style='font-weight:900;font-size:100px;line-height:1.1;color:{CREAM}'>4 أسئلة<br><span class='hl'>اسألها</span><br>لأي محامي</div>
</div>
<div class='hebox' style='position:absolute;top:1000px;right:72px;left:72px'>
  <div class='heh' style='font-size:48px'>4 שאלות לשאול כל עורך דין</div>
  <div class='hep'>לפני שחותמים על ייפוי כוח</div>
</div>
<div style='position:absolute;top:1170px;right:72px;font-size:36px;font-weight:600;color:{CREAM}'>احفظ البوست وابعته لحدا بيحتاجه 🔖</div>
"""
slides.append(frame(1, cover))

for k, (h, p, heh, hep) in enumerate(MISTAKES, start=1):
    inner = f"""
<div style='position:absolute;top:210px;right:72px'><div class='num'>0{k}</div></div>
<div style='position:absolute;top:500px;right:72px;left:72px'>
  <div style='font-size:34px;font-weight:600;color:{GOLD};margin-bottom:18px'>سؤال {k}</div>
  <div class='h'>{h}</div>
  <div class='p' style='margin-top:34px'>{p}</div>
  <div class='hebox' style='margin-top:56px'><div class='heh'>{heh}</div><div class='hep'>{hep}</div></div>
</div>"""
    slides.append(frame(k + 1, inner))

cta = f"""
<div style='position:absolute;top:240px;right:72px;left:72px;text-align:center'>
  <div style='display:flex;justify-content:center'>{mark(220)}</div>
  <div class='h' style='margin-top:60px;font-size:88px'>هيك <span class='hl'>منشتغل</span> عنا</div>
  <div class='p' style='margin-top:26px;font-size:46px'>وكل سؤال إله جواب واضح <b style='color:{CREAM}'>قبل</b> ما توقّع.</div>
  <div class='heh' style='margin-top:44px;font-size:42px'>אצלנו לכל שאלה יש תשובה ברורה לפני החתימה.</div>
  <div style='margin:70px auto 0;display:inline-flex;align-items:center;gap:22px;background:{GOLD};color:{NAVY};border-radius:999px;padding:24px 56px'>
    <span style='font-weight:700;font-size:36px'>واتساب · וואטסאפ</span>
    <span style='font-weight:900;font-size:56px;direction:ltr'>{PHONE}</span>
  </div>
  <div style='margin-top:40px;font-size:30px;color:#AFB8C8'>خبرة +20 سنة · חיפה · עפולה</div>
</div>"""
slides.append(frame(N, cta, swipe=False))

render_all([(html, OUT / f"slide-{i+1}.png") for i, html in enumerate(slides)], W, H)
print(OUT)
