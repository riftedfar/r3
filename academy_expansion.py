"""Academy expansion: practice, roadmaps, cheatsheets, projects, glossary and challenges."""
import html, json, threading, time

def install():
    def boot():
        for _ in range(120):
            mod = __import__("app")
            app = getattr(mod, "APP", None)
            layout = getattr(mod, "layout", None)
            if app is None or layout is None:
                time.sleep(0.25)
                continue
            try:
                from flask import Response

                def card(title, text, href=None, label="Open →"):
                    inside = f"<h3>{html.escape(title)}</h3><p>{html.escape(text)}</p>"
                    if href:
                        inside += f'<span class="btn primary">{html.escape(label)}</span>'
                        return f'<a class="card" href="{html.escape(href)}" style="display:block">{inside}</a>'
                    return f'<div class="card">{inside}</div>'

                def shell(title, eyebrow, intro, body):
                    return layout(
                        f'''<section class="section">
<div class="eyebrow">{html.escape(eyebrow)}</div>
<h1 style="font-size:clamp(42px,7vw,76px);max-width:900px">{html.escape(title)}</h1>
<p style="font-size:18px;max-width:800px">{html.escape(intro)}</p>
{body}</section>''',
                        title,
                        intro
                    )

                @app.route("/practice")
                def academy_practice():
                    labs = [
                        ("Predict the output", "Read a short Python snippet, predict the result, then run it in your head before checking.", "/learn/7"),
                        ("Fix the bug", "Find the smallest change that makes a broken program work. Debugging is a skill, not a punishment.", "/learn/18"),
                        ("Explain the code", "Take a working snippet and explain each line in plain English. If you cannot explain it, keep digging.", "/learn/25"),
                        ("Refactor it", "Take repetitive code and make it clearer without changing what it does.", "/learn/32"),
                        ("Build from a spec", "Start from requirements and turn them into a small, testable implementation.", "/courses/python"),
                        ("Security review", "Look for unsafe input handling, leaked secrets, weak authorization and dangerous assumptions.", "/learn/95"),
                    ]
                    body='<div class="grid" style="margin-top:28px">'+''.join(card(*x) for x in labs)+'</div>'
                    body += '''<div class="banner" style="margin-top:24px"><div><div class="eyebrow">RULE</div><h2>Do the hard part yourself.</h2><p style="margin:0">Use AI as a tutor, reviewer or pair programmer. Do not paste a solution you cannot explain.</p></div><a class="btn primary" href="/courses">Pick a course →</a></div>'''
                    return shell("Practice Center", "HANDS-ON", "A collection of ways to turn passive reading into actual programming skill.", body)

                @app.route("/roadmap")
                def academy_roadmap():
                    stages = [
                        ("01","Computer basics","Files, folders, terminals, editors, processes and how programs actually run."),
                        ("02","Programming core","Variables, types, conditions, loops, functions, collections and debugging."),
                        ("03","Python builder","Modules, OOP, exceptions, files, testing, databases, APIs and packaging."),
                        ("04","Web & APIs","HTML, CSS, JavaScript, HTTP, JSON, authentication and backend architecture."),
                        ("05","Data & AI","SQL, data modeling, statistics basics, ML concepts, embeddings and LLM systems."),
                        ("06","Ship projects","Git, testing, deployment, observability, security and documentation."),
                    ]
                    steps=''.join(f'<div class="step"><span class="eyebrow">{n}</span><b>{html.escape(t)}</b><p>{html.escape(d)}</p></div>' for n,t,d in stages)
                    body=f'<div class="path" style="margin-top:28px">{steps}</div>'
                    body += '<h2 style="margin-top:55px">Choose a destination</h2><div class="grid">'+''.join(card(*x) for x in [
                        ("Python Developer","Build scripts, automation, APIs, CLIs and backend applications.","/courses/python"),
                        ("Web Developer","Learn HTML, CSS, JavaScript and the architecture around web apps.","/courses/html"),
                        ("AI Builder","Understand AI systems before jumping into frameworks and agents.","/courses/ai"),
                        ("Data Builder","Learn SQL and the data concepts behind useful applications.","/courses/sql"),
                    ])+'</div>'
                    return shell("The Developer Roadmap", "YOUR PATH", "A practical sequence from first programs to projects you can actually ship.", body)

                @app.route("/cheatsheets")
                def academy_cheatsheets():
                    sheets = [
                        ("Python", "print(), variables, f-strings, if/elif/else, for, while, def, return, list, dict, set, tuple, try/except, import."),
                        ("Git", "git init · git status · git add · git commit · git log · git branch · git switch · git merge · git pull · git push."),
                        ("SQL", "SELECT · WHERE · ORDER BY · GROUP BY · HAVING · JOIN · INSERT · UPDATE · DELETE · CREATE TABLE · indexes."),
                        ("HTML", "doctype · html · head · body · header · nav · main · section · article · form · label · input · button · footer."),
                        ("CSS", "display · box model · margin · padding · flex · grid · gap · position · media queries · variables · transition."),
                        ("JavaScript", "const · let · function · array · object · map · filter · reduce · async · await · fetch · DOM events."),
                        ("TypeScript", "type · interface · union · narrowing · generic · unknown · never · Promise<T> · async/await."),
                        ("Go", "package · func · var · := · if · switch · for · slice · map · struct · interface · error · goroutine."),
                    ]
                    blocks=''.join(f'<div class="card"><div class="eyebrow">{html.escape(t)}</div><div class="snippet">{html.escape(s)}</div><button class="btn" onclick="navigator.clipboard.writeText(this.previousElementSibling.textContent);this.textContent=&quot;Copied ✓&quot;">Copy</button></div>' for t,s in sheets)
                    return shell("Developer Cheatsheets", "QUICK REFERENCE", "Compact reminders for syntax and concepts. Learn the idea first; use the sheet when your memory blanks.", '<div class="grid" style="margin-top:28px">'+blocks+'</div>')

                @app.route("/projects")
                def academy_projects():
                    projects = [
                        ("01","CLI Task Manager","Build add/list/complete/delete commands, persist data, validate input and write tests.",[("Python","python"),("Bash / Linux","bash-linux")]),
                        ("02","Quiz Engine","Store questions, randomize a quiz, score answers and show a useful review.",[("Python","python")]),
                        ("03","Course Tracker","Track users, courses and completed lessons in a relational database.",[("Python","python"),("PostgreSQL","postgresql"),("MySQL","mysql")]),
                        ("04","REST API","Create CRUD endpoints with validation, authentication, authorization and structured errors.",[("FastAPI","fastapi"),("REST API Engineering","rest-api"),("Python","python")]),
                        ("05","Search Engine","Crawl a controlled dataset, normalize documents, build an inverted index and rank results.",[("Python","python"),("Data Structures & Algorithms","dsa"),("Algorithms","algorithms")]),
                        ("06","AI Study Helper","Build retrieval, prompting, citations and a clear boundary around generated answers.",[("AI","ai"),("Python","python")]),
                        ("07","File Organizer","Classify files by extension, add dry-run mode, logs and safe collision handling.",[("Python","python"),("Bash / Linux","bash-linux")]),
                        ("08","Portfolio Site","Ship a responsive site with semantic HTML, CSS, JavaScript and SEO basics.",[("HTML","html"),("CSS","css"),("JavaScript","javascript")]),
                    ]
                    def project_links(skills):
                        return ''.join(f'<a class="btn" href="/course/{html.escape(slug)}">{html.escape(name)} →</a>' for name,slug in skills)
                    cards=''.join(f'<div class="card"><span class="eyebrow">{n}</span><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p><div class="eyebrow" style="margin-top:14px">SKILLS USED</div><div class="actions">{project_links(skills)}</div></div>' for n,t,d,skills in projects)
                    body='<div class="grid" style="margin-top:28px">'+cards+'</div><div class="notice" style="margin-top:24px">Project rule: start with a tiny vertical slice. Make it work, test it, then expand.</div>'
                    return shell("Project Forge", "BUILD MODE", "Projects arranged from small practical builds to systems that force you to combine multiple engineering skills.", body)

                @app.route("/glossary")
                def academy_glossary():
                    terms = [
                        ("API","A defined interface through which software components communicate."),
                        ("Algorithm","A repeatable procedure for solving a problem or transforming input."),
                        ("Authentication","Verifying who a user or system is."),
                        ("Authorization","Deciding what an authenticated identity is allowed to do."),
                        ("Backend","Server-side software responsible for data, rules, APIs and other application logic."),
                        ("Bug","A defect that causes software to behave differently from its intended behavior."),
                        ("Cache","Stored data used to avoid repeating expensive work."),
                        ("CI/CD","Automated processes that build, test and/or deploy software."),
                        ("Database","A system for storing and querying structured or semi-structured information."),
                        ("Dependency","External software your project relies on."),
                        ("Endpoint","A network-accessible operation exposed by an API."),
                        ("Exception","A runtime event representing an error or unusual condition."),
                        ("Framework","A reusable application structure that provides conventions and infrastructure."),
                        ("Git","A distributed version-control system for tracking source changes."),
                        ("HTTP","A protocol used for communication between clients and web servers."),
                        ("JSON","A text data format commonly used for structured API payloads."),
                        ("Latency","The time between an operation being requested and its result becoming available."),
                        ("Library","Reusable code that an application can call."),
                        ("Module","A unit of code that can be imported and reused."),
                        ("Query","A request for information or an operation against a data system."),
                        ("Runtime","The environment in which a program executes."),
                        ("Schema","A defined structure for data, often describing fields, types and relationships."),
                        ("SQL","A language for querying and manipulating relational databases."),
                        ("Token","A unit of text or data processed by a model or security system, depending on context."),
                        ("Version Control","A system for tracking changes and collaborating on code."),
                    ]
                    terms.sort()
                    rows=''.join(f'<div class="card"><h3 style="margin-top:0">{html.escape(t)}</h3><p>{html.escape(d)}</p></div>' for t,d in terms)
                    return shell("Developer Glossary", "REFERENCE", "Plain-English definitions for terms you will encounter while learning software engineering.", '<input id="termsearch" class="search" placeholder="⌕ Search a term…"><div id="terms" class="grid">'+rows+'</div><script>const q=document.getElementById("termsearch");q.oninput=()=>{const x=q.value.toLowerCase();document.querySelectorAll("#terms .card").forEach(c=>c.style.display=c.textContent.toLowerCase().includes(x)?"block":"none")}</script>')

                @app.route("/challenges")
                def academy_challenges():
                    qs = [
                        ("Python","What does list(range(3)) produce?",["[0, 1, 2]","[1, 2, 3]","[0, 1, 2, 3]"],0),
                        ("Python","Which keyword defines a function?",["func","def","function"],1),
                        ("Web","Which element is intended for the main unique content of a page?",["<main>","<div>","<content>"],0),
                        ("CSS","Which layout system is designed for two-dimensional rows and columns?",["Flexbox","Grid","Float"],1),
                        ("Git","Which command creates a commit from staged changes?",["git save","git commit","git push"],1),
                        ("SQL","Which clause filters rows before grouping?",["WHERE","HAVING","ORDER"],0),
                        ("AI","What is an embedding commonly used to represent?",["Meaning/features as vectors","A password","A CSS rule"],0),
                        ("Security","Where should authorization be enforced?",["Only in the UI","On the server/resource boundary","In a button label"],1),
                    ]
                    data=json.dumps([{"cat":c,"q":q,"opts":o,"a":a} for c,q,o,a in qs],separators=(",",":"))
                    body=f'''<div class="card" style="margin-top:28px"><div class="stats"><span id="score">0 / {len(qs)}</span><span id="progress">Question 1</span></div><div id="quiz"></div><div class="actions"><button class="btn" id="next">Next →</button><button class="btn" id="reset">Reset</button></div></div>
<script>
const questions={data};let i=0,score=0,locked=false;
const qel=document.getElementById("quiz"),scoreEl=document.getElementById("score"),prog=document.getElementById("progress"),next=document.getElementById("next");
function draw(){{locked=false;const q=questions[i];prog.textContent="Question "+(i+1)+" of "+questions.length;qel.innerHTML='<div class="eyebrow">'+q.cat+'</div><h2>'+q.q+'</h2>'+q.opts.map((x,n)=>'<button class="btn option" data-n="'+n+'" style="display:block;width:100%;text-align:left;margin:8px 0">'+x+'</button>').join("");document.querySelectorAll(".option").forEach(b=>b.onclick=()=>{{if(locked)return;locked=true;const ok=+b.dataset.n===q.a;if(ok)score++;b.textContent=ok?"✓ "+b.textContent:"✕ "+b.textContent;scoreEl.textContent=score+" / "+(i+1);}})}}
next.onclick=()=>{{if(i<questions.length-1){{i++;draw()}}else{{qel.innerHTML='<h2>Challenge complete.</h2><p>You scored '+score+' / '+questions.length+'. Review the topics you missed, then try again.</p>';prog.textContent="Finished";next.disabled=true}}}};
document.getElementById("reset").onclick=()=>{{i=0;score=0;next.disabled=false;scoreEl.textContent="0 / {len(qs)}";draw()}};
draw();
</script>'''
                    return shell("Challenge Arena", "CHECK YOURSELF", "A quick mixed-topic quiz. The goal is retrieval practice, not a leaderboard.", body)

                @app.route("/api/academy/search")
                def academy_search():
                    q = (mod.request.args.get("q") or "").strip().lower()
                    if not q:
                        return mod.jsonify(results=[])
                    # Keep this endpoint deliberately small and public: it exposes course titles only.
                    from additional_courses import COURSES
                    courses = [{"title":"Python","slug":"python","href":"/courses/python"}] + [{"title":c["title"],"slug":c["slug"],"href":"/courses/"+c["slug"]} for c in COURSES]
                    return mod.jsonify(results=[c for c in courses if q in c["title"].lower() or q in c["slug"].lower()][:12])

                @app.route("/academy")
                def academy_hub():
                    body='<div class="grid" style="margin-top:28px">'+''.join(card(*x) for x in [
                        ("Practice Center","Turn lessons into active recall, debugging and build sessions.","/practice"),
                        ("Developer Roadmap","Follow a practical path from fundamentals to shipped projects.","/roadmap"),
                        ("Project Forge","Pick a project and learn the skills required to finish it.","/projects"),
                        ("Cheatsheets","Keep compact syntax reminders nearby while you work.","/cheatsheets"),
                        ("Glossary","Look up software terms in plain English.","/glossary"),
                        ("Challenge Arena","Test what you actually remember with short quizzes.","/challenges"),
                    ])+'</div><div class="banner" style="margin-top:25px"><div><div class="eyebrow">NEXT MOVE</div><h2>Stop collecting tutorials.</h2><p style="margin:0">Pick one course, one project, and one thing to ship.</p></div><a class="btn primary" href="/courses">Start learning →</a></div>'
                    return shell("Academy Hub", "LEARNPYTHON", "The extra layer around the course library: practice, projects, references and challenges.", body)

                return
            except Exception as e:
                print("[LearnPython] academy expansion retry:", repr(e))
                time.sleep(1)
    threading.Thread(target=boot, daemon=True).start()
