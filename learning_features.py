"""EaseWithPy learning-platform features: interactive labs, progression, social practice and learner utilities."""
import html, json, time

def install():
    def boot():
        for _ in range(120):
            try:
                mod = __import__("app")
                app = getattr(mod, "APP", None)
                layout = getattr(mod, "layout", None)
                if app is None or layout is None:
                    time.sleep(.25); continue
                from flask import request, jsonify, Response, redirect

                con = mod.db()
                con.executescript("""
                CREATE TABLE IF NOT EXISTS learner_meta(user_id INTEGER PRIMARY KEY,xp INTEGER DEFAULT 0,streak INTEGER DEFAULT 0,last_active TEXT NULL,theme TEXT DEFAULT 'dark');
                CREATE TABLE IF NOT EXISTS bookmarks(user_id INTEGER NOT NULL,item_key VARCHAR(255) NOT NULL,title VARCHAR(500) NOT NULL,href VARCHAR(1000) NOT NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY(user_id,item_key));
                CREATE TABLE IF NOT EXISTS learner_notes(user_id INTEGER NOT NULL,item_key VARCHAR(255) NOT NULL,note TEXT NOT NULL,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY(user_id,item_key));
                CREATE TABLE IF NOT EXISTS learner_activity(user_id INTEGER NOT NULL,item_key VARCHAR(255) NOT NULL,title VARCHAR(500) NOT NULL,href VARCHAR(1000) NOT NULL,seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY(user_id,item_key));
                """)
                con.commit(); con.close()

                def current_user(): return mod.user()
                def auth_json():
                    u=current_user()
                    return (u,None) if u else (None,(jsonify(error="login_required"),401))
                def csrf_ok():
                    d=request.get_json(silent=True) or request.form
                    return mod.secrets.compare_digest(str(d.get("csrf","")),str(mod.session.get("csrf","")))
                def award_xp(amount):
                    u=current_user()
                    if not u:return 0
                    con=mod.db(); row=con.execute("SELECT xp FROM learner_meta WHERE user_id=?",(u["id"],)).fetchone()
                    if row: con.execute("UPDATE learner_meta SET xp=xp+?,last_active=CURRENT_TIMESTAMP WHERE user_id=?",(amount,u["id"]))
                    else: con.execute("INSERT INTO learner_meta(user_id,xp,streak,last_active) VALUES(?,?,1,CURRENT_TIMESTAMP)",(u["id"],amount))
                    con.commit(); total=(int(row["xp"]) if row else 0)+amount; con.close(); return total
                def shell(title,eyebrow,intro,body):
                    return layout(f'<section class="section feature-shell"><div class="eyebrow">{html.escape(eyebrow)}</div><h1 style="font-size:clamp(42px,7vw,76px);max-width:950px">{html.escape(title)}</h1><p style="font-size:18px;max-width:850px">{html.escape(intro)}</p>{body}</section>',title,intro)

                @app.get("/playground")
                def playground():
                    starter="print('Hello, EaseWithPy!')"
                    body=f'''<div class="labtoolbar"><select id="lang"><option value="python">Python</option><option value="javascript">JavaScript</option><option value="typescript">TypeScript</option><option value="html">HTML</option><option value="css">CSS</option></select><button id="run" class="btn primary">▶ Run</button><button id="clear" class="btn">Clear</button><button id="reset" class="btn">Reset</button></div><textarea id="code" spellcheck="false">{html.escape(starter)}</textarea><div class="eyebrow" style="margin-top:18px">OUTPUT</div><pre id="out" class="output">Ready.</pre><div class="card" style="margin-top:18px"><b>Local execution</b><p>JavaScript runs in your browser. Python loads Pyodide in the browser. Editor code is not sent to the EaseWithPy server.</p></div>
<script>
const initial={json.dumps(starter)},ed=document.getElementById("code"),out=document.getElementById("out"),lang=document.getElementById("lang");
reset.onclick=()=>{{ed.value=initial;out.textContent="Ready."}};clear.onclick=()=>out.textContent="";
lang.onchange=()=>{{ed.value=lang.value==="python"?"print('Hello, EaseWithPy!')":lang.value==="javascript"?"console.log('Hello, EaseWithPy!')":lang.value==="typescript"?"const message: string = 'Hello, EaseWithPy!'; console.log(message)":lang.value==="html"?"<h1>Hello, EaseWithPy!</h1>":"body {{ font-family: system-ui; }}"}}};
run.onclick=async()=>{{const src=ed.value,l=lang.value;out.textContent="Running…";if(l==="python"){{try{{if(!window.pyodide){{out.textContent="Loading Python runtime…";window.pyodide=await loadPy()}}let a=[];pyodide.setStdout({{batched:s=>a.push(s)}});await pyodide.runPythonAsync(src);out.textContent=a.join("\\n")||"✓ Finished."}}catch(e){{out.textContent=String(e)}}}}else if(l==="javascript"||l==="typescript"){{try{{let a=[];new Function("console",src.replace(/:\\s*(string|number|boolean|any)(?=[,)=;])/g,""))({{log:(...x)=>a.push(x.join(" "))}});out.textContent=a.join("\\n")||"✓ Finished."}}catch(e){{out.textContent=String(e)}}}}else{{const w=window.open();w.document.write(l==="html"?src:"<style>"+src+"</style><div>Preview</div>");w.document.close();out.textContent="Preview opened."}};awardXP(5)}};
function loadPy(){{return new Promise((resolve,reject)=>{{if(window.loadPyodide)return window.loadPyodide({{indexURL:"https://cdn.jsdelivr.net/pyodide/v0.27.7/full/"}}).then(resolve,reject);const s=document.createElement("script");s.src="https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js";s.onload=()=>window.loadPyodide({{indexURL:"https://cdn.jsdelivr.net/pyodide/v0.27.7/full/"}}).then(resolve,reject);s.onerror=reject;document.head.appendChild(s)}})}}
async function awardXP(n){{try{{await fetch("/api/feature/xp",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{csrf:"{html.escape(str(mod.csrf()))}",amount:n}})}})}}catch(e){{}}}}
</script>'''
                    return shell("Code Playground","BUILD MODE","Experiment without leaving the platform. Use it to learn, test and prototype.",body)

                @app.get("/visualizer")
                def visualizer():
                    body='''<div class="grid" style="margin-top:28px">
<div class="card"><div class="eyebrow">DATA STRUCTURES</div><h2>Stack / Queue</h2><div id="ds" class="viz"></div><div class="actions"><button class="btn" onclick="pushV()">Push</button><button class="btn" onclick="popV()">Pop</button><button class="btn" onclick="enqueue()">Enqueue</button><button class="btn" onclick="dequeue()">Dequeue</button></div></div>
<div class="card"><div class="eyebrow">ALGORITHM</div><h2>Bubble sort</h2><div id="sort" class="viz"></div><button class="btn primary" onclick="sortV()">Animate sort</button></div>
</div><div class="card" style="margin-top:18px"><div class="eyebrow">EXECUTION VISUALIZER</div><h2>Step through a loop</h2><pre id="exec" class="output">Press Step to execute the next iteration.</pre><button class="btn primary" onclick="stepV()">Step</button><button class="btn" onclick="resetV()">Reset</button></div>
<script>
let stack=[3,7,2],queue=[1,4,8],arr=[5,2,9,1,6],step=0;function draw(){ds.innerHTML="<b>Stack:</b> "+stack.map(x=>"<span class='vizbox'>"+x+"</span>").join("")+"<br><b>Queue:</b> "+queue.map(x=>"<span class='vizbox'>"+x+"</span>").join("");sort.innerHTML=arr.map(x=>"<span class='vizbar' style='height:"+Math.max(20,x*14)+"px'>"+x+"</span>").join("")}function pushV(){stack.push(Math.floor(Math.random()*9)+1);draw()}function popV(){stack.pop();draw()}function enqueue(){queue.push(Math.floor(Math.random()*9)+1);draw()}function dequeue(){queue.shift();draw()}function sortV(){arr.sort((a,b)=>a-b);draw()}function stepV(){step++;exec.textContent="for i in range(3):\\n  i = "+((step-1)%3)+"\\n  print(i)\\n\\nCurrent step: "+step}function resetV(){step=0;exec.textContent="Press Step to execute the next iteration."}draw();
</script>'''
                    return shell("Visual Learning Lab","SEE THE CONCEPT","Interact with stacks, queues, sorting and program execution instead of only reading about them.",body)

                @app.get("/practice-lab")
                def practice_lab():
                    problems=[
                        ("Python","Variables","Create a variable called score with the value 100 and print it."),
                        ("Python","Lists","Create a list of three languages and print the second item."),
                        ("Python","Loops","Use a loop to print the numbers 1 through 5."),
                        ("Python","Functions","Write a function named greet that accepts a name and returns a greeting."),
                        ("SQL","Filtering","Write a query that selects rows where active equals 1."),
                        ("JavaScript","Arrays","Create an array of three numbers and print the first one."),
                        ("Git","Commits","Write the command that records staged changes with the message 'first commit'."),
                        ("Web","HTML","Create a button whose visible text is 'Start'.")
                    ]
                    body=f'''<div class="card"><div class="stats"><span id="pcat"></span><span id="ptopic"></span><span id="pnum"></span></div><h2 id="prompt"></h2><textarea id="attempt" placeholder="Write your solution or explain your approach…"></textarea><div class="actions"><button class="btn primary" id="newp">New problem</button><button class="btn" id="hint">Hint</button><button class="btn" id="answer">Show answer</button></div><div id="feedback" class="notice" style="display:none"></div></div>
<script>
const problems={json.dumps(problems,separators=(",",":"))};let pi=Math.floor(Math.random()*problems.length);function drawP(){{const p=problems[pi];pcat.textContent=p[0];ptopic.textContent=p[1];pnum.textContent="Problem "+(pi+1)+" / "+problems.length;prompt.textContent=p[2];attempt.value="";feedback.style.display="none"}}newp.onclick=()=>{{pi=Math.floor(Math.random()*problems.length);drawP()}};hint.onclick=()=>{{feedback.textContent="Hint: identify the exact syntax or operation the prompt is asking for, then test the smallest working version.";feedback.style.display="block"}};answer.onclick=()=>{{feedback.textContent="Open the relevant lesson and implement the smallest solution yourself before comparing with a reference.";feedback.style.display="block"}};drawP();
</script>'''
                    return shell("Practice Generator","ACTIVE RECALL","Generate a different small problem, attempt it yourself, then use the lesson material to verify your approach.",body)

                @app.get("/interview")
                def interview():
                    qs=[("Python","What is the difference between a list and a tuple?","Lists are mutable; tuples are immutable."),("Python","What does a dictionary map?","Keys to values."),("Web","What does HTTP 404 mean?","The requested resource was not found."),("SQL","Why use a parameterized query?","It separates data from SQL syntax and reduces injection risk."),("Git","What does a commit represent?","A recorded snapshot of staged changes."),("JavaScript","What is a Promise?","An object representing the eventual result of an asynchronous operation."),("Systems","What is caching used for?","To reuse stored results and reduce repeated work or latency."),("Security","What is authentication?","Verifying identity; authorization decides what it may do.")]
                    body=f'''<div class="card interview-card"><div class="stats"><span id="iqcat"></span><span id="iqnum"></span></div><h2 id="iq"></h2><textarea id="ia" placeholder="Type your answer first…"></textarea><div class="actions"><button id="reveal" class="btn primary">Reveal answer</button><button id="nextq" class="btn">Next</button></div><div id="ians" class="notice" style="display:none"></div></div><script>const qs={json.dumps(qs,separators=(",",":"))};let qi=0;function drawQ(){{const q=qs[qi];iqcat.textContent=q[0];iqnum.textContent=(qi+1)+" / "+qs.length;iq.textContent=q[1];ia.value="";ians.style.display="none"}}reveal.onclick=()=>{{ians.textContent="Model answer: "+qs[qi][2];ians.style.display="block"}};nextq.onclick=()=>{{qi=(qi+1)%qs.length;drawQ()}};drawQ();</script>'''
                    return shell("Interview Mode","INTERVIEW PRACTICE","Practice explaining concepts before seeing the model answer.",body)

                @app.get("/battles")
                def battles():
                    body='''<div class="grid" style="margin-top:28px"><div class="card"><div class="eyebrow">SOLO</div><h2>Beat the clock</h2><p>Use timed challenges to practice under pressure.</p><a class="btn primary" href="/timed">Start timed challenge →</a></div><div class="card"><div class="eyebrow">ROOMS</div><h2>Battle lobby</h2><p>Create a room code and compare challenge results with friends.</p><button class="btn primary" onclick="makeRoom()">Create room</button><p id="room" class="snippet">No room yet.</p></div></div><script>function makeRoom(){{const c="ROOM-"+Math.random().toString(36).slice(2,8).toUpperCase();room.textContent=c;navigator.clipboard?.writeText(c)}}</script>'''
                    return shell("Coding Battles","COMPETE","Practice under pressure without making competition the measure of programming ability.",body)

                @app.get("/leaderboard")
                def leaderboard():
                    con=mod.db(); rows=con.execute("SELECT u.name,COALESCE(m.xp,0) xp FROM users u LEFT JOIN learner_meta m ON m.user_id=u.id ORDER BY xp DESC LIMIT 50").fetchall(); con.close()
                    body='<div class="card" style="margin-top:28px">'
                    body+=''.join(f'<div class="leader-row"><span>#{i}</span><b>{html.escape(str(r["name"]))}</b><span>{int(r["xp"])} XP</span></div>' for i,r in enumerate(rows,1)) or '<p>No scores yet. Be the first.</p>'
                    return shell("Leaderboard","COMMUNITY","A simple XP activity board. XP reflects platform activity, not programming ability.",body+'</div>')

                @app.get("/achievements")
                def achievements():
                    u=current_user()
                    if not u:return redirect("/login")
                    con=mod.db(); done=int(con.execute("SELECT COUNT(*) n FROM progress WHERE user_id=? AND completed=1",(u["id"],)).fetchone()["n"]); xp=int((con.execute("SELECT COALESCE(xp,0) xp FROM learner_meta WHERE user_id=?",(u["id"],)).fetchone() or {"xp":0})["xp"]); bm=int(con.execute("SELECT COUNT(*) n FROM bookmarks WHERE user_id=?",(u["id"],)).fetchone()["n"]); con.close()
                    badges=[("FIRST STEP","Complete your first lesson",done>=1),("TEN DOWN","Complete 10 lessons",done>=10),("CENTURY","Complete 100 lessons",done>=100),("XP HUNTER","Earn 500 XP",xp>=500),("XP ENGINE","Earn 2000 XP",xp>=2000),("BOOKMARKER","Save 5 bookmarks",bm>=5)]
                    cards=''.join(f'<div class="badge-card {"unlocked" if ok else ""}"><div class="badge-icon">{"✓" if ok else "○"}</div><b>{html.escape(t)}</b><p>{html.escape(d)}</p></div>' for t,d,ok in badges)
                    return shell("Achievements & Badges","YOUR MILESTONES","Unlock badges by learning, practicing and returning.",f'<div class="badge-grid" style="margin-top:28px">{cards}</div>')

                @app.get("/timed")
                def timed():
                    ps=[("Easy","Write a Python expression that returns the length of a list called items.","len(items)"),("Medium","Filter even numbers from nums.","[x for x in nums if x % 2 == 0]"),("Medium","Select active users from users in SQL.","SELECT * FROM users WHERE active = 1;"),("Hard","Double every value in nums with JavaScript.","nums.map(x => x * 2)")]
                    body=f'''<div class="card"><div class="stats"><span id="difficulty"></span><span id="clock">01:00</span></div><h2 id="problem"></h2><textarea id="answer" placeholder="Write your solution…"></textarea><div class="actions"><button class="btn primary" id="start">Start 60s</button><button class="btn" id="show">Show reference</button><button class="btn" id="next">Next</button></div><pre id="reference" class="output" style="display:none"></pre></div><script>const ps={json.dumps(ps,separators=(",",":"))};let pi=0,t=60,timer=null;function draw(){{difficulty.textContent=ps[pi][0];problem.textContent=ps[pi][1];answer.value="";reference.style.display="none";reference.textContent="Reference: "+ps[pi][2]}}start.onclick=()=>{{clearInterval(timer);t=60;clock.textContent="01:00";timer=setInterval(()=>{{t--;clock.textContent="00:"+String(t).padStart(2,"0");if(t<=0){{clearInterval(timer);reference.style.display="block"}}}},1000)}};show.onclick=()=>reference.style.display="block";next.onclick=()=>{{pi=(pi+1)%ps.length;draw()}};draw();</script>'''
                    return shell("Timed Challenges","SPEED + ACCURACY","Short timed exercises for syntax recall and interview pressure.",body)

                @app.get("/search")
                def global_search():
                    return shell("Search Everything","FIND IT FAST","Search courses and lessons from one place.",'''<input id="gq" class="searchbox" placeholder="Search Python, FastAPI, loops, SQL…"><div id="results" class="grid"></div><script>const q=document.getElementById("gq"),r=document.getElementById("results");async function go(){{const x=q.value.trim();if(!x){{r.innerHTML="";return}}const z=await fetch("/api/feature/search?q="+encodeURIComponent(x)).then(x=>x.json());r.innerHTML=z.results.map(a=>'<a class="card" href="'+a.href+'"><h3>'+a.title+'</h3><p>'+a.kind+'</p></a>').join("")||'<div class="card"><p>No results.</p></div>'}}q.oninput=go;</script>''')

                @app.get("/settings")
                def settings():
                    u=current_user()
                    if not u:return redirect("/login")
                    return shell("Learning Settings","PREFERENCES","Control the appearance and shortcuts of your learning space.",'''<div class="card" style="max-width:700px;margin-top:28px"><h2>Appearance</h2><div class="actions"><button class="btn" onclick="setTheme('dark')">Dark</button><button class="btn" onclick="setTheme('light')">Light</button><button class="btn" onclick="setTheme('system')">System</button></div><h2 style="margin-top:35px">Keyboard shortcuts</h2><p><kbd>Ctrl/Cmd + K</kbd> command palette · <kbd>G</kbd> then <kbd>P</kbd> playground · <kbd>G</kbd> then <kbd>C</kbd> courses</p></div><script>function setTheme(t){{localStorage.setItem("ease-theme",t);applyTheme()}}function applyTheme(){{const t=localStorage.getItem("ease-theme")||"dark";document.documentElement.dataset.theme=t;if(t==="light")document.body.style.background="#f6f6f6";else document.body.style.background=""}}applyTheme()</script>''')

                @app.post("/api/feature/xp")
                def feature_xp():
                    u,err=auth_json()
                    if err:return err
                    if not csrf_ok():return jsonify(error="csrf"),400
                    d=request.get_json(silent=True) or {}; amount=max(0,min(50,int(d.get("amount",0))))
                    return jsonify(ok=True,xp=award_xp(amount))

                @app.post("/api/feature/bookmark")
                def bookmark():
                    u,err=auth_json()
                    if err:return err
                    if not csrf_ok():return jsonify(error="csrf"),400
                    d=request.get_json(silent=True) or {}; key=str(d.get("key",""))[:255]; title=str(d.get("title",""))[:500]; href=str(d.get("href",""))[:1000]
                    if not key or not href:return jsonify(error="invalid"),400
                    con=mod.db();con.execute("INSERT INTO bookmarks(user_id,item_key,title,href) VALUES(?,?,?,?) ON CONFLICT(user_id,item_key) DO UPDATE SET title=excluded.title,href=excluded.href", (u["id"],key,title,href));con.commit();con.close();return jsonify(ok=True)

                @app.delete("/api/feature/bookmark")
                def unbookmark():
                    u,err=auth_json()
                    if err:return err
                    if not csrf_ok():return jsonify(error="csrf"),400
                    key=str((request.get_json(silent=True) or {}).get("key",""))[:255]
                    con=mod.db();con.execute("DELETE FROM bookmarks WHERE user_id=? AND item_key=?",(u["id"],key));con.commit();con.close();return jsonify(ok=True)

                @app.post("/api/feature/note")
                def save_note():
                    u,err=auth_json()
                    if err:return err
                    if not csrf_ok():return jsonify(error="csrf"),400
                    d=request.get_json(silent=True) or {};key=str(d.get("key",""))[:255];note=str(d.get("note",""))[:5000]
                    con=mod.db();con.execute("INSERT INTO learner_notes(user_id,item_key,note) VALUES(?,?,?) ON CONFLICT(user_id,item_key) DO UPDATE SET note=excluded.note,updated_at=CURRENT_TIMESTAMP",(u["id"],key,note));con.commit();con.close();return jsonify(ok=True)

                @app.get("/api/feature/library")
                def library_state():
                    u,err=auth_json()
                    if err:return err
                    con=mod.db();bm=con.execute("SELECT item_key,title,href FROM bookmarks WHERE user_id=? ORDER BY created_at DESC LIMIT 100",(u["id"],)).fetchall();notes=con.execute("SELECT item_key,note FROM learner_notes WHERE user_id=?",(u["id"],)).fetchall();recent=con.execute("SELECT item_key,title,href FROM learner_activity WHERE user_id=? ORDER BY seen_at DESC LIMIT 12",(u["id"],)).fetchall();con.close()
                    return jsonify(bookmarks=[dict(x) for x in bm],notes=[dict(x) for x in notes],recent=[dict(x) for x in recent])

                @app.post("/api/feature/activity")
                def activity():
                    u,err=auth_json()
                    if err:return err
                    if not csrf_ok():return jsonify(error="csrf"),400
                    d=request.get_json(silent=True) or {};key=str(d.get("key",""))[:255];title=str(d.get("title",""))[:500];href=str(d.get("href",""))[:1000]
                    con=mod.db();con.execute("INSERT INTO learner_activity(user_id,item_key,title,href) VALUES(?,?,?,?) ON CONFLICT(user_id,item_key) DO UPDATE SET title=excluded.title,href=excluded.href,seen_at=CURRENT_TIMESTAMP",(u["id"],key,title,href));con.commit();con.close();return jsonify(ok=True)

                @app.get("/api/feature/search")
                def feature_search():
                    q=(request.args.get("q") or "").strip().lower()
                    if not q:return jsonify(results=[])
                    try:
                        from course_registry import extra_courses
                        from additional_courses import COURSES as legacy
                        courses=extra_courses(mod.COURSE,legacy)
                    except Exception: courses=legacy
                    results=[{"kind":"Course","title":"Python","href":"/course/python"}]
                    for c in courses:
                        results.append({"kind":"Course","title":c["title"],"href":"/course/"+c["slug"]})
                        for i,l in enumerate(c.get("lessons",[]),1):results.append({"kind":"Lesson · "+c["title"],"title":l.get("title","Lesson"),"href":f"/learn/{c['slug']}/{i}"})
                    for i,l in enumerate(mod.COURSE,1):results.append({"kind":"Lesson · Python","title":l.get("title","Lesson"),"href":f"/learn/{i}"})
                    return jsonify(results=[x for x in results if q in (x["title"]+" "+x["kind"]).lower()][:30])

                @app.get("/manifest.webmanifest")
                def manifest(): return jsonify(name="EaseWithPy",short_name="EaseWithPy",start_url="/",display="standalone",background_color="#050505",theme_color="#050505",icons=[])
                @app.get("/sw.js")
                def sw():
                    return Response("""const CACHE='easewithpy-v1';const ASSETS=['/','/courses','/playground','/manifest.webmanifest'];self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS))));self.addEventListener('fetch',e=>{if(e.request.method==='GET')e.respondWith(caches.match(e.request).then(x=>x||fetch(e.request).then(r=>{const c=r.clone();caches.open(CACHE).then(k=>k.put(e.request,c));return r}).catch(()=>caches.match('/'))))});""",mimetype="application/javascript")

                old_layout=layout
                def upgraded_layout(content,title="EaseWithPy",description=None):
                    base=old_layout(content,title)
                    base=base.replace('<div class="navlinks">','<div class="navlinks"><a href="/playground">Playground</a><a href="/practice-lab">Practice Lab</a><a href="/visualizer">Visualize</a><a href="/projects">Projects</a>',1)
                    base=base.replace('</head>','<style>.feature-shell{padding-bottom:80px}.labtoolbar{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0 12px}.labtoolbar select{background:#0d0d0d;color:#fff;border:1px solid #292929;border-radius:10px;padding:10px}.leader-row{display:grid;grid-template-columns:60px 1fr auto;gap:12px;padding:14px;border-bottom:1px solid #292929}.badge-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.badge-card{padding:20px;border:1px solid #292929;border-radius:16px;background:#0d0d0d}.badge-card.unlocked{border-color:#777}.badge-icon{font-size:28px;margin-bottom:12px}.viz{min-height:100px;padding:18px;background:#080808;border:1px solid #292929;border-radius:12px;margin:14px 0;display:flex;gap:7px;align-items:flex-end;flex-wrap:wrap}.vizbox{display:inline-flex;padding:10px 14px;border:1px solid #444;border-radius:8px;background:#151515}.vizbar{display:inline-flex;width:34px;min-height:20px;background:#aaa;color:#000;align-items:flex-end;justify-content:center;border-radius:5px 5px 0 0}.cmd-overlay{position:fixed;inset:0;background:#000a;z-index:9999;padding:12vh 5vw}.cmd{max-width:720px;margin:auto;background:#0d0d0d;border:1px solid #444;border-radius:18px;padding:14px;box-shadow:0 30px 100px #000}.cmd input{width:100%;background:#080808;color:#fff;border:1px solid #333;border-radius:10px;padding:15px}.cmd a{display:flex;justify-content:space-between;padding:13px;border-radius:9px}.cmd a:hover{background:#181818}.cmd small{color:#888}.searchbox{margin-top:25px}.kbd,kbd{border:1px solid #444;border-bottom-width:2px;border-radius:5px;padding:2px 6px;background:#111;color:#ddd}@media(max-width:800px){.badge-grid{grid-template-columns:1fr}.leader-row{grid-template-columns:45px 1fr auto}.labtoolbar>*{flex:1}.feature-shell{padding-top:25px}}</style></head>',1)
                    base=base.replace('</body>','''<div id="cmd" class="cmd-overlay" hidden><div class="cmd"><input id="cmdq" placeholder="⌘K · Search EaseWithPy"><div id="cmdr"></div></div></div><script>
if("serviceWorker" in navigator)navigator.serviceWorker.register("/sw.js").catch(()=>{});
document.addEventListener("keydown",e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==="k"){e.preventDefault();const x=document.getElementById("cmd");if(x){x.hidden=false;document.getElementById("cmdq").focus()}}if(e.key==="Escape"){const x=document.getElementById("cmd");if(x)x.hidden=true}});
const cq=document.getElementById("cmdq");if(cq)cq.oninput=async()=>{const q=cq.value.trim();if(!q)return;const z=await fetch("/api/feature/search?q="+encodeURIComponent(q)).then(r=>r.json());document.getElementById("cmdr").innerHTML=z.results.slice(0,8).map(x=>'<a href="'+x.href+'"><b>'+x.title+'</b><small>'+x.kind+'</small></a>').join("")};
document.querySelectorAll('a[href^="/learn/"],a[href^="/course/"]').forEach(a=>a.addEventListener("click",()=>fetch("/api/feature/activity",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({csrf:"{html.escape(str(mod.csrf()))}",key:a.getAttribute("href"),title:a.textContent.trim(),href:a.getAttribute("href")})}).catch(()=>{})));
</script></body>''',1)
                    return base
                mod.layout=upgraded_layout;app.layout=upgraded_layout
                print("[EaseWithPy] advanced learner features installed")
                return
            except Exception as e:
                print("[EaseWithPy] feature install retry:",repr(e));time.sleep(1)
    threading.Thread(target=boot,daemon=True).start()
