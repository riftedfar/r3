"""LearnPython platform UI: course library, auth, dashboard, and extra-course routing."""
import sys, threading, time, html

def install():
    for _ in range(120):
        mod = sys.modules.get("app") or sys.modules.get("__main__")
        app = getattr(mod, "APP", None) if mod else None
        if app is None or not hasattr(mod, "COURSE") or not hasattr(mod, "layout"):
            time.sleep(0.25)
            continue
        try:
            from additional_courses import COURSES as EXTRA
            from flask import abort, redirect, request, jsonify

            def L(body, title="LearnPython"):
                return mod.layout(body, title)

            def all_courses():
                py={"slug":"python","title":"Python","tag":"PYTHON","description":"The complete beginner-to-builder Python path: syntax, data, functions, files, errors, OOP, modules, projects and more.","lessons":mod.COURSE,"href":"/courses/python"}
                return [py]+[{"slug":c["slug"],"title":c["title"],"tag":c["tag"],"description":c["description"],"lessons":c["lessons"],"href":f"/courses/{c['slug']}"} for c in EXTRA]

            def nav_auth():
                u=mod.user()
                if u:
                    return '<a class="navbtn" href="/dashboard">Dashboard</a><span class="userchip">Hi, '+html.escape(str(u["name"]))+'</span><form method="post" action="/logout" class="inline"><input type="hidden" name="csrf" value="'+html.escape(str(mod.csrf()))+'"><button class="ghost">Log out</button></form>'
                return '<a class="navbtn" href="/login">Log in</a><a class="navbtn primary" href="/register">Create account</a>'

            def layout(body,title="LearnPython"):
                return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} · LearnPython</title>
