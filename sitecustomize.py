"""LearnPython course extension loaded before the Flask app starts."""
import sys, threading, time

def _install():
    for _ in range(300):
        mod = sys.modules.get("app") or sys.modules.get("__main__")
        app = getattr(mod, "APP", None) if mod else None
        if app is not None and hasattr(mod, "COURSE") and hasattr(mod, "render_lesson_body"):
            try:
                from additional_courses import COURSES
                import html as H
                import secrets
                from flask import abort, jsonify

                def page(body, title="LearnPython"):
                    return mod.layout(body, title)

                def lab(course):
                    slug = course["slug"]
                    starters = {
                        "ai": 'text = "I love this awesome course!"\npositive = ["love", "awesome", "great", "fun", "good"]\nscore = sum(w in text.lower() for w in positive)\nprint("positive" if score else "neutral")',
                        "go": 'package main\n\nimport "fmt"\n\nfunc main() {\n    for i := 1; i <= 5; i++ {\n        fmt.Println("Level", i)\n    }\n}',
                        "typescript": 'type Player = { name: string; score: number };\nconst player: Player = { name: "Rex", score: 100 };\nconsole.log(player.name + ": " + player.score);',
                        "html": '<main>\n  <h1>Hello, web!</h1>\n  <p>Edit this HTML and preview it.</p>\n  <button>Click me</button>\n</main>',
                        "css": '<style>\nbody { font-family: system-ui; padding: 24px; }\n.card { padding: 24px; border: 1px solid #aaa; border-radius: 16px; }\n</style>\n<div class="card"><h2>Style me</h2><p>Change the CSS.</p></div>'
                    }
                    starter=starters[slug]
                    if slug=="html":
                        controls=f'<textarea id="code">{H.escape(starter)}</textarea><div class="actions"><button class="solid" onclick="previewHTML()">▶ Preview</button><button onclick="resetLab()">↻ Reset</button></div><iframe id="preview" title="HTML preview" style="width:100%;height:300px;border:1px solid #292929;border-radius:12px;background:white;margin-top:12px"></iframe>'
                        script='''<script>const original=document.getElementById("code").value;function previewHTML(){document.getElementById("preview").srcdoc=document.getElementById("code").value}function resetLab(){document.getElementById("code").value=original;previewHTML()}document.addEventListener("DOMContentLoaded",previewHTML);</script>'''
                    elif slug=="css":
                        controls=f'<textarea id="code">{H.escape(starter)}</textarea><div class="actions"><button class="solid" onclick="previewCSS()">▶ Preview</button><button onclick="resetLab()">↻ Reset</button></div><iframe id="preview" title="CSS preview" style="width:100%;height:300px;border:1px solid #292929;border-radius:12px;background:white;margin-top:12px"></iframe>'
                        script='''<script>const original=document.getElementById("code").value;function previewCSS(){document.getElementById("preview").srcdoc=document.getElementById("code").value}function resetLab(){document.getElementById("code").value=original;previewCSS()}document.addEventListener("DOMContentLoaded",previewCSS);</script>'''
                    elif slug=="typescript":
                        controls=f'<textarea id="code">{H.escape(starter)}</textarea><div class="actions"><button class="solid" onclick="compileTS()">⚡ Compile TypeScript</button><button onclick="resetLab()">↻ Reset</button></div><div id="out" class="output">The TypeScript compiler checks your code in the browser.</div>'
                        script='''<script src="https://cdn.jsdelivr.net/npm/typescript@5.9.2/lib/typescript.min.js"></script><script>const original=document.getElementById("code").value;function compileTS(){const out=document.getElementById("out");try{const r=ts.transpileModule(document.getElementById("code").value,{compilerOptions:{target:ts.ScriptTarget.ES2020,module:ts.ModuleKind.ES2020},reportDiagnostics:true});const d=(r.diagnostics||[]).map(x=>ts.flattenDiagnosticMessageText(x.messageText,"\\n"));out.textContent=d.length?d.join("\\n"):"✓ TypeScript compiled successfully.\\n\\nJavaScript output:\\n"+r.outputText}catch(e){out.textContent="Compiler error: "+e}}function resetLab(){document.getElementById("code").value=original;document.getElementById("out").textContent="Reset. Try changing a type."}</script>'''
                    elif slug=="ai":
                        controls='<input id="prompt" type="text" value="I love this awesome course" placeholder="Type a message…"><div class="actions"><button class="solid" onclick="classify()">🧠 Classify</button></div><div id="out" class="output">Toy model: simple keyword scoring. This is a learning demo, not a real AI model.</div>'
                        script='''<script>const pos=["love","awesome","great","good","fun","happy","best","win"],neg=["hate","bad","terrible","boring","sad","worst","lose","awful"];function classify(){const t=document.getElementById("prompt").value.toLowerCase(),p=pos.filter(x=>t.includes(x)).length,n=neg.filter(x=>t.includes(x)).length,l=p>n?"positive":n>p?"negative":"neutral";document.getElementById("out").textContent="Toy model result: "+l+"\\npositive score: "+p+"\\nnegative score: "+n+"\\n\\nReal ML learns parameters from data; this demo uses hand-written rules."}</script>'''
                    else:
                        controls=f'<textarea id="code">{H.escape(starter)}</textarea><div class="actions"><button class="solid" onclick="checkGo()">✓ Check Go</button><button onclick="resetLab()">↻ Reset</button></div><div id="out" class="output">Safe structural checker — run real Go locally for compiler feedback.</div>'
                        script='''<script>const original=document.getElementById("code").value;function checkGo(){const c=document.getElementById("code").value,o=document.getElementById("out"),t=[];if(!c.includes("package main"))t.push("Add package main.");if(!c.includes("func main()"))t.push("Add func main().");if((c.match(/{/g)||[]).length!==(c.match(/}/g)||[]).length)t.push("Your braces do not balance.");o.textContent=t.length?t.join("\\n"):"✓ Looks structurally solid! Next: run it with the real Go compiler."}function resetLab(){document.getElementById("code").value=original;document.getElementById("out").textContent="Reset. Make a change and check again."}</script>'''
                    return f'<div class="play"><div class="playtop"><div><div class="eyebrow">CODE LAB · {H.escape(course["tag"])}</div><h2>Build. Test. Tinker.</h2></div><div class="labstats">Browser-safe practice</div></div><p>Edit the starter, test it, break it on purpose, then fix it.</p>{controls}</div>{script}'

                def library():
                    cards="".join(f'<a class="card" href="/learn/{c["slug"]}/1"><div class="eyebrow">{H.escape(c["tag"])} · {len(c["lessons"])} LESSONS</div><h2>{H.escape(c["title"])}</h2><p>{H.escape(c["description"])}</p><span class="pill solid">Start course →</span></a>' for c in COURSES)
                    return page(f'<section class="course"><div class="eyebrow">Course library</div><h1 style="font-size:60px">Learn more.<br><span style="color:var(--accent)">Build more.</span></h1><p>Pick a path, learn the idea, mess with the code, and build something real.</p></section><section class="section"><div class="grid">{cards}</div></section>',"Course Library")

                def lesson(slug,n):
                    c=next((x for x in COURSES if x["slug"]==slug),None)
                    if not c or n<1 or n>len(c["lessons"]): abort(404)
                    item=c["lessons"][n-1]; title=item["title"]; body=item["body"]
                    u=mod.user(); pid=1000+(COURSES.index(c)*100)+n; done=False
                    if u:
                        con=mod.db(); done=bool(con.execute("SELECT completed FROM progress WHERE user_id=? AND lesson_id=?",(u["id"],pid)).fetchone()); con.close()
                    safe=mod.render_lesson_body(f"{title}\n{body}")
                    done_btn=f'<button id="done" class="solid" onclick="completeNew()">{"✓ Lesson complete" if done else "✓ Complete lesson"}</button>' if u else '<a class="pill" href="/login">Log in to save progress</a>'
                    nxt=f'<a class="pill solid" href="/learn/{slug}/{n+1}">Next lesson →</a>' if n<len(c["lessons"]) else ''
                    cap='<section class="finalboss"><div class="eyebrow">FINAL BOSS · CAPSTONE</div><h2>Ship something you understand.</h2><p>Build a small project, test weird inputs, explain your choices, then polish it.</p><div class="bossgrid"><div><strong>01 · BUILD</strong><p>Make the smallest working version.</p></div><div><strong>02 · BREAK</strong><p>Try cases you did not expect.</p></div><div><strong>03 · EXPLAIN</strong><p>Know why your important decisions work.</p></div><div><strong>04 · SHIP</strong><p>Clean it up and show someone.</p></div></div></section>' if n==len(c["lessons"]) else ''
                    js=f'''<script>async function completeNew(){{const r=await fetch("/api/course-progress/{slug}/{n}",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{csrf:"{mod.csrf()}"}})}});if(r.ok){{document.getElementById("done").textContent="✓ Lesson complete";document.getElementById("done").disabled=true;}}}}</script>'''
                    return page(f'<section class="lessonpage"><a class="muted" href="/courses">← All courses</a><div style="margin-top:30px" class="eyebrow">{H.escape(c["title"])}</div><h1 style="font-size:56px">Lesson {n}: {H.escape(title)}</h1><div class="stats"><span>▣ {n}/{len(c["lessons"])}</span><span>⚡ Learn → practice → build</span></div><div class="lessonbody">{safe}</div>{lab(c)}{cap}<div class="actions"><a class="pill" href="/courses">Course library</a>{done_btn}{nxt}</div></section>{js}',f'{title} · {c["title"]}')

                def save_progress(slug,n):
                    c=next((x for x in COURSES if x["slug"]==slug),None)
                    u=mod.user()
                    if not u or not c or n<1 or n>len(c["lessons"]): return jsonify(error="unauthorized"),401
                    data=mod.request.get_json(silent=True) or {}
                    if not secrets.compare_digest(str(data.get("csrf","")),str(mod.session.get("csrf",""))): return jsonify(error="csrf"),400
                    pid=1000+(COURSES.index(c)*100)+n
                    con=mod.db(); con.execute("INSERT INTO progress(user_id,lesson_id,completed) VALUES(?,?,1) ON CONFLICT(user_id,lesson_id) DO UPDATE SET completed=1,updated_at=CURRENT_TIMESTAMP",(u["id"],pid)); con.commit(); con.close()
                    return jsonify(ok=True)

                app.add_url_rule("/learn/<slug>/<int:n>",endpoint="extra_course_lesson",view_func=lesson,methods=["GET"])
                app.add_url_rule("/api/course-progress/<slug>/<int:n>",endpoint="extra_course_progress",view_func=save_progress,methods=["POST"])
                app.view_functions["courses"]=library
                print("[LearnPython] loaded extra courses:",", ".join(c["slug"] for c in COURSES))
                return
            except Exception as e:
                print("[LearnPython] course extension failed:",repr(e))
                return
        time.sleep(0.1)

threading.Thread(target=_install,daemon=True).start()

# Load the modern home/auth UI upgrade after Flask initializes.\nimport ui_upgrade\n