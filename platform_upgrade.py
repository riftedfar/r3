"""EaseWithPy platform UI: course library, auth, dashboard, and extra-course routing."""
import sys, threading, time, html, traceback

def install():
    for _ in range(120):
        mod = sys.modules.get("app") or sys.modules.get("__main__")
        app = getattr(mod, "APP", None) if mod else None
        if app is None or not hasattr(mod, "COURSE") or not hasattr(mod, "layout"):
            time.sleep(0.25)
            continue
        try:
            from additional_courses import COURSES as LEGACY_EXTRA
            from course_registry import extra_courses
            EXTRA = extra_courses(mod.COURSE, LEGACY_EXTRA)
            from lesson_teaching import enrich_lessons
            enrich_lessons(EXTRA)
            from flask import abort, redirect, request, jsonify, Response

            def L(body, title="EaseWithPy"):
                return mod.layout(body, title)

            def all_courses():
                py={"slug":"python","title":"Python","tag":"PYTHON","description":"The complete beginner-to-builder Python path: syntax, data, functions, files, errors, OOP, modules, projects and more.","lessons":mod.COURSE,"href":"/course/python"}
                return [py]+[{"slug":c["slug"],"title":c["title"],"tag":c["tag"],"description":c["description"],"lessons":c["lessons"],"href":f"/course/{c['slug']}"} for c in EXTRA]

            def nav_auth():
                u=mod.user()
                if u:
                    return '<a class="navbtn" href="/dashboard">Dashboard</a><span class="userchip">Hi, '+html.escape(str(u["name"]))+'</span><form method="post" action="/logout" class="inline"><input type="hidden" name="csrf" value="'+html.escape(str(mod.csrf()))+'"><button class="ghost">Log out</button></form>'
                return '<a class="navbtn" href="/login">Log in</a><a class="navbtn primary" href="/register">Create account</a>'

            def layout(body,title="EaseWithPy",description="Interactive coding courses with lessons, labs, projects and progress tracking."):
                canonical=html.escape("https://easewithpy.de5.net" + request.path, quote=True)
                desc=html.escape(description[:160], quote=True)
                page_title=html.escape(title, quote=True)
                base=request.url_root.rstrip("/")
                return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{page_title} · EaseWithPy</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:site_name" content="EaseWithPy"><meta property="og:title" content="{page_title} · EaseWithPy"><meta property="og:description" content="{desc}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{html.escape(base + '/og.svg', quote=True)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{page_title} · EaseWithPy"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{html.escape(base + '/og.svg', quote=True)}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"EaseWithPy","url":{__import__('json').dumps(base)},"description":{__import__('json').dumps(description)}}}</script>
<style>
:root{{--bg:#0b0d0c;--panel:#111412;--panel2:#151916;--line:#303631;--line2:#454d47;--text:#eeeade;--muted:#9aa39b;--dim:#69716b;--accent:#b8ff57;--accent2:#8bd63d;--danger:#ff746b}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;overflow-x:hidden}}
body:before{{content:"";position:fixed;inset:0;pointer-events:none;z-index:-2;background:linear-gradient(90deg,rgba(184,255,87,.025),transparent 28%,transparent 72%,rgba(184,255,87,.018))}}
body:after{{content:"";position:fixed;inset:0;pointer-events:none;z-index:-1;opacity:.34;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:42px 42px;mask-image:linear-gradient(to bottom,#000 0%,rgba(0,0,0,.35) 48%,transparent 88%);animation:gridMove 24s linear infinite}}
a{{color:inherit;text-decoration:none}}
button,input,textarea,select{{font:inherit}}
button{{cursor:pointer}}
.top{{height:66px;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50;background:rgba(11,13,12,.96);display:flex;align-items:center;padding:0 4vw;gap:28px}}
.logo{{font-weight:950;font-size:21px;letter-spacing:-.065em;white-space:nowrap;display:inline-flex;gap:2px;align-items:center}}
.logo span{{color:var(--accent)}}
.logo:before{{content:"";width:7px;height:7px;background:var(--accent);display:inline-block;margin-right:7px;animation:logoPulse 2.6s ease-in-out infinite}}
.nav{{display:flex;align-items:center;gap:4px;margin-left:auto}}
.nav>a,.navbtn,.ghost{{padding:8px 11px;border:1px solid transparent;border-radius:6px;color:var(--muted);background:transparent}}
.nav>a:hover,.navbtn:hover,.ghost:hover{{color:var(--text);border-color:var(--line);background:var(--panel2)}}
.area-menu{{position:relative}}
.area-trigger{{padding:8px 12px;border:1px solid var(--line2);border-radius:6px;color:var(--text);background:var(--panel);font-weight:800;display:inline-flex;align-items:center;gap:7px}}
.area-trigger:hover{{border-color:var(--accent);color:var(--accent)}}
.area-chevron{{font-size:9px;color:var(--dim);transition:transform .2s}}
.area-menu.open .area-chevron{{transform:rotate(180deg)}}
.area-panel{{position:absolute;right:0;top:calc(100% + 9px);width:350px;max-width:calc(100vw - 24px);padding:8px;border:1px solid var(--line2);background:#0d100e;box-shadow:0 28px 70px rgba(0,0,0,.65);display:none;z-index:100}}
.area-menu.open .area-panel{{display:block;animation:panelIn .18s ease both}}
.area-label{{font-size:9px;letter-spacing:.18em;color:var(--dim);font-weight:900;padding:9px 10px 6px;text-transform:uppercase}}
.area-grid{{display:grid;grid-template-columns:1fr 1fr;gap:2px}}
.area-link{{display:flex!important;flex-direction:column;gap:3px;padding:10px!important;border:1px solid transparent!important;border-radius:4px!important;color:var(--muted)!important}}
.area-link b{{font-size:13px;color:var(--text)}}
.area-link span{{font-size:10px;color:var(--dim)}}
.area-link:hover{{background:#171b18!important;border-color:var(--line)!important;transform:translateX(3px)}}
.area-divider{{height:1px;background:var(--line);margin:7px 0}}
.area-menu .area-panel a{{display:block}}
.primary{{background:var(--accent)!important;color:#111!important;border-color:var(--accent)!important;font-weight:900}}
.userchip{{color:var(--text);font-size:13px;padding:8px 5px}}
.inline{{display:inline}}
.shell{{width:min(1180px,91vw);margin:auto}}
.hero{{min-height:620px;padding:84px 0 70px;display:grid;grid-template-columns:1.1fr .9fr;gap:70px;align-items:center;position:relative}}
.hero:before{{content:"";position:absolute;left:-18vw;top:18%;width:55vw;height:1px;background:var(--line);opacity:.55;animation:ruleSweep 8s ease-in-out infinite}}
.hero>div{{position:relative}}
.eyebrow{{font-size:10px;font-weight:900;letter-spacing:.19em;color:var(--accent);text-transform:uppercase}}
h1{{font-size:clamp(50px,7vw,94px);line-height:.9;letter-spacing:-.085em;margin:13px 0 24px;max-width:850px}}
h2{{letter-spacing:-.055em;font-size:clamp(28px,4vw,44px);margin:9px 0}}
h3{{letter-spacing:-.035em}}
p{{color:var(--muted);line-height:1.72}}
.hero p{{font-size:17px;max-width:620px}}
.actions{{display:flex;gap:8px;flex-wrap:wrap;margin-top:25px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--line2);background:var(--panel);padding:10px 14px;border-radius:6px;font-weight:800;position:relative;overflow:hidden;transition:transform .22s,border-color .22s,background .22s}}
.btn:hover{{transform:translateY(-2px);border-color:var(--accent)}}
.btn.primary:hover{{box-shadow:0 8px 28px rgba(184,255,87,.13)}}
.btn:after{{content:"";position:absolute;left:-100%;top:0;width:70%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.22),transparent);transform:skewX(-20deg);transition:left .55s}}
.btn:hover:after{{left:140%}}
.terminal{{border:1px solid var(--line2);background:#0d100e;border-radius:4px;padding:0;box-shadow:22px 22px 0 rgba(184,255,87,.045);overflow:hidden;animation:terminalIn .75s .12s both}}
.termhead{{height:38px;border-bottom:1px solid var(--line);display:flex;align-items:center;padding:0 13px;color:var(--dim);font:600 10px ui-monospace,monospace;letter-spacing:.08em}}
.termhead:before{{content:"";width:7px;height:7px;border:1px solid var(--accent);margin-right:8px}}
.code{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;white-space:pre-wrap;line-height:1.8;color:#d8ddd9;padding:24px;min-height:285px}}
.code:after{{content:"";display:inline-block;width:7px;height:15px;background:var(--accent);margin-left:3px;vertical-align:-2px;animation:cursorBlink .9s steps(1) infinite}}
.section{{padding:70px 0}}
.sectionhead{{display:flex;justify-content:space-between;gap:20px;align-items:end;margin-bottom:22px;border-bottom:1px solid var(--line);padding-bottom:16px}}
.sectionhead p{{margin:5px 0}}
.search{{width:100%;padding:14px 15px;border:1px solid var(--line);border-radius:5px;background:#0a0d0b;color:var(--text);outline:none;margin:8px 0 18px}}
.search:focus,input:focus,textarea:focus,select:focus{{border-color:var(--accent);box-shadow:0 0 0 2px rgba(184,255,87,.08)}}
.filters{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:18px}}
.filter{{border:1px solid var(--line);background:transparent;color:var(--muted);padding:7px 10px;border-radius:4px;cursor:pointer}}
.filter.active,.filter:hover{{background:var(--accent);color:#101410;border-color:var(--accent)}}
.cgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;border-top:1px solid var(--line);border-left:1px solid var(--line)}}
.coursecard{{min-height:285px;padding:22px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);background:rgba(15,18,16,.92);display:flex;flex-direction:column;position:relative;overflow:hidden;transition:background .25s,transform .35s,border-color .25s}}
.coursecard:before{{content:"";position:absolute;top:0;left:0;width:3px;height:0;background:var(--accent);transition:height .35s}}
.coursecard:after{{content:"";position:absolute;right:16px;top:17px;width:5px;height:5px;background:var(--line2);transition:background .25s}}
.coursecard:hover{{background:#151a16;transform:translateY(-5px);z-index:2}}
.coursecard:hover:before{{height:100%}}
.coursecard:hover:after{{background:var(--accent)}}
.tag{{font-size:9px;font-weight:900;letter-spacing:.15em;color:var(--accent);border:1px solid #3d493d;border-radius:3px;padding:4px 6px;width:max-content}}
.coursecard h3{{font-size:25px;margin:13px 0 7px}}
.coursecard p{{font-size:13px;margin:0 0 15px}}
.meta{{display:flex;justify-content:space-between;color:var(--dim);font:600 10px ui-monospace,monospace;margin-top:auto;margin-bottom:13px;text-transform:uppercase}}
.coursecard .btn{{width:max-content}}
.path{{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;border-top:1px solid var(--line);border-left:1px solid var(--line)}}
.step,.card{{border-right:1px solid var(--line);border-bottom:1px solid var(--line);background:#0f1210;border-radius:0;padding:20px;position:relative}}
.step:before{{content:"";position:absolute;left:0;top:0;width:100%;height:1px;background:var(--accent);transform:scaleX(0);transform-origin:left;transition:transform .4s}}
.step:hover:before{{transform:scaleX(1)}}
.step b{{display:block;margin-top:9px;font-size:17px}}
.step p{{font-size:12px;margin-bottom:0}}
.banner{{border:1px solid var(--line2);background:#111511;border-radius:3px;padding:25px;display:flex;justify-content:space-between;align-items:center;gap:20px;position:relative;overflow:hidden}}
.banner:before{{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent);animation:barPulse 3s ease-in-out infinite}}
footer{{border-top:1px solid var(--line);padding:30px 4vw;color:var(--dim);margin-top:45px;font-size:12px}}
.libraryhero{{padding:55px 0 20px}}.libraryhero h1{{font-size:clamp(44px,6vw,72px)}}
.catalog{{display:grid;grid-template-columns:230px 1fr;gap:20px}}
.side{{position:sticky;top:84px;height:max-content;border:1px solid var(--line);background:#0e110f;padding:13px}}
.side a{{display:block;padding:9px;color:var(--muted);border-left:2px solid transparent}}.side a:hover{{color:var(--text);border-left-color:var(--accent);background:#151915}}
.coursehero{{border:1px solid var(--line2);background:#101310;padding:27px;margin-bottom:16px;position:relative}}
.lessonrow{{display:flex;align-items:center;gap:14px;padding:14px;border-bottom:1px solid var(--line);background:#0c0f0d;margin:0;transition:padding-left .22s,background .22s}}
.lessonrow:first-of-type{{border-top:1px solid var(--line)}}.lessonrow:hover{{padding-left:20px;background:#141814}}
.num{{width:32px;height:32px;border:1px solid var(--line2);background:#151916;display:flex;align-items:center;justify-content:center;font:800 11px ui-monospace,monospace;flex:none;color:var(--accent)}}
.lessonrow small{{margin-left:auto;color:var(--dim)}}
.form{{max-width:500px;margin:70px auto 90px;border:1px solid var(--line2);background:#101310;padding:27px}}
.form h1{{font-size:43px;margin-bottom:10px}}
label{{display:block;margin:16px 0 7px;font-size:12px;color:var(--text)}}
input[type=text],input[type=email],input[type=password]{{width:100%;padding:13px;border:1px solid var(--line);border-radius:4px;background:#090c0a;color:var(--text);outline:none}}
.form button{{width:100%;margin-top:18px;padding:12px;border:1px solid var(--accent);background:var(--accent);color:#101410;border-radius:4px;font-weight:900}}
.hint{{font-size:12px;color:var(--dim)}}
.dash{{padding:50px 0}}.dashgrid{{display:grid;grid-template-columns:1fr 320px;gap:16px}}
.progress{{border:1px solid var(--line);background:#0f1210;padding:20px}}.bar{{height:5px;background:#252a26;overflow:hidden}}.bar i{{display:block;height:100%;background:var(--accent)}}
.statgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;margin:15px 0;border-top:1px solid var(--line);border-left:1px solid var(--line)}}
.stat{{border-right:1px solid var(--line);border-bottom:1px solid var(--line);padding:15px;background:#0f1210}}.stat strong{{font-size:24px;display:block}}.stat span{{color:var(--dim);font-size:11px}}
.reveal{{opacity:0;transform:translateY(24px);transition:opacity .65s ease,transform .65s cubic-bezier(.16,1,.3,1);transition-delay:var(--delay,0ms)}}
.reveal.visible{{opacity:1;transform:none}}
@keyframes gridMove{{to{{background-position:42px 42px}}}}
@keyframes logoPulse{{0%,100%{{box-shadow:0 0 0 0 rgba(184,255,87,0)}}50%{{box-shadow:0 0 0 5px rgba(184,255,87,.07)}}}}
@keyframes panelIn{{from{{opacity:0;transform:translateY(-6px)}}to{{opacity:1;transform:none}}}}
@keyframes ruleSweep{{0%,100%{{transform:translateX(-4%);opacity:.25}}50%{{transform:translateX(18%);opacity:.7}}}}
@keyframes terminalIn{{from{{opacity:0;transform:translateX(25px)}}to{{opacity:1;transform:none}}}}
@keyframes cursorBlink{{50%{{opacity:0}}}}
@keyframes barPulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
@media(max-width:850px){{
.top{{height:60px;padding:0 12px;gap:8px}}.logo{{font-size:18px}}.nav{{gap:4px}}.nav>a:not(.primary),.nav>form,.userchip{{display:none}}.area-trigger{{padding:8px 10px;font-size:12px}}
.area-panel{{position:fixed;top:66px;right:10px;left:10px;width:auto;max-width:none;max-height:calc(100vh - 78px);overflow:auto}}.area-grid{{grid-template-columns:1fr 1fr}}
.hero{{min-height:0;grid-template-columns:1fr;padding:55px 0 35px;gap:35px}}.hero h1{{font-size:clamp(44px,12vw,66px)}}.hero p{{font-size:15px}}.hero:before{{display:none}}
.cgrid{{grid-template-columns:1fr}}.path{{grid-template-columns:1fr 1fr}}.catalog,.dashgrid{{grid-template-columns:1fr}}.side{{position:static}}.banner{{align-items:flex-start;flex-direction:column}}.section{{padding:45px 0}}.shell{{width:min(94vw,760px)}}
.coursehero{{padding:20px}}.coursehero .actions{{display:grid;grid-template-columns:1fr}}.coursehero .actions .btn{{width:100%}}.lessonrow{{min-width:0}}.lessonrow>div:nth-child(2){{min-width:0}}.lessonrow h3{{font-size:15px;overflow-wrap:anywhere}}.search{{font-size:16px}}.form{{margin:35px auto 50px;padding:20px}}
}}
@media(max-width:480px){{
.area-panel{{top:63px;left:8px;right:8px;max-height:calc(100vh - 72px)}}.area-grid{{grid-template-columns:1fr}}.path{{grid-template-columns:1fr}}h1{{font-size:40px}}.hero{{padding-top:38px}}.actions{{width:100%}}.actions .btn{{width:100%}}.coursecard{{min-height:0}}.coursecard .btn{{width:100%}}.sectionhead{{align-items:flex-start;flex-direction:column}}.sectionhead>.btn{{width:100%}}.statgrid{{grid-template-columns:1fr}}
}}
@media(prefers-reduced-motion:reduce){{
*,*:before,*:after{{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}}.reveal{{opacity:1!important;transform:none!important}}
}}
</style></head><body><div class="motion-bg" aria-hidden="true"><div class="motion-orb one"></div><div class="motion-orb two"></div><div class="motion-code">010101  class Course:  build()  learn()  practice()
def practice(skill):  return progress(skill)
const learner = new Learner()
while learning:  learner.practice()</div></div><header class="top"><a class="logo" href="/">Ease<span>WithPy</span></a><nav class="nav"><div class="area-menu" id="areaMenu"><button class="area-trigger" id="areaTrigger" type="button" aria-expanded="false" aria-haspopup="true">Explore <span class="area-chevron">▼</span></button><div class="area-panel" id="areaPanel"><div class="area-label">Explore EaseWithPy</div><div class="area-grid"><a class="area-link" href="/courses"><b>Library</b><span>All courses & lessons</span></a><a class="area-link" href="/academy"><b>Academy</b><span>Practice, projects & references</span></a><a class="area-link" href="/tools"><b>Toolkit</b><span>Labs, playground & utilities</span></a><a class="area-link" href="/practice"><b>Practice</b><span>Hands-on coding practice</span></a><a class="area-link" href="/projects"><b>Projects</b><span>Build real things</span></a><a class="area-link" href="/challenges"><b>Challenges</b><span>Test your knowledge</span></a><a class="area-link" href="/cheatsheets"><b>Cheatsheets</b><span>Quick references</span></a><a class="area-link" href="/glossary"><b>Glossary</b><span>Developer terms</span></a></div><div class="area-divider"></div><div class="area-label">Site & legal</div><div class="area-grid"><a class="area-link" href="/about"><b>About</b><span>About EaseWithPy</span></a><a class="area-link" href="/contact"><b>Contact</b><span>Report a problem</span></a><a class="area-link" href="/terms"><b>Terms of Service</b><span>Rules for using the site</span></a><a class="area-link" href="/privacy"><b>Privacy</b><span>Data and privacy</span></a><a class="area-link" href="/disclaimer"><b>Disclaimer</b><span>Educational disclaimer</span></a></div><div class="area-divider"></div><div class="area-label">Your learning</div><div class="area-grid"><a class="area-link" href="/dashboard"><b>Dashboard</b><span>Progress & activity</span></a><a class="area-link" href="/skills"><b>Skills</b><span>Skill mastery</span></a><a class="area-link" href="/adaptive"><b>Adaptive</b><span>What to do next</span></a><a class="area-link" href="/continue"><b>Continue</b><span>Pick up where you left off</span></a><a class="area-link" href="/saved"><b>Saved</b><span>Saved lessons</span></a><a class="area-link" href="/notes"><b>Notes</b><span>Your learning notes</span></a><a class="area-link" href="/achievements"><b>Achievements</b><span>Badges & XP</span></a><a class="area-link" href="/leaderboard"><b>Leaderboard</b><span>Community XP</span></a></div></div></div><a href="/courses">Courses</a><a href="/academy">Academy</a><a href="/tools">Toolkit</a>{nav_auth()}</nav></header><main class="shell">{body}</main><footer>EaseWithPy · Learn / practice / build · Free to start · <a href="/about">About</a> · <a href="/terms">Terms</a> · <a href="/privacy">Privacy</a> · <a href="/disclaimer">Disclaimer</a></footer><script>
(function(){{
  const reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if(reduce)return;
  document.documentElement.classList.add("motion-ready");
  const items=document.querySelectorAll(".reveal,.stagger");
  items.forEach((el,i)=>el.style.setProperty("--delay",Math.min(i*70,420)+"ms"));
  if("IntersectionObserver" in window){{
    const io=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add("is-visible");io.unobserve(e.target)}}),{{threshold:.1,rootMargin:"0px 0px -50px"}});
    items.forEach(el=>io.observe(el));
  }}else items.forEach(el=>el.classList.add("is-visible"));
}})();
</script><script>
const areaMenu=document.getElementById("areaMenu"),areaTrigger=document.getElementById("areaTrigger");
if(areaMenu&&areaTrigger){{areaTrigger.onclick=e=>{{e.stopPropagation();const open=areaMenu.classList.toggle("open");areaTrigger.setAttribute("aria-expanded",open?"true":"false")}};document.addEventListener("click",e=>{{if(!areaMenu.contains(e.target)){{areaMenu.classList.remove("open");areaTrigger.setAttribute("aria-expanded","false")}}}});document.addEventListener("keydown",e=>{{if(e.key==="Escape"){{areaMenu.classList.remove("open");areaTrigger.setAttribute("aria-expanded","false")}}}})}}
</script><div id="cursorGlow" aria-hidden="true"></div><script>
(function(){{
const g=document.getElementById("cursorGlow");
if(g && window.matchMedia("(hover:hover)").matches){{
let x=-500,y=-500,tx=-500,ty=-500;
window.addEventListener("pointermove",function(e){{tx=e.clientX;ty=e.clientY}},{{passive:true}});
(function loop(){{x+=(tx-x)*.12;y+=(ty-y)*.12;g.style.left=x+"px";g.style.top=y+"px";requestAnimationFrame(loop)}})();
}}
}})();
</script></body></html>'''

            def home():
                u=mod.user()
                courses=all_courses()
                cards=''.join(f'<a class="coursecard" data-course="{html.escape((c["title"]+" "+c["tag"]+" "+c["description"]).lower())}" href="{c["href"]}"><span class="tag">{html.escape(c["tag"])}</span><span class="card-index" aria-hidden="true"></span><h3>{html.escape(c["title"])}</h3><p>{html.escape(c["description"])}</p><div class="meta"><span>{len(c["lessons"])} lessons</span><span>LESSON TRACK</span></div><span class="btn primary">{"Continue →" if u else "Start course →"}</span></a>' for c in courses)
                actions='<a class="btn primary" href="/dashboard">Continue learning</a><a class="btn" href="/courses">Browse all courses</a>' if u else '<a class="btn primary" href="/courses">Explore courses</a><a class="btn" href="/register">Create free account</a>'
                return layout(f'''<section class="hero"><div><div class="eyebrow">PRACTICAL PROGRAMMING LAB</div><h1>Write code.<br>Ship understanding.</h1><p>Structured lessons, working examples, deliberate practice, and projects. Learn the syntax, use the tool, then prove you can build with it.</p><div class="actions">{actions}</div></div><div class="terminal"><div class="termhead">~/learnpython · interactive</div><div class="code">{"# Welcome back, "+html.escape(str(u["name"])) if u else "# Start with a course"}\n\ncourse = choose(" + '"your path"' + ")\nlearn(course)\npractice(course)\nbuild(project)\n\n# no gatekeeping. just build.</div></div></section><section class="section reveal"><div class="sectionhead"><div><div class="eyebrow">COURSE LIBRARY</div><h2>Pick what you want to learn.</h2><p>Python, AI, Go, TypeScript, HTML, CSS, JavaScript, SQL and Git — with more tracks ready to add.</p></div><a class="btn" href="/courses">Open library →</a></div><input class="search" id="q" placeholder="⌕  Search Python, AI, web, Go…"><div id="grid" class="cgrid stagger reveal">{cards}</div></section><section class="section"><div class="eyebrow">THE LEARNING LOOP</div><h2>Less passive watching. More doing.</h2><div class="path stagger reveal"><div class="step"><span class="eyebrow">01</span><b>Learn</b><p>Learn the concept and the syntax.</p></div><div class="step"><span class="eyebrow">02</span><b>Practice</b><p>Use it immediately in a small exercise.</p></div><div class="step"><span class="eyebrow">03</span><b>Break it</b><p>Change the code and inspect what breaks.</p></div><div class="step"><span class="eyebrow">04</span><b>Build</b><p>Combine the pieces into something useful.</p></div></div></section><section class="section"><div class="banner"><div><div class="eyebrow">YOUR ACCOUNT</div><h2>Save your progress.</h2><p style="margin:0">Create a free account and your completed lessons follow you between sessions.</p></div><div class="actions" style="margin:0"><a class="btn primary" href="{"/dashboard" if u else "/register"}">{ "Open dashboard" if u else "Create account" }</a></div></div></section>
<script>
(function(){{
  const reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const items=[...document.querySelectorAll(".section,.coursecard,.step,.banner,.terminal")];
  items.forEach((el,i)=>{{el.classList.add("reveal");el.style.setProperty("--delay",Math.min(i*35,280)+"ms")}});
  if(!reduce && "IntersectionObserver" in window){{
    const io=new IntersectionObserver(entries=>entries.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add("visible");io.unobserve(e.target)}}}}),{{threshold:.08}});
    items.forEach(el=>io.observe(el));
  }}else items.forEach(el=>el.classList.add("visible"));

  const code=document.querySelector(".terminal .code");
  if(code && !reduce){{
    const full=code.textContent;
    code.textContent="";
    let i=0;
    const type=()=>{{ if(i<full.length){{code.textContent+=full[i++];setTimeout(type,12)}} }};
    setTimeout(type,420);
  }}
}})();
</script><script>const q=document.getElementById("q");q.addEventListener("input",()=>{{const x=q.value.toLowerCase().trim();document.querySelectorAll("[data-course]").forEach(c=>c.style.display=!x||c.dataset.course.includes(x)?"flex":"none")}})</script>''',"EaseWithPy — Interactive Code School")

            def courses_page():
                cs=all_courses()
                cards=''.join(f'<a class="coursecard" data-cat="{html.escape(c["tag"])}" data-course="{html.escape((c["title"]+" "+c["tag"]+" "+c["description"]).lower())}" href="{c["href"]}"><span class="tag">{html.escape(c["tag"])}</span><h3>{html.escape(c["title"])}</h3><p>{html.escape(c["description"])}</p><div class="meta"><span>{len(c["lessons"])} lessons</span><span>Beginner → Master</span></div><span class="btn primary">Open course →</span></a>' for c in cs)
                filters=''.join(f'<button class="filter" data-filter="{html.escape(t["tag"])}">{html.escape(t["title"])}</button>' for t in cs)
                return layout(f'''<section class="libraryhero"><div class="eyebrow">EASEWITHPY ACADEMY</div><h1>Choose your path.</h1><p>Start from zero, switch tracks whenever you want, and keep your progress in one account.</p><input id="search" class="search" placeholder="⌕  Search the library…"><div class="filters"><button class="filter active" data-filter="ALL">All</button>{filters}</div></section><section class="section" style="padding-top:10px"><div id="catalog" class="cgrid">{cards}</div></section><script>const s=document.getElementById("search"),fs=[...document.querySelectorAll(".filter")],cards=[...document.querySelectorAll("[data-cat]")];let f="ALL";function render(){{const q=s.value.toLowerCase().trim();cards.forEach(c=>c.style.display=(f==="ALL"||c.dataset.cat===f)&&(!q||c.dataset.course.includes(q))?"flex":"none")}}s.addEventListener("input",render);fs.forEach(b=>b.onclick=()=>{{fs.forEach(x=>x.classList.remove("active"));b.classList.add("active");f=b.dataset.filter;render()}})</script>''',"Course Library")

            def course_overview(slug):
                cs=all_courses(); c=next((x for x in cs if x["slug"]==slug),None)
                if not c: abort(404)
                rows=[]
                if slug=="python":
                    rows=''.join(f'<a class="lessonrow" href="/learn/{x["n"]}"><span class="num">{x["n"]}</span><span><b>{html.escape(x["title"])}</b><br><span class="hint">{html.escape(x.get("part",""))} · {html.escape(x.get("level","Master"))}</span></span><small>Lesson →</small></a>' for x in c["lessons"])
                else:
                    rows=''.join(f'<a class="lessonrow" href="/learn/{slug}/{i}"><span class="num">{i}</span><span><b>{html.escape(x["title"])}</b><br><span class="hint">{html.escape(x.get("part",""))} · {html.escape(x.get("level","Master"))}</span></span><small>Lesson →</small></a>' for i,x in enumerate(c["lessons"],1))
                return layout(f'''<section class="libraryhero"><a class="hint" href="/courses">← Course library</a><div class="coursehero"><div class="eyebrow">{html.escape(c["tag"])}</div><h1 style="font-size:clamp(42px,6vw,68px)">{html.escape(c["title"])}</h1><p>{html.escape(c["description"])}</p><div class="actions"><a class="btn primary" href="{"/learn/1" if slug=="python" else f"/learn/{slug}/1"}">Start from lesson 1 →</a><a class="btn" href="/dashboard">My progress</a></div></div></section><section class="section" style="padding-top:5px"><div class="sectionhead"><div><div class="eyebrow">CURRICULUM</div><h2>{len(c["lessons"])} lessons</h2></div></div>{rows}</section>''',f'{c["title"]} Course')

            if "favicon_page" not in app.view_functions:
                def favicon_page():
                    return Response('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#080808"/><path d="M18 16h28v8H26v8h17v8H26v8h20v8H18z" fill="#fff"/></svg>',mimetype="image/svg+xml")
                app.add_url_rule("/favicon.svg","favicon_page",favicon_page)

            if "og_page" not in app.view_functions:
                def og_page():
                    return Response('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630"><rect width="1200" height="630" fill="#070707"/><text x="80" y="240" fill="white" font-family="Arial" font-size="76" font-weight="800">EaseWithPy</text><text x="82" y="315" fill="#aaa" font-family="Arial" font-size="34">Learn code. Actually build.</text></svg>',mimetype="image/svg+xml")
                app.add_url_rule("/og.svg","og_page",og_page)
            def _legal(title, body):
                return L(f'<section class="section"><nav class="hint"><a href="/">Home</a> / {html.escape(title)}</nav><h1>{html.escape(title)}</h1><p style="max-width:850px;font-size:17px">{html.escape(body)}</p></section>',title)
            legal_pages = {
                "about_page": ("/about", "About EaseWithPy", "EaseWithPy is an independent educational coding project for programming lessons, practice and projects."),
                "terms_page": ("/terms", "Terms of Use", "Use EaseWithPy lawfully and responsibly. Do not abuse the service, attempt unauthorized access, upload malicious content, or violate another person's rights."),
                "privacy_page": ("/privacy", "Privacy Notice", "Account information and learning progress may be stored to operate the service. Do not submit sensitive information unless specifically required."),
                "disclaimer_page": ("/disclaimer", "Educational Disclaimer", "All content and code are provided for educational and informational purposes only. Verify important software, security, legal, financial, and operational decisions against current authoritative sources. Test code before production use.")
            }
            for endpoint, (path, title, body) in legal_pages.items():
                if endpoint not in app.view_functions:
                    app.add_url_rule(path, endpoint, lambda title=title, body=body: _legal(title, body))

            def custom_404(e):
                return L('<section class="section" style="text-align:center;padding:110px 0"><div class="eyebrow">404 · NOT FOUND</div><h1>That page vanished.</h1><p>The URL does not match a EaseWithPy page.</p><a class="btn primary" href="/">Go home</a></section>',"Page Not Found"),404
            if 404 not in app.error_handler_spec.get(None, {}):
                app.register_error_handler(404, custom_404)

            def dashboard():
                u=mod.user()
                if not u: return redirect("/login")
                con=mod.db()
                done=int(con.execute("SELECT COUNT(*) AS n FROM progress WHERE user_id=? AND completed=1",(u["id"],)).fetchone()["n"])
                recent=con.execute("SELECT lesson_id,updated_at FROM progress WHERE user_id=? AND completed=1 ORDER BY updated_at DESC LIMIT 10",(u["id"],)).fetchall()
                con.close()
                total=len(mod.COURSE)+sum(len(c["lessons"]) for c in EXTRA)
                pct=round(min(done/total*100,100)) if total else 0

                recent_items=[]
                for r in recent:
                    lid=int(r["lesson_id"])
                    if lid <= len(mod.COURSE):
                        target=f"/learn/{lid}"
                        label=f"Python · Lesson {lid}"
                    else:
                        code=lid-1000
                        course_index=(code-1)//100
                        lesson_no=(code-1)%100+1
                        if 0 <= course_index < len(EXTRA) and 1 <= lesson_no <= len(EXTRA[course_index]["lessons"]):
                            target=f"/learn/{EXTRA[course_index]['slug']}/{lesson_no}"
                            label=f"{EXTRA[course_index]['title']} · Lesson {lesson_no}"
                        else:
                            continue
                    recent_items.append(f'<a class="lessonrow" href="{target}"><span class="num">✓</span><span><b>{html.escape(label)}</b><br><span class="hint">Completed {html.escape(str(r["updated_at"]))}</span></span><small>→</small></a>')
                recent_html="".join(recent_items) or '<p class="hint">Nothing completed yet. Pick a course and start lesson 1.</p>'

                return layout(f'''<section class="dash"><div class="eyebrow">YOUR LEARNING SPACE</div><h1 style="font-size:clamp(42px,6vw,68px)">Welcome, {html.escape(str(u["name"]))}.</h1><div class="statgrid"><div class="stat"><strong>{done}</strong><span>lessons complete</span></div><div class="stat"><strong>{pct}%</strong><span>overall progress</span></div><div class="stat"><strong>{len(EXTRA)+1}</strong><span>learning paths</span></div></div><div class="dashgrid"><div><div class="progress"><div style="display:flex;justify-content:space-between"><b>Keep your streak alive</b><span>{pct}%</span></div><div class="bar" style="margin-top:12px"><i style="width:{pct}%"></i></div><p>Every completed lesson is one more thing you can actually build with.</p><div class="actions"><a class="btn primary" href="/courses">Choose a course →</a></div></div><section class="section"><div class="eyebrow">RECENT</div><h2>Your progress</h2>{recent_html}</section></div><aside class="card"><div class="eyebrow">ALL PATHS</div><h3>Keep exploring</h3><p>Switch between Python, AI, Go, TypeScript, HTML, CSS, JavaScript, SQL, and Git whenever you want.</p><a class="btn primary" href="/courses">Browse courses</a></aside></div></section>''',"Dashboard")
            def login():
                if mod.user(): return redirect("/dashboard")
                if request.method=="POST":
                    mod.require_csrf()
                    email=request.form.get("email","").strip().lower(); pw=request.form.get("password","")
                    if not mod.valid_email(email) or not mod.valid_password(pw): return L('<div class="form"><div class="eyebrow">LOGIN</div><h1>That did not work.</h1><p>Check your email and password and try again.</p><a class="btn primary" href="/login">Try again</a></div>',"Log in")
                    if not mod.rate_limit("login:"+request.remote_addr+":"+email,8,600): return L('<div class="form"><div class="eyebrow">SLOW DOWN</div><h1>Too many tries.</h1><p>Wait a few minutes and try again.</p></div>',"Log in")
                    con=mod.db(); u=con.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone(); con.close()
                    if not u or not mod.verify_password(u["password"],pw): return L('<div class="form"><div class="eyebrow">LOGIN</div><h1>That did not work.</h1><p>We could not sign you in. Check your details and try again.</p><a class="btn primary" href="/login">Try again</a></div>',"Log in")
                    mod.session.clear(); mod.session["uid"]=u["id"]; mod.session["csrf"]=mod.secrets.token_urlsafe(24)
                    return redirect("/dashboard")
                return L(f'<form class="form" method="post" autocomplete="on"><div class="eyebrow">WELCOME BACK</div><h1>Log in.</h1><p>Pick up exactly where you left off.</p><input type="hidden" name="csrf" value="{html.escape(str(mod.csrf()))}"><label>Email</label><input type="email" name="email" autocomplete="email" required><label>Password</label><input type="password" name="password" autocomplete="current-password" required><button>Log in →</button><p class="hint">No account? <a href="/register" style="color:#fff">Create one free.</a></p></form>',"Log in")

            def register():
                if mod.user(): return redirect("/dashboard")
                if request.method=="POST":
                    mod.require_csrf()
                    email=request.form.get("email","").strip().lower(); name=request.form.get("name","").strip(); pw=request.form.get("password",""); confirm=request.form.get("confirm_password","")
                    if not mod.rate_limit("register:"+request.remote_addr+":"+email,5,600): return L('<div class="form"><div class="eyebrow">SLOW DOWN</div><h1>Too many tries.</h1><p>Wait a few minutes and try again.</p></div>',"Create account")
                    if not mod.valid_name(name) or not mod.valid_email(email) or not mod.valid_password(pw) or pw!=confirm or request.form.get("age_confirm") != "1":
                        return L('<div class="form"><div class="eyebrow">CREATE ACCOUNT</div><h1>Check your details.</h1><p>Use a valid email, a 12–128 character password, and matching confirmation.</p><a class="btn primary" href="/register">Try again</a></div>',"Create account")
                    try:
                        con=mod.db(); cur=con.execute("INSERT INTO users(email,name,password) VALUES(?,?,?)",(email,name,mod.hash_password(pw))); con.commit(); uid=cur.lastrowid; con.close()
                        mod.session.clear(); mod.session["uid"]=uid; mod.session["csrf"]=mod.secrets.token_urlsafe(24)
                        return redirect("/dashboard")
                    except Exception:
                        return L('<div class="form"><div class="eyebrow">ACCOUNT</div><h1>We could not create the account.</h1><p>Check the information and try again.</p><a class="btn primary" href="/register">Try again</a></div>',"Create account")
                return L(f'<form class="form" method="post" autocomplete="on"><div class="eyebrow">START FREE</div><h1>Create your account.</h1><p>Save lessons, track progress, and keep every course in one place.</p><input type="hidden" name="csrf" value="{html.escape(str(mod.csrf()))}"><label>Name</label><input type="text" name="name" autocomplete="name" maxlength="80" required><label>Email</label><input type="email" name="email" autocomplete="email" maxlength="254" required><label>Password</label><input type="password" name="password" autocomplete="new-password" minlength="12" maxlength="128" required><label>Confirm password</label><input type="password" name="confirm_password" autocomplete="new-password" minlength="12" maxlength="128" required><label style="display:flex;gap:8px;align-items:flex-start;font-size:13px;color:#aaa"><input type="checkbox" name="age_confirm" value="1" required style="width:auto;margin-top:3px"> I confirm that I am 13 or older.</label><button>Create account →</button><p class="hint">Already registered? <a href="/login" style="color:#fff">Log in.</a></p></form>',"Create account")

            def extra_lesson(slug,n):
                c=next((x for x in EXTRA if x["slug"]==slug),None)
                if not c or n<1 or n>len(c["lessons"]): abort(404)
                item=c["lessons"][n-1]; u=mod.user(); pid=1000+(EXTRA.index(c)*100)+n; done=False
                if u:
                    con=mod.db(); row=con.execute("SELECT completed FROM progress WHERE user_id=? AND lesson_id=?",(u["id"],pid)).fetchone(); con.close(); done=bool(row)
                safe=mod.render_lesson_body(item["title"]+"\n"+item["body"])
                complete=(f'<button id="done" class="btn primary" onclick="doneLesson()">{"✓ Completed" if done else "✓ Complete lesson"}</button>' if u else '<a class="btn" href="/login">Log in to save progress</a>')
                nxt=f'<a class="btn primary" href="/learn/{slug}/{n+1}">Next lesson →</a>' if n<len(c["lessons"]) else '<a class="btn primary" href="/courses/'+slug+'">Course complete →</a>'
                js=f'''<script>async function doneLesson(){{const r=await fetch("/api/course-progress/{slug}/{n}",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{csrf:"{html.escape(str(mod.csrf()))}"}})}});if(r.ok){{document.getElementById("done").textContent="✓ Completed";document.getElementById("done").disabled=true}}}}</script>'''
                return L(f'<section class="section"><a class="hint" href="/course/{slug}">← {html.escape(c["title"])}</a><div style="margin-top:30px" class="eyebrow">{html.escape(c["tag"])} · LESSON {n}/{len(c["lessons"])}</div><h1 style="font-size:clamp(42px,6vw,68px)"> {html.escape(item["title"])}</h1><div class="card" style="margin-bottom:16px">{safe}</div><div class="actions"><a class="btn" href="/course/{slug}">Course index</a>{complete}{nxt}</div></section>{js}',f'{item["title"]} · {c["title"]}')

            def save_progress(slug,n):
                u=mod.user(); c=next((x for x in EXTRA if x["slug"]==slug),None)
                if not u or not c or n<1 or n>len(c["lessons"]): return jsonify(error="unauthorized"),401
                data=request.get_json(silent=True) or {}
                if not mod.secrets.compare_digest(str(data.get("csrf","")),str(mod.session.get("csrf",""))): return jsonify(error="csrf"),400
                pid=1000+(EXTRA.index(c)*100)+n
                con=mod.db(); con.execute("INSERT INTO progress(user_id,lesson_id,completed) VALUES(?,?,1) ON CONFLICT(user_id,lesson_id) DO UPDATE SET completed=1,updated_at=CURRENT_TIMESTAMP",(u["id"],pid)); con.commit(); con.close()
                return jsonify(ok=True)

            app.view_functions["home"]=home
            app.view_functions["courses"]=courses_page
            app.view_functions["dashboard"]=dashboard
            app.view_functions["login"]=login
            app.view_functions["register"]=register
            if "course_overview_v2" not in app.view_functions:
                app.add_url_rule("/course/<slug>",endpoint="course_overview_v2",view_func=course_overview,methods=["GET"])
                if "course_overview_legacy" not in app.view_functions:
                    app.add_url_rule("/courses/<slug>",endpoint="course_overview_legacy",view_func=course_overview,methods=["GET"])
            if "extra_course_lesson" in app.view_functions:
                app.view_functions["extra_course_lesson"]=extra_lesson
            else:
                app.add_url_rule("/learn/<slug>/<int:n>",endpoint="extra_course_lesson",view_func=extra_lesson,methods=["GET"])
            if "extra_course_progress" in app.view_functions:
                app.view_functions["extra_course_progress"]=save_progress
            else:
                app.add_url_rule("/api/course-progress/<slug>/<int:n>",endpoint="extra_course_progress",view_func=save_progress,methods=["POST"])
            mod.layout=layout
            app.layout=layout
            print("[EaseWithPy] platform UI installed: modular course library + auth + dashboard")
            return
        except Exception as e:
            print("[EaseWithPy] platform install retry:",repr(e)); traceback.print_exc()
            time.sleep(1)

install()
