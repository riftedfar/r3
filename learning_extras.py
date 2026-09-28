"""Final learning-layer additions for EaseWithPy."""
import html, json, time, threading

def install():
    def boot():
        for _ in range(120):
            try:
                mod = __import__("app")
                app = mod.APP
                layout = mod.layout
                from flask import jsonify, redirect, request
                if app is None or layout is None:
                    time.sleep(.25); continue

                def courses():
                    try:
                        from course_registry import extra_courses
                        from additional_courses import COURSES as legacy
                        return [{"slug":"python","title":"Python","lessons":mod.COURSE}] + extra_courses(mod.COURSE, legacy)
                    except Exception:
                        return [{"slug":"python","title":"Python","lessons":mod.COURSE}]

                def find_lesson(slug, n):
                    for c in courses():
                        if c["slug"] == slug and 1 <= n <= len(c["lessons"]):
                            return c, c["lessons"][n-1]
                    return None, None

                def context_for(title, course):
                    t=(title+" "+course).lower()
                    rules=[
                        (["variable","data type","string","boolean","number"], "Real-world connection", "Variables hold the state your application needs: usernames, prices, settings, counters and API responses."),
                        (["list","array","tuple","set","collection"], "Real-world connection", "Collections appear whenever software handles multiple records: search results, shopping carts, users, messages or configuration values."),
                        (["dictionary","map","object"], "Real-world connection", "Key/value structures are common in APIs, JSON payloads, caches and application state because values can be retrieved by a meaningful key."),
                        (["if","conditional","condition","boolean","comparison"], "Real-world connection", "Conditionals implement business rules such as permissions, validation, pricing rules and feature flags."),
                        (["loop","iteration","for ","while"], "Real-world connection", "Loops automate repeated work: processing records, validating inputs, walking files, handling messages and transforming datasets."),
                        (["function","method","lambda"], "Real-world connection", "Functions turn repeated behavior into reusable units, making applications easier to test, maintain and compose."),
                        (["class","object","oop","inheritance"], "Real-world connection", "Objects model related state and behavior in systems such as users, orders, game entities and service clients."),
                        (["exception","error handling","try","catch"], "Real-world connection", "Error handling keeps real applications from collapsing when input is invalid, a network fails or an external service returns an unexpected result."),
                        (["file","filesystem","path"], "Real-world connection", "File APIs power configuration, logs, uploads, exports, caches and local application data."),
                        (["json","api","rest","http"], "Real-world connection", "These concepts are the plumbing behind web applications, mobile apps, integrations and services communicating across a network."),
                        (["sql","database","postgres","mysql","sqlite","query"], "Real-world connection", "Databases store durable application state such as accounts, orders, inventory, analytics and course progress."),
                        (["git","branch","commit","merge"], "Real-world connection", "Version control lets teams review changes, recover history, collaborate safely and ship features without losing working code."),
                        (["docker","container","kubernetes","deploy","ci/cd"], "Real-world connection", "These tools help teams package software consistently, automate delivery and run services reliably across environments."),
                        (["algorithm","sort","search","tree","graph","complexity"], "Real-world connection", "Algorithms determine how efficiently software searches, ranks, routes, schedules and transforms data."),
                        (["security","auth","permission","crypt","vulnerability"], "Real-world connection", "Security concepts protect accounts, data and infrastructure by controlling identity, access and untrusted input."),
                    ]
                    for keys,head,text in rules:
                        if any(k in t for k in keys):
                            return head,text
                    return "Real-world connection", f"This {course} concept becomes useful when you turn isolated examples into a larger application. Look for where the lesson's main idea appears in a real system."

                def challenge_for(title, course):
                    t=title.lower()
                    if any(x in t for x in ["variable","print","syntax","type","string","number","boolean"]):
                        task=f'Create a tiny {course} program that stores one meaningful value related to "{title}" and displays or uses it.'
                    elif any(x in t for x in ["list","array","tuple","set","collection"]):
                        task=f'Create a collection relevant to {course}, add at least three values, then access or transform one of them.'
                    elif any(x in t for x in ["if","condition","comparison","boolean"]):
                        task=f'Write a small {course} example using a condition based on a value you choose. Test both branches.'
                    elif any(x in t for x in ["loop","iteration","for ","while"]):
                        task=f'Write a {course} loop that processes at least five values and produces a visible result.'
                    elif any(x in t for x in ["function","method","lambda"]):
                        task=f'Write a reusable {course} function related to "{title}". Give it an input and make it return a useful result.'
                    elif any(x in t for x in ["class","object","oop","struct"]):
                        task=f'Design one small {course} object related to "{title}" with at least one piece of state and one behavior.'
                    elif any(x in t for x in ["sql","database","query"]):
                        task='Write a small database query for a realistic table. Include a filter or operation directly related to this lesson.'
                    elif any(x in t for x in ["api","http","rest","json"]):
                        task='Design one realistic API request/response for this lesson. Identify the endpoint, input and expected result.'
                    elif any(x in t for x in ["git","branch","commit","merge"]):
                        task='Write the Git commands you would use for the workflow described by this lesson, then explain what each command changes.'
                    else:
                        task=f'Build a 10–20 line mini-example that demonstrates the main idea from "{title}" using {course}. Add one small variation of your own.'
                    return task

                @app.get("/api/lesson-layer/<slug>/<int:n>")
                def lesson_layer(slug,n):
                    c,l=find_lesson(slug,n)
                    if not c: return jsonify(error="not_found"),404
                    title=l.get("title","Lesson")
                    h,t=context_for(title,c["title"])
                    return jsonify(
                        course=c["title"], lesson=title,
                        context={"heading":h,"text":t},
                        challenge=challenge_for(title,c["title"])
                    )

                @app.post("/api/lesson-challenge")
                def lesson_challenge():
                    u=mod.user()
                    if not u: return jsonify(error="login_required"),401
                    d=request.get_json(silent=True) or {}
                    if not mod.secrets.compare_digest(str(d.get("csrf","")),str(mod.session.get("csrf",""))):
                        return jsonify(error="csrf"),400
                    slug=str(d.get("slug",""))[:80]; n=int(d.get("n",0) or 0)
                    c,l=find_lesson(slug,n)
                    if not c: return jsonify(error="not_found"),404
                    con=mod.db()
                    row=con.execute("SELECT xp FROM learner_meta WHERE user_id=?",(u["id"],)).fetchone()
                    if row: con.execute("UPDATE learner_meta SET xp=xp+10,last_active=CURRENT_TIMESTAMP WHERE user_id=?",(u["id"],))
                    else: con.execute("INSERT INTO learner_meta(user_id,xp,streak,last_active) VALUES(?,?,1,CURRENT_TIMESTAMP)",(u["id"],10))
                    con.commit(); xp=int((row["xp"] if row else 0))+10; con.close()
                    return jsonify(ok=True,xp=xp)

                @app.get("/skills")
                def skill_mastery():
                    u=mod.user()
                    if not u: return redirect("/login")
                    con=mod.db()
                    done_rows=con.execute("SELECT lesson_id FROM progress WHERE user_id=? AND completed=1",(u["id"],)).fetchall()
                    done={int(r["lesson_id"]) for r in done_rows}
                    con.close()
                    rows=[]
                    for idx,c in enumerate(courses()):
                        total=len(c["lessons"])
                        if c["slug"]=="python":
                            complete=sum(1 for i in range(1,total+1) if i in done)
                        else:
                            base=1000+(idx-1)*100
                            complete=sum(1 for i in range(1,total+1) if base+i in done)
                        pct=round(complete/total*100) if total else 0
                        rows.append((c["title"],complete,total,pct,c["slug"]))
                    rows.sort(key=lambda x:(-x[3],x[0].lower()))
                    cards=''.join(f'''<a class="card" href="/course/{html.escape(s)}"><div style="display:flex;justify-content:space-between;gap:10px"><b>{html.escape(t)}</b><span>{p}%</span></div><div class="bar" style="margin-top:13px"><i style="width:{p}%"></i></div><p>{n}/{total} lessons complete</p></a>''' for t,n,total,p,s in rows)
                    body=f'<div class="grid" style="margin-top:28px">{cards}</div>'
                    return layout(f'<section class="section feature-shell"><div class="eyebrow">SKILL MASTERY</div><h1 style="font-size:clamp(42px,7vw,76px)">Your skills.</h1><p style="font-size:18px;max-width:800px">See your progress by technology and identify which learning paths need more practice.</p>{body}</section>',"Skill Mastery")

                @app.get("/adaptive")
                def adaptive():
                    u=mod.user()
                    if not u: return redirect("/login")
                    con=mod.db()
                    done=int(con.execute("SELECT COUNT(*) n FROM progress WHERE user_id=? AND completed=1",(u["id"],)).fetchone()["n"])
                    xp=int((con.execute("SELECT COALESCE(xp,0) xp FROM learner_meta WHERE user_id=?",(u["id"],)).fetchone() or {"xp":0})["xp"])
                    recent=con.execute("SELECT title,href FROM learner_activity WHERE user_id=? ORDER BY seen_at DESC LIMIT 6",(u["id"],)).fetchall()
                    con.close()
                    suggestions=[]
                    if done==0:
                        suggestions.append(("Start with Python fundamentals","Complete your first lesson, then use its challenge before moving on.","/course/python"))
                    elif done<5:
                        suggestions.append(("Build your foundation","Keep the next few lessons focused on core syntax and small exercises.","/course/python"))
                    else:
                        suggestions.append(("Mix learning with building","After a lesson, spend time in the playground or choose a project that uses the same concept.","/playground"))
                    if xp<500:
                        suggestions.append(("Strengthen retrieval","Use Practice Lab and Timed Challenges to turn recognition into recall.","/practice-lab"))
                    else:
                        suggestions.append(("Push difficulty","Try a project or interview session using a topic you recently studied.","/projects"))
                    if recent:
                        suggestions.append(("Continue where you left off",f'Return to {recent[0]["title"]} and finish the next step.',recent[0]["href"]))
                    cards=''.join(f'<a class="card" href="{html.escape(h)}"><div class="eyebrow">RECOMMENDED</div><h2>{html.escape(t)}</h2><p>{html.escape(d)}</p><span class="btn primary">Open →</span></a>' for t,d,h in suggestions)
                    return layout(f'<section class="section feature-shell"><div class="eyebrow">ADAPTIVE LEARNING</div><h1 style="font-size:clamp(42px,7vw,76px)">What to do next.</h1><p style="font-size:18px;max-width:800px">Recommendations adjust to your current progress, activity and practice history.</p><div class="stats"><span>{done} lessons complete</span><span>{xp} XP</span></div><div class="grid" style="margin-top:28px">{cards}</div></section>',"Adaptive Learning")

                old_layout=layout
                def upgraded_layout(content,title="EaseWithPy",description=None):
                    base=old_layout(content,title)
                    # Add direct access without replacing the existing navigation.
                    marker='<a href="/playground">Playground</a>'
                    if marker in base and '/skills' not in base:
                        base=base.replace(marker, marker+'<a href="/skills">Skills</a><a href="/adaptive">For You</a>',1)
                    style='''<style>
.lesson-challenge{margin:28px 0;padding:22px;border:1px solid #353535;border-radius:18px;background:linear-gradient(135deg,#121212,#090909)}
.lesson-challenge h3{margin:7px 0 8px}.challenge-task{padding:15px;border:1px dashed #444;border-radius:12px;background:#080808;color:#ddd}.realworld{margin:28px 0;padding:22px;border-left:3px solid #aaa;border-top:1px solid #292929;border-right:1px solid #292929;border-bottom:1px solid #292929;border-radius:14px;background:#0d0d0d}
.realworld h3{margin:0 0 7px}.challenge-status{margin-top:9px;color:#aaa}
</style>'''
                    base=base.replace('</head>',style+'</head>',1)
                    csrf_token=html.escape(str(mod.csrf()))
                    script = """<script>
if(location.pathname.startsWith("/learn/")){
 const parts=location.pathname.split("/").filter(Boolean);
 const slug=parts.length===2 ? "python" : parts[1];
 const n=parts.length===2 ? Number(parts[1]) : Number(parts[2]);
 if(Number.isFinite(n)){
  fetch("/api/lesson-layer/"+encodeURIComponent(slug)+"/"+n).then(r=>r.ok?r.json():null).then(d=>{
   if(!d)return;
   const main=document.querySelector("main"); if(!main)return;
   const box=document.createElement("div"); box.className="lesson-challenge";
   box.innerHTML='<div class="eyebrow">TRY IT YOURSELF</div><h3>Put this lesson into practice</h3><div class="challenge-task">'+d.challenge+'</div><textarea id="lessonChallengeAttempt" placeholder="Write your attempt, code, commands, or explanation here…"></textarea><div class="actions"><button id="challengeDone" class="btn primary">✓ I attempted it</button><span id="challengeStatus" class="challenge-status"></span></div>';
   const note=document.createElement("div"); note.className="realworld";
   note.innerHTML='<div class="eyebrow">REAL WORLD</div><h3>'+d.context.heading+'</h3><p>'+d.context.text+'</p>';
   const target=main.querySelector(".section"); if(target){target.appendChild(box);target.appendChild(note)}else{main.append(box,note)}
   document.getElementById("challengeDone").onclick=async()=>{
    const b=document.getElementById("challengeDone"),s=document.getElementById("challengeStatus");
    if(!document.getElementById("lessonChallengeAttempt").value.trim()){s.textContent="Write an attempt first.";return}
    try{
     const r=await fetch("/api/lesson-challenge",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({csrf:"__TOKEN__",slug:slug,n:n})});
     s.textContent=r.ok?"Challenge logged · +10 XP":"Log in to save challenge XP.";
     if(r.ok)b.disabled=true;
    }catch(e){s.textContent="Challenge attempted locally."}
   };
  }).catch(()=>{});
 }
}
</script>""".replace("__TOKEN__",csrf_token)
                    base=base.replace('</body>',script+'</body>',1)
                    return base
                mod.layout=upgraded_layout
                app.layout=upgraded_layout
                print("[EaseWithPy] lesson challenges + real-world context + adaptive learning installed")
                return
            except Exception as e:
                print("[EaseWithPy] learning extras retry:",repr(e))
                time.sleep(1)
    threading.Thread(target=boot,daemon=True).start()