<meta name="description" content="Interactive coding courses with lessons, labs, projects and progress tracking.">
<style>
:root{{--bg:#060606;--panel:#0d0d0d;--panel2:#141414;--line:#292929;--text:#f5f5f5;--muted:#9a9a9a;--soft:#cfcfcf}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif}}a{{color:inherit;text-decoration:none}}button,input{{font:inherit}}button{{cursor:pointer}}
.top{{height:68px;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50;background:#060606eF;backdrop-filter:blur(16px);display:flex;align-items:center;padding:0 4vw;gap:25px}}.logo{{font-weight:950;font-size:22px;letter-spacing:-.06em;white-space:nowrap}}.logo span{{color:#aaa}}.nav{{display:flex;align-items:center;gap:7px;margin-left:auto}}.nav a,.navbtn,.ghost{{padding:9px 12px;border:1px solid transparent;border-radius:10px;color:#aaa;background:transparent}}.nav a:hover,.ghost:hover{{color:#fff;background:#101010;border-color:#222}}.primary{{background:#fff!important;color:#000!important;border-color:#fff!important;font-weight:850}}.userchip{{color:#ddd;font-size:13px;padding:8px 5px}}.inline{{display:inline}}
.shell{{width:min(1200px,92vw);margin:auto}}.hero{{padding:80px 0 55px;display:grid;grid-template-columns:1.15fr .85fr;gap:45px;align-items:center}}.eyebrow{{font-size:11px;font-weight:900;letter-spacing:.16em;color:#fff;text-transform:uppercase}}h1{{font-size:clamp(46px,7vw,86px);line-height:.92;letter-spacing:-.075em;margin:12px 0 22px}}h2{{letter-spacing:-.045em}}h3{{letter-spacing:-.03em}}p{{color:var(--muted);line-height:1.7}}.hero p{{font-size:18px;max-width:690px}}.actions{{display:flex;gap:10px;flex-wrap:wrap;margin-top:25px}}.btn{{display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--line);background:var(--panel2);padding:11px 15px;border-radius:11px;font-weight:750}}.btn:hover{{border-color:#555}}.btn.primary{{background:#fff;color:#000;border-color:#fff}}.terminal{{border:1px solid var(--line);background:linear-gradient(145deg,#151515,#090909);border-radius:24px;padding:24px;box-shadow:0 30px 100px #000}}.termhead{{color:#666;font-size:12px;margin-bottom:18px}}.code{{font-family:ui-monospace,monospace;white-space:pre-wrap;line-height:1.65;color:#eee}}
.section{{padding:50px 0}}.sectionhead{{display:flex;justify-content:space-between;gap:20px;align-items:end;margin-bottom:20px}}.sectionhead p{{margin:5px 0}}.search{{width:100%;padding:15px 17px;border:1px solid var(--line);border-radius:13px;background:#090909;color:#fff;outline:none;margin:8px 0 18px}}.search:focus{{border-color:#666}}
.filters{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}}.filter{{border:1px solid var(--line);background:#0c0c0c;color:#aaa;padding:8px 11px;border-radius:999px;cursor:pointer}}.filter.active{{background:#fff;color:#000;border-color:#fff}}
.cgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.coursecard{{min-height:270px;padding:22px;border:1px solid var(--line);border-radius:19px;background:linear-gradient(155deg,#151515,#0a0a0a);display:flex;flex-direction:column;transition:.16s}}.coursecard:hover{{transform:translateY(-4px);border-color:#555}}.tag{{font-size:10px;font-weight:900;letter-spacing:.12em;color:#aaa;border:1px solid #333;border-radius:999px;padding:5px 8px;width:max-content}}.coursecard h3{{font-size:26px;margin:12px 0 7px}}.coursecard p{{font-size:14px;margin:0 0 15px}}.meta{{display:flex;justify-content:space-between;color:#777;font-size:12px;margin-top:auto;margin-bottom:13px}}
.path{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}.step,.card{{border:1px solid var(--line);background:#0d0d0d;border-radius:16px;padding:18px}}.step b{{display:block;margin-top:7px}}.step p{{font-size:13px;margin-bottom:0}}
.banner{{border:1px solid #3a3a3a;background:linear-gradient(110deg,#161616,#0a0a0a);border-radius:20px;padding:25px;display:flex;justify-content:space-between;align-items:center;gap:20px}}footer{{border-top:1px solid var(--line);padding:35px 4vw;color:#666;margin-top:45px}}
.libraryhero{{padding:55px 0 20px}}.libraryhero h1{{font-size:clamp(42px,6vw,70px)}}.catalog{{display:grid;grid-template-columns:240px 1fr;gap:20px}}.side{{position:sticky;top:88px;height:max-content;border:1px solid var(--line);background:#0b0b0b;border-radius:16px;padding:16px}}.side a{{display:block;padding:10px;border-radius:9px;color:#aaa}}.side a:hover{{background:#171717;color:#fff}}.coursehero{{border:1px solid var(--line);border-radius:20px;background:linear-gradient(145deg,#151515,#090909);padding:27px;margin-bottom:16px}}.lessonrow{{display:flex;align-items:center;gap:14px;padding:15px;border:1px solid var(--line);border-radius:12px;background:#0c0c0c;margin:8px 0}}.lessonrow:hover{{background:#141414;border-color:#444}}.num{{width:34px;height:34px;border-radius:10px;background:#1b1b1b;display:flex;align-items:center;justify-content:center;font-weight:900;flex:none}}.lessonrow small{{margin-left:auto;color:#666}}
.form{{max-width:500px;margin:70px auto 90px;border:1px solid var(--line);background:#0d0d0d;border-radius:20px;padding:27px}}.form h1{{font-size:43px;margin-bottom:10px}}label{{display:block;margin:16px 0 7px;font-size:13px;color:#ddd}}input[type=text],input[type=email],input[type=password]{{width:100%;padding:14px;border:1px solid var(--line);border-radius:10px;background:#080808;color:#fff;outline:none}}input:focus{{border-color:#666}}.form button{{width:100%;margin-top:18px;padding:13px;border:1px solid #fff;background:#fff;color:#000;border-radius:10px;font-weight:900}}.hint{{font-size:13px;color:#777}}
.dash{{padding:50px 0}}.dashgrid{{display:grid;grid-template-columns:1fr 320px;gap:16px}}.progress{{border:1px solid var(--line);border-radius:16px;background:#0d0d0d;padding:20px}}.bar{{height:8px;background:#222;border-radius:99px;overflow:hidden}}.bar i{{display:block;height:100%;background:#fff}}.statgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:15px 0}}.stat{{border:1px solid var(--line);border-radius:13px;padding:15px;background:#0c0c0c}}.stat strong{{font-size:24px;display:block}}.stat span{{color:#777;font-size:12px}}
@media(max-width:850px){{.top{{padding:0 3vw;gap:10px}}.nav a:not(.primary):not(.navbtn){{display:none}}.userchip{{display:none}}.hero{{grid-template-columns:1fr;padding:55px 0 35px}}.cgrid{{grid-template-columns:1fr}}.path{{grid-template-columns:1fr 1fr}}.catalog,.dashgrid{{grid-template-columns:1fr}}.side{{position:static}}.banner{{align-items:flex-start;flex-direction:column}}.section{{padding:35px 0}}.shell{{width:92vw}}}}
@media(max-width:480px){{.logo{{font-size:19px}}.top{{height:62px}}.navbtn,.nav a{{padding:8px 9px;font-size:12px}}.path{{grid-template-columns:1fr}}h1{{font-size:42px}}.hero p{{font-size:16px}}}}
</style></head><body><header class="top"><a class="logo" href="/">Learn<span>Python</span></a><nav class="nav"><a href="/courses">Courses</a><a href="/tools">Toolkit</a>{nav_auth()}</nav></header><main class="shell">{body}</main><footer>LearnPython · Learn → practice → build · Free to start</footer></body></html>'''

            def home():
                u=mod.user()
                courses=all_courses()
                cards=''.join(f'<a class="coursecard" data-course="{html.escape((c["title"]+" "+c["tag"]+" "+c["description"]).lower())}" href="{c["href"]}"><span class="tag">{html.escape(c["tag"])}</span><h3>{html.escape(c["title"])}</h3><p>{html.escape(c["description"])}</p><div class="meta"><span>{len(c["lessons"])} lessons</span><span>Beginner → builder</span></div><span class="btn primary">{"Continue →" if u else "Start course →"}</span></a>' for c in courses)
                actions='<a class="btn primary" href="/dashboard">Continue learning</a><a class="btn" href="/courses">Browse all courses</a>' if u else '<a class="btn primary" href="/courses">Explore courses</a><a class="btn" href="/register">Create free account</a>'
                return layout(f'''<section class="hero"><div><div class="eyebrow">THE INTERACTIVE CODE SCHOOL</div><h1>Learn code.<br>Actually build.</h1><p>Choose a path, learn one idea at a time, practice it in a lab, break it, fix it, and finish with projects. Built to feel more like a coding platform than a pile of tutorial pages.</p><div class="actions">{actions}</div></div><div class="terminal"><div class="termhead">~/learnpython · interactive</div><div class="code">{"# Welcome back, "+html.escape(str(u["name"])) if u else "# Start with a course"}\n\ncourse = choose(" + '"your path"' + ")\nlearn(course)\npractice(course)\nbuild(project)\n\n# no gatekeeping. just build.</div></div></section><section class="section"><div class="sectionhead"><div><div class="eyebrow">COURSE LIBRARY</div><h2>Pick what you want to learn.</h2><p>Python, AI, Go, TypeScript, HTML and CSS — with room to add more later.</p></div><a class="btn" href="/courses">Open library →</a></div><input class="search" id="q" placeholder="⌕  Search Python, AI, web, Go…"><div id="grid" class="cgrid">{cards}</div></section><section class="section"><div class="eyebrow">THE LEARNING LOOP</div><h2>Less passive watching. More doing.</h2><div class="path"><div class="step"><span class="eyebrow">01</span><b>Learn</b><p>Short explanations without the textbook fog.</p></div><div class="step"><span class="eyebrow">02</span><b>Practice</b><p>Labs, questions and experiments while the idea is fresh.</p></div><div class="step"><span class="eyebrow">03</span><b>Break it</b><p>Make mistakes on purpose and learn from the error.</p></div><div class="step"><span class="eyebrow">04</span><b>Build</b><p>Projects that prove you can use the skill.</p></div></div></section><section class="section"><div class="banner"><div><div class="eyebrow">YOUR ACCOUNT</div><h2>Save your progress.</h2><p style="margin:0">Create a free account and your completed lessons follow you between sessions.</p></div><div class="actions" style="margin:0"><a class="btn primary" href="{"/dashboard" if u else "/register"}">{ "Open dashboard" if u else "Create account" }</a></div></div></section><script>const q=document.getElementById("q");q.addEventListener("input",()=>{{const x=q.value.toLowerCase().trim();document.querySelectorAll("[data-course]").forEach(c=>c.style.display=!x||c.dataset.course.includes(x)?"flex":"none")}})</script>''',"LearnPython — Interactive Code School")

            def courses_page():
                cs=all_courses()
                cards=''.join(f'<a class="coursecard" data-cat="{html.escape(c["tag"])}" data-course="{html.escape((c["title"]+" "+c["tag"]+" "+c["description"]).lower())}" href="{c["href"]}"><span class="tag">{html.escape(c["tag"])}</span><h3>{html.escape(c["title"])}</h3><p>{html.escape(c["description"])}</p><div class="meta"><span>{len(c["lessons"])} lessons</span><span>Free</span></div><span class="btn primary">Open course →</span></a>' for c in cs)
                return layout(f'''<section class="libraryhero"><div class="eyebrow">LEARNPYTHON ACADEMY</div><h1>Choose your path.</h1><p>Start from zero, switch tracks whenever you want, and keep your progress in one account.</p><input id="search" class="search" placeholder="⌕  Search the library…"><div class="filters"><button class="filter active" data-filter="ALL">All</button><button class="filter" data-filter="PYTHON">Python</button><button class="filter" data-filter="AI">AI</button><button class="filter" data-filter="GO">Go</button><button class="filter" data-filter="TS">TypeScript</button><button class="filter" data-filter="HTML">HTML</button><button class="filter" data-filter="CSS">CSS</button></div></section><section class="section" style="padding-top:10px"><div id="catalog" class="cgrid">{cards}</div></section><script>const s=document.getElementById("search"),fs=[...document.querySelectorAll(".filter")],cards=[...document.querySelectorAll("[data-cat]")];let f="ALL";function render(){{const q=s.value.toLowerCase().trim();cards.forEach(c=>c.style.display=(f==="ALL"||c.dataset.cat===f)&&(!q||c.dataset.course.includes(q))?"flex":"none")}}s.addEventListener("input",render);fs.forEach(b=>b.onclick=()=>{{fs.forEach(x=>x.classList.remove("active"));b.classList.add("active");f=b.dataset.filter;render()}})</script>''',"Course Library")

            def course_overview(slug):
                cs=all_courses(); c=next((x for x in cs if x["slug"]==slug),None)
                if not c: abort(404)
                rows=[]
                if slug=="python":
                    rows=''.join(f'<a class="lessonrow" href="/learn/{x["n"]}"><span class="num">{x["n"]}</span><span><b>{html.escape(x["title"])}</b><br><span class="hint">{html.escape(x["part"])}</span></span><small>Lesson →</small></a>' for x in c["lessons"])
                else:
                    rows=''.join(f'<a class="lessonrow" href="/learn/{slug}/{i}"><span class="num">{i}</span><span><b>{html.escape(x["title"])}</b><br><span class="hint">Learn · practice · build</span></span><small>Lesson →</small></a>' for i,x in enumerate(c["lessons"],1))
                return layout(f'''<section class="libraryhero"><a class="hint" href="/courses">← Course library</a><div class="coursehero"><div class="eyebrow">{html.escape(c["tag"])}</div><h1 style="font-size:clamp(42px,6vw,68px)">{html.escape(c["title"])}</h1><p>{html.escape(c["description"])}</p><div class="actions"><a class="btn primary" href="{"/learn/1" if slug=="python" else f"/learn/{slug}/1"}">Start from lesson 1 →</a><a class="btn" href="/dashboard">My progress</a></div></div></section><section class="section" style="padding-top:5px"><div class="sectionhead"><div><div class="eyebrow">CURRICULUM</div><h2>{len(c["lessons"])} lessons</h2></div></div>{rows}</section>''',f'{c["title"]} Course')

            def dashboard():
                u=mod.user()
                if not u: return redirect("/login")
                con=mod.db()
                done=int(con.execute("SELECT COUNT(*) AS n FROM progress WHERE user_id=? AND completed=1",(u["id"],)).fetchone()["n"])
                recent=con.execute("SELECT lesson_id,updated_at FROM progress WHERE user_id=? AND completed=1 ORDER BY updated_at DESC LIMIT 8",(u["id"],)).fetchall()
                con.close()
                total=len(mod.COURSE)+sum(len(c["lessons"]) for c in EXTRA)
                pct=round(min(done/total*100,100)) if total else 0
                recent_html=''.join(f'<a class="lessonrow" href="/learn/{r["lesson_id"]}"><span class="num">✓</span><span><b>Python lesson {r["lesson_id"]}</b><br><span class="hint">Completed {html.escape(str(r["updated_at"]))}</span></span><small>→</small></a>' for r in recent) or '<p class="hint">Nothing completed yet. Pick a course and start lesson 1.</p>'
                return layout(f'''<section class="dash"><div class="eyebrow">YOUR LEARNING SPACE</div><h1 style="font-size:clamp(42px,6vw,68px)">Welcome, {html.escape(str(u["name"]))}.</h1><div class="statgrid"><div class="stat"><strong>{done}</strong><span>lessons complete</span></div><div class="stat"><strong>{pct}%</strong><span>overall progress</span></div><div class="stat"><strong>{len(EXTRA)+1}</strong><span>learning paths</span></div></div><div class="dashgrid"><div><div class="progress"><div style="display:flex;justify-content:space-between"><b>Keep your streak alive</b><span>{pct}%</span></div><div class="bar" style="margin-top:12px"><i style="width:{pct}%"></i></div><p>Every completed lesson is one more thing you can actually build with.</p><div class="actions"><a class="btn primary" href="/courses">Choose a course →</a></div></div><section class="section"><div class="eyebrow">RECENT</div><h2>Your progress</h2>{recent_html}</section></div><aside class="card"><div class="eyebrow">ALL PATHS</div><h3>Keep exploring</h3><p>Switch between Python, AI, Go, TypeScript, HTML and CSS whenever you want.</p><a class="btn primary" href="/courses">Browse courses</a></aside></div></section>''',"Dashboard")

            def login():
                if mod.user(): return redirect("/dashboard")
                if request.method=="POST":
                    mod.require_csrf()
                    email=request.form.get("email","").strip().lower(); pw=request.form.get("password","")
                    if not mod.valid_email(email) or len(pw)>128: return L('<div class="form"><div class="eyebrow">LOGIN</div><h1>That did not work.</h1><p>Check your email and password and try again.</p><a class="btn primary" href="/login">Try again</a></div>',"Log in")
                    if not mod.rate_limit("login:"+request.remote_addr+":"+email,8,600): return L('<div class="form"><div class="eyebrow">SLOW DOWN</div><h1>Too many tries.</h1><p>Wait a few minutes and try again.</p></div>',"Log in")
                    con=mod.db(); u=con.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone(); con.close()
                    if not u or not mod.check_password_hash(u["password"],pw): return L('<div class="form"><div class="eyebrow">LOGIN</div><h1>Wrong details.</h1><p>The email or password was not accepted.</p><a class="btn primary" href="/login">Try again</a></div>',"Log in")
                    mod.session.clear(); mod.session["uid"]=u["id"]; mod.session["csrf"]=mod.secrets.token_urlsafe(24)
                    return redirect("/dashboard")
                return L(f'<form class="form" method="post" autocomplete="on"><div class="eyebrow">WELCOME BACK</div><h1>Log in.</h1><p>Pick up exactly where you left off.</p><input type="hidden" name="csrf" value="{html.escape(str(mod.csrf()))}"><label>Email</label><input type="email" name="email" autocomplete="email" required><label>Password</label><input type="password" name="password" autocomplete="current-password" required><button>Log in →</button><p class="hint">No account? <a href="/register" style="color:#fff">Create one free.</a></p></form>',"Log in")

            def register():
                if mod.user(): return redirect("/dashboard")
                if request.method=="POST":
                    mod.require_csrf()
                    email=request.form.get("email","").strip().lower(); name=request.form.get("name","").strip(); pw=request.form.get("password",""); confirm=request.form.get("confirm_password","")
                    if not mod.rate_limit("register:"+request.remote_addr+":"+email,5,600): return L('<div class="form"><div class="eyebrow">SLOW DOWN</div><h1>Too many tries.</h1><p>Wait a few minutes and try again.</p></div>',"Create account")
                    if len(name)<2 or len(name)>80 or not mod.valid_email(email) or len(pw)<12 or len(pw)>128 or pw!=confirm:
                        return L('<div class="form"><div class="eyebrow">CREATE ACCOUNT</div><h1>Check your details.</h1><p>Use a valid email, a 12–128 character password, and matching confirmation.</p><a class="btn primary" href="/register">Try again</a></div>',"Create account")
                    try:
                        con=mod.db(); cur=con.execute("INSERT INTO users(email,name,password) VALUES(?,?,?)",(email,name,mod.generate_password_hash(pw))); con.commit(); uid=cur.lastrowid; con.close()
                        mod.session.clear(); mod.session["uid"]=uid; mod.session["csrf"]=mod.secrets.token_urlsafe(24)
                        return redirect("/dashboard")
                    except Exception:
                        return L('<div class="form"><div class="eyebrow">ACCOUNT</div><h1>That email may already be registered.</h1><p>Try logging in instead.</p><a class="btn primary" href="/login">Log in</a></div>',"Create account")
                return L(f'<form class="form" method="post" autocomplete="on"><div class="eyebrow">START FREE</div><h1>Create your account.</h1><p>Save lessons, track progress, and keep every course in one place.</p><input type="hidden" name="csrf" value="{html.escape(str(mod.csrf()))}"><label>Name</label><input type="text" name="name" autocomplete="name" maxlength="80" required><label>Email</label><input type="email" name="email" autocomplete="email" maxlength="254" required><label>Password</label><input type="password" name="password" autocomplete="new-password" minlength="12" maxlength="128" required><label>Confirm password</label><input type="password" name="confirm_password" autocomplete="new-password" minlength="12" maxlength="128" required><button>Create account →</button><p class="hint">Already registered? <a href="/login" style="color:#fff">Log in.</a></p></form>',"Create account")

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
                return L(f'<section class="section"><a class="hint" href="/courses/{slug}">← {html.escape(c["title"])}</a><div style="margin-top:30px" class="eyebrow">{html.escape(c["tag"])} · LESSON {n}/{len(c["lessons"])}</div><h1 style="font-size:clamp(42px,6vw,68px)"> {html.escape(item["title"])}</h1><div class="card" style="margin-bottom:16px">{safe}</div><div class="actions"><a class="btn" href="/courses/{slug}">Course index</a>{complete}{nxt}</div></section>{js}',f'{item["title"]} · {c["title"]}')

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
            app.add_url_rule("/courses/<slug>",endpoint="course_overview",view_func=course_overview,methods=["GET"])
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
            print("[LearnPython] platform UI installed: course library + auth + dashboard")
            return
        except Exception as e:
            print("[LearnPython] platform install retry:",repr(e))
            time.sleep(1)

threading.Thread(target=install,daemon=True).start()
