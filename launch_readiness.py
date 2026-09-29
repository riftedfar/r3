"""EaseWithPy launch-readiness layer.

Adds production-focused exercises, autosave, feedback, SEO metadata,
security headers, polished error pages, and launch diagnostics.
"""
import html
import json
import time
import threading
import traceback

def install():
    def boot():
        for _ in range(120):
            try:
                mod = __import__("app")
                app = getattr(mod, "APP", None)
                layout = getattr(mod, "layout", None)
                if app is None or layout is None:
                    time.sleep(.25)
                    continue
                from flask import request, jsonify, Response, redirect

                con = mod.db()
                con.executescript("""
                CREATE TABLE IF NOT EXISTS learner_code(
                    user_id INTEGER NOT NULL,
                    item_key VARCHAR(255) NOT NULL,
                    code TEXT NOT NULL,
                    language VARCHAR(40) NOT NULL DEFAULT 'text',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY(user_id,item_key)
                );
                CREATE TABLE IF NOT EXISTS lesson_feedback(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    item_key VARCHAR(255) NOT NULL,
                    rating VARCHAR(20) NOT NULL,
                    reason VARCHAR(80),
                    message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS exercise_attempts(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    exercise_key VARCHAR(255) NOT NULL,
                    passed INTEGER NOT NULL DEFAULT 0,
                    answer TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS bug_reports(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    page_url VARCHAR(1000) NOT NULL,
                    category VARCHAR(80) NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)
                con.commit()
                con.close()

                def user():
                    return mod.user()

                def csrf_ok(data):
                    token = str((data or {}).get("csrf",""))
                    expected = str(mod.session.get("csrf",""))
                    return bool(expected) and mod.secrets.compare_digest(token, expected)

                def xp(amount):
                    u=user()
                    if not u:
                        return
                    con=mod.db()
                    row=con.execute("SELECT xp FROM learner_meta WHERE user_id=?",(u["id"],)).fetchone()
                    if row:
                        con.execute("UPDATE learner_meta SET xp=xp+?,last_active=CURRENT_TIMESTAMP WHERE user_id=?",(amount,u["id"]))
                    else:
                        con.execute("INSERT INTO learner_meta(user_id,xp,streak,last_active) VALUES(?,?,1,CURRENT_TIMESTAMP)",(u["id"],amount))
                    con.commit()
                    con.close()

                exercises = {
                    "python-variables": {
                        "title":"Variables",
                        "prompt":"Create a variable named score with the integer value 100, then print score.",
                        "starter":"# Write your solution here\n",
                        "hint":"Use assignment with =, then print the variable.",
                        "tests":["score = 100","print(score)"],
                        "solution":"score = 100\nprint(score)"
                    },
                    "python-conditionals": {
                        "title":"Conditionals",
                        "prompt":"Create age = 18 and print 'adult' when age is at least 18, otherwise print 'minor'.",
                        "starter":"age = 18\n# Write your if/else here\n",
                        "hint":"Compare age with 18 using >=.",
                        "tests":["age = 18","if age >= 18","print('adult')","else:","print('minor')"],
                        "solution":"age = 18\nif age >= 18:\n    print('adult')\nelse:\n    print('minor')"
                    },
                    "python-loops": {
                        "title":"Loops",
                        "prompt":"Use a for loop to print the numbers 1 through 5, one per line.",
                        "starter":"# Write your solution here\n",
                        "hint":"range(1, 6) produces 1 through 5.",
                        "tests":["for ","range(1, 6)","print("],
                        "solution":"for i in range(1, 6):\n    print(i)"
                    },
                    "python-functions": {
                        "title":"Functions",
                        "prompt":"Write greet(name) so that greet('Sam') returns 'Hello, Sam!'.",
                        "starter":"def greet(name):\n    # return the greeting\n    pass\n",
                        "hint":"Return an f-string containing the name.",
                        "tests":["def greet(","return ","Hello, ","name"],
                        "solution":"def greet(name):\n    return f'Hello, {name}!'"
                    },
                    "python-lists": {
                        "title":"Lists",
                        "prompt":"Create numbers = [10, 20, 30] and print the second item.",
                        "starter":"# Write your solution here\n",
                        "hint":"Python lists use zero-based indexing.",
                        "tests":["numbers = [10, 20, 30]","print(numbers[1])"],
                        "solution":"numbers = [10, 20, 30]\nprint(numbers[1])"
                    }
                }

                @app.post("/api/launch/autosave")
                def autosave():
                    u=user()
                    if not u: return jsonify(error="login_required"),401
                    d=request.get_json(silent=True) or {}
                    if not csrf_ok(d): return jsonify(error="csrf"),400
                    key=str(d.get("item_key",""))[:255]
                    code=str(d.get("code",""))
                    language=str(d.get("language","text"))[:40]
                    if not key or len(code)>200000: return jsonify(error="invalid"),400
                    con=mod.db()
                    con.execute("""INSERT INTO learner_code(user_id,item_key,code,language)
                                   VALUES(?,?,?,?)
                                   ON CONFLICT(user_id,item_key) DO UPDATE SET code=excluded.code,
                                   language=excluded.language,updated_at=CURRENT_TIMESTAMP""",
                                (u["id"],key,code,language))
                    con.commit(); con.close()
                    return jsonify(ok=True)

                @app.get("/api/launch/autosave/<path:key>")
                def load_autosave(key):
                    u=user()
                    if not u:return jsonify(error="login_required"),401
                    con=mod.db(); row=con.execute("SELECT code,language,updated_at FROM learner_code WHERE user_id=? AND item_key=?",(u["id"],key[:255])).fetchone(); con.close()
                    return jsonify(found=bool(row),code=(row["code"] if row else ""),language=(row["language"] if row else ""),updated_at=(str(row["updated_at"]) if row else None))

                @app.post("/api/launch/exercise")
                def exercise():
                    u=user()
                    if not u:return jsonify(error="login_required"),401
                    d=request.get_json(silent=True) or {}
                    if not csrf_ok(d):return jsonify(error="csrf"),400
                    key=str(d.get("exercise_key",""))
                    answer=str(d.get("answer",""))
                    ex=exercises.get(key)
                    if not ex or len(answer)>20000:return jsonify(error="invalid"),400
                    normalized=" ".join(answer.lower().split())
                    passed=all(" ".join(t.lower().split()) in normalized for t in ex["tests"])
                    con=mod.db()
                    con.execute("INSERT INTO exercise_attempts(user_id,exercise_key,passed,answer) VALUES(?,?,?,?)",(u["id"],key,int(passed),answer))
                    con.commit();con.close()
                    if passed: xp(25)
                    return jsonify(passed=passed,tests=len(ex["tests"]),message=("All checks passed. +25 XP" if passed else "Not quite yet. Check the requirements and try again."),solution=ex["solution"] if d.get("reveal") else None)

                @app.get("/exercises")
                def exercises_page():
                    cards=[]
                    for key,ex in exercises.items():
                        cards.append(f'<a class="card launch-exercise-card" href="/exercise/{html.escape(key)}"><div class="eyebrow">HANDS-ON</div><h2>{html.escape(ex["title"])}</h2><p>{html.escape(ex["prompt"])}</p><span class="btn">Open exercise →</span></a>')
                    return layout(f'<section class="section feature-shell"><div class="eyebrow">PRACTICE</div><h1>Build it. Run it. Pass it.</h1><p class="launch-intro">Short, testable exercises that make lessons practical instead of passive.</p><div class="grid launch-grid">{"".join(cards)}</div></section>',"Exercises","Hands-on coding exercises")

                @app.get("/exercise/<key>")
                def exercise_page(key):
                    ex=exercises.get(key)
                    if not ex:return ("Not found",404)
                    u=user()
                    csrf=html.escape(str(mod.csrf())) if u else ""
                    login_note="" if u else '<div class="notice">Log in to submit attempts and save progress.</div>'
                    body=f'''<section class="section feature-shell">
<a class="hint" href="/exercises">← All exercises</a>
<div class="eyebrow" style="margin-top:30px">HANDS-ON EXERCISE</div>
<h1>{html.escape(ex["title"])}</h1>
<div class="card launch-exercise"><p class="exercise-prompt">{html.escape(ex["prompt"])}</p>
<textarea id="answer" spellcheck="false" placeholder="Write your solution here…">{html.escape(ex["starter"])}</textarea>
<div class="actions"><button class="btn primary" id="submit">▶ Submit</button><button class="btn" id="hint">Hint</button><button class="btn" id="solution">Show solution</button></div>
<div id="result" class="notice" style="display:none"></div><pre id="sol" class="output" style="display:none">{html.escape(ex["solution"])}</pre>{login_note}</div></section>
<script>
const csrf="{csrf}", key="{html.escape(key)}", area=document.getElementById("answer");
let saveTimer=null;
async function save(){{if(!csrf)return;clearTimeout(saveTimer);saveTimer=setTimeout(()=>fetch("/api/launch/autosave",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{csrf,item_key:"exercise:"+key,code:area.value,language:"python"}})}}),500)}}
area.addEventListener("input",save);
document.getElementById("submit").onclick=async()=>{{if(!csrf){{location.href="/login";return}};const r=await fetch("/api/launch/exercise",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{csrf,exercise_key:key,answer:area.value}})}});const d=await r.json();result.textContent=d.message||"Submitted";result.style.display="block";}};
document.getElementById("hint").onclick=()=>{{result.textContent="{html.escape(ex["hint"])}";result.style.display="block"}};
document.getElementById("solution").onclick=()=>sol.style.display="block";
</script>'''
                    return layout(body,ex["title"],"Hands-on coding exercise")

                @app.post("/api/launch/feedback")
                def feedback():
                    d=request.get_json(silent=True) or {}
                    if not csrf_ok(d):return jsonify(error="csrf"),400
                    key=str(d.get("item_key",""))[:255]
                    rating=str(d.get("rating",""))[:20]
                    reason=str(d.get("reason",""))[:80]
                    message=str(d.get("message",""))[:4000]
                    if rating not in ("helpful","not_helpful") or not key:return jsonify(error="invalid"),400
                    u=user(); uid=u["id"] if u else None
                    con=mod.db();con.execute("INSERT INTO lesson_feedback(user_id,item_key,rating,reason,message) VALUES(?,?,?,?,?)",(uid,key,rating,reason,message));con.commit();con.close()
                    return jsonify(ok=True)

                @app.post("/api/launch/bug")
                def bug():
                    d=request.get_json(silent=True) or {}
                    if not csrf_ok(d):return jsonify(error="csrf"),400
                    message=str(d.get("message","")).strip()[:4000]
                    category=str(d.get("category","Other"))[:80]
                    if not message:return jsonify(error="message_required"),400
                    u=user();uid=u["id"] if u else None
                    con=mod.db();con.execute("INSERT INTO bug_reports(user_id,page_url,category,message) VALUES(?,?,?,?)",(uid,str(d.get("page_url",""))[:1000],category,message));con.commit();con.close()
                    return jsonify(ok=True)

                @app.get("/contact")
                def contact():
                    csrf=html.escape(str(mod.csrf()))
                    return layout(f'''<section class="section feature-shell"><div class="eyebrow">CONTACT</div><h1>Tell us what needs fixing.</h1><p>Found a broken lesson, confusing explanation, or UI problem? Send a report directly from here.</p><div class="card launch-form"><label>Category</label><select id="cat"><option>Bug</option><option>Lesson issue</option><option>Content error</option><option>Suggestion</option><option>Other</option></select><label>What happened?</label><textarea id="msg" maxlength="4000" placeholder="Describe the problem clearly…"></textarea><button class="btn primary" id="send">Send report</button><div id="status" class="notice" style="display:none"></div></div></section><script>send.onclick=async()=>{{const m=msg.value.trim();if(!m){{status.textContent="Please describe the issue.";status.style.display="block";return}};const r=await fetch("/api/launch/bug",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{csrf:"{csrf}",category:cat.value,message:m,page_url:location.href}})}});status.textContent=r.ok?"Report received. Thanks.":"Could not send the report.";status.style.display="block";if(r.ok)msg.value=""}};</script>''',"Contact","Report a problem or contact EaseWithPy")

                def legal(title, eyebrow, body):
                    return layout(f'<section class="section feature-shell legal-page"><div class="eyebrow">{html.escape(eyebrow)}</div><h1>{html.escape(title)}</h1>{body}</section>',title,title)

                @app.get("/about")
                def about():
                    return legal("About EaseWithPy","ABOUT","<p>EaseWithPy is an independent programming-learning platform focused on practical lessons, interactive practice, projects and tools for learners at different stages.</p><h2>Our focus</h2><p>Explain concepts clearly, show working syntax, let learners practice, and make progress easy to track.</p>")

                @app.get("/privacy")
                def privacy():
                    return legal("Privacy","PRIVACY","<h2>What we store</h2><p>Account details and learning activity are stored to provide accounts, progress tracking, saved items and related features. Exercise drafts may be saved when you are signed in.</p><h2>What you should not submit</h2><p>Do not submit passwords, payment credentials, government identifiers, or other sensitive information into lessons, notes, exercises or feedback.</p><h2>Control</h2><p>Use the account controls available on the platform to manage your account. Contact the site operator if you need help with an account or data request.</p>")

                @app.get("/terms")
                def terms():
                    return legal("Terms of Use","TERMS","<h2>Use of the service</h2><p>Use EaseWithPy lawfully and do not attempt unauthorized access, abuse the service, interfere with other users, or upload malicious content.</p><h2>Educational content</h2><p>Examples are provided for learning. Test code and verify important technical or operational decisions before using them in production.</p><h2>Accounts</h2><p>You are responsible for keeping your account credentials secure and for activity performed through your account.</p>")

                @app.get("/disclaimer")
                def disclaimer():
                    return legal("Educational Disclaimer","DISCLAIMER","<p>EaseWithPy is an educational resource. Code, security guidance, cloud instructions and other technical material can become outdated or behave differently across environments. Verify important decisions against current authoritative documentation and test before production use.</p>")

                # Security baseline. Keep these headers conservative and compatible with the existing inline scripts.
                @app.after_request
                def launch_headers(response):
                    response.headers.setdefault("X-Content-Type-Options","nosniff")
                    response.headers.setdefault("X-Frame-Options","SAMEORIGIN")
                    response.headers.setdefault("Referrer-Policy","strict-origin-when-cross-origin")
                    response.headers.setdefault("Permissions-Policy","camera=(), microphone=(), geolocation=()")
                    response.headers.setdefault("Cross-Origin-Opener-Policy","same-origin-allow-popups")
                    if request.is_secure:
                        response.headers.setdefault("Strict-Transport-Security","max-age=31536000; includeSubDomains")
                    return response

                # Friendly production errors without exposing stack traces.
                def err_page(code,title,message):
                    return layout(f'<section class="section feature-shell error-page"><div class="eyebrow">{code}</div><h1>{html.escape(title)}</h1><p>{html.escape(message)}</p><div class="actions"><a class="btn primary" href="/">Go home</a><a class="btn" href="/courses">Browse courses</a></div></section>',title,message)
                app.register_error_handler(404, lambda e: err_page(404,"That page is not here.","The page may have moved or the URL may be incorrect."))
                app.register_error_handler(500, lambda e: err_page(500,"Something went wrong.","The problem has been recorded by the server. Please try again in a moment."))

                # Add launch links without touching admin routes.
                original_layout=layout
                def launch_layout(content,title="",description=""):
                    page=original_layout(content,title,description)
                    marker='<a class="launch-nav-link" href="/exercises">Exercises</a>'
                    if marker not in page and "</nav>" in page:
                        page=page.replace("</nav>",marker+"</nav>",1)
                    style='''<style>
.launch-intro{max-width:800px;font-size:18px}.launch-grid{margin-top:28px}.launch-exercise-card{display:flex;flex-direction:column;gap:8px}.launch-exercise-card .btn{align-self:flex-start}.launch-exercise{max-width:900px}.launch-exercise textarea,.launch-form textarea{min-height:260px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}.launch-form{max-width:760px;display:grid;gap:10px}.launch-form label{margin-top:8px}.legal-page{max-width:900px}.error-page{text-align:center;padding-top:100px;padding-bottom:120px}.error-page p{max-width:700px;margin:0 auto 24px}.launch-nav-link{margin-left:10px}
@media(max-width:600px){.launch-nav-link{display:none}.launch-exercise textarea,.launch-form textarea{min-height:220px}.error-page{padding-top:70px}}
</style>'''
                    return page.replace("</head>",style+"</head>",1)
                mod.layout=launch_layout
                app.layout=launch_layout

                print("[EaseWithPy] launch-readiness layer installed")
                return
            except Exception as e:
                print("[EaseWithPy] launch layer retry:",repr(e))
                traceback.print_exc()
                time.sleep(1)
    threading.Thread(target=boot,daemon=True).start()
