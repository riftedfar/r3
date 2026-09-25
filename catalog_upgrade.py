import html
from flask import request, redirect, url_for, jsonify, abort

from app import APP, db, user, csrf, require_csrf, layout

COURSES = {
    "html-css": {
        "title":"HTML & CSS: Build for the Web","level":"Beginner","category":"Web",
        "description":"Build real pages from semantic HTML to responsive layouts, forms, cards and polished UI.",
        "lessons":[
            ("HTML mental model","Learn how elements, attributes and document structure fit together."),
            ("Semantic HTML","Build pages with headings, sections, nav, main, article and footer."),
            ("Links, images & media","Connect pages and use images and media accessibly."),
            ("Forms that make sense","Create labels, inputs, buttons and useful form structure."),
            ("CSS selectors","Target elements cleanly with classes, attributes and combinators."),
            ("Box model","Master margin, padding, border, width and sizing."),
            ("Flexbox","Build responsive rows, columns, navbars and card layouts."),
            ("CSS Grid","Create two-dimensional layouts without fighting your CSS."),
            ("Responsive design","Make your site work on phones, tablets and desktops."),
            ("Transitions & polish","Add motion, states, shadows and visual hierarchy."),
            ("Build a landing page","Combine the skills into a responsive landing page."),
            ("Ship your portfolio page","Finish and polish a page you can actually publish.")
        ]
    },
    "javascript": {
        "title":"JavaScript Foundations","level":"Beginner","category":"Programming",
        "description":"Go from variables and functions to DOM interaction, events, APIs and browser apps.",
        "lessons":[
            ("JavaScript in the browser","Understand scripts, the console and how JS runs on a page."),
            ("Variables & values","Use let, const, strings, numbers, booleans and null."),
            ("Conditions","Make programs choose what happens next."),
            ("Loops","Repeat work safely with for, while and array methods."),
            ("Functions","Write reusable logic with parameters and return values."),
            ("Arrays & objects","Model real data with the structures you use constantly."),
            ("DOM basics","Select and change elements on a live page."),
            ("Events","Make buttons, forms and keyboard interactions respond."),
            ("Local storage","Persist simple app state in the browser."),
            ("Fetch & APIs","Request JSON data and handle async results."),
            ("Build an interactive app","Combine DOM, state, events and APIs."),
            ("Ship it","Debug, polish and deploy your JavaScript project.")
        ]
    },
    "sql": {
        "title":"SQL & Databases","level":"Beginner","category":"Data",
        "description":"Learn how applications store, query, filter, join and safely change structured data.",
        "lessons":[
            ("Database thinking","Tables, rows, columns, keys and relationships."),
            ("SELECT","Read exactly the records you need."),
            ("WHERE & filtering","Turn raw tables into useful answers."),
            ("ORDER BY & LIMIT","Sort results and control result size."),
            ("INSERT, UPDATE, DELETE","Change data deliberately and safely."),
            ("Aggregates","Use COUNT, SUM, AVG, MIN and MAX."),
            ("GROUP BY","Turn rows into useful summaries."),
            ("JOINs","Combine related tables without duplicating your data."),
            ("Constraints & indexes","Protect data quality and speed up common queries."),
            ("Build a mini schema","Design a small database for a real app.")
        ]
    },
    "git-github": {
        "title":"Git & GitHub","level":"Beginner","category":"Tools",
        "description":"Learn version control the way developers actually use it: branches, commits, remotes and pull requests.",
        "lessons":[
            ("Why Git exists","Understand snapshots, history and why version control matters."),
            ("Your first repository","Initialize Git and inspect the working tree."),
            ("Commits","Make small, useful snapshots with meaningful messages."),
            ("Branches","Experiment without wrecking your main line."),
            ("Merging","Bring completed work back together."),
            ("Remote repositories","Push and pull code with GitHub."),
            ("Pull requests","Review changes before they become part of the project."),
            ("Undoing mistakes","Recover from bad edits, commits and staging decisions."),
            (".gitignore & secrets","Keep generated files and credentials out of Git."),
            ("Team workflow","Use a clean branch → PR → review → merge workflow.")
        ]
    },
    "ai-ml": {
        "title":"AI & Machine Learning Foundations","level":"Intermediate","category":"AI",
        "description":"Understand datasets, models, training, evaluation, embeddings and practical AI systems.",
        "lessons":[
            ("AI vs ML vs deep learning","Separate the terms and understand what each actually means."),
            ("Datasets & features","See how useful training data is represented."),
            ("Training & inference","Understand what a model learns and what prediction means."),
            ("Classification","Build intuition for predicting categories."),
            ("Regression","Predict continuous values and measure error."),
            ("Overfitting","Learn why memorizing training data fails."),
            ("Evaluation","Use train/test splits and meaningful metrics."),
            ("Neural network intuition","Understand layers, weights and activations without the math wall."),
            ("Embeddings","Represent text and other data as useful vectors."),
            ("LLM fundamentals","Understand tokens, context, prompts and generation."),
            ("Build an AI feature","Design a small AI-powered application."),
            ("Responsible shipping","Handle privacy, validation, cost and failure modes.")
        ]
    }
}

def _init_catalog_db():
    con=db()
    con.execute("""CREATE TABLE IF NOT EXISTS course_progress(
        user_id INTEGER NOT NULL, course_slug TEXT NOT NULL, lesson_id INTEGER NOT NULL,
        completed INTEGER DEFAULT 0, updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(user_id,course_slug,lesson_id),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")
    con.commit(); con.close()

_init_catalog_db()

def _progress(slug):
    u=user()
    if not u: return set()
    con=db()
    rows=con.execute("SELECT lesson_id FROM course_progress WHERE user_id=? AND course_slug=? AND completed=1",(u["id"],slug)).fetchall()
    con.close()
    return {int(r["lesson_id"]) for r in rows}

def catalog():
    q=request.args.get("q","").strip().lower()
    cat=request.args.get("category","All")
    cards=[]
    all_courses=[("python","The Ultimate Python Course","Programming","Intermediate",47,"The complete Python path with browser code labs, projects and progress tracking.")]
    for slug,c in COURSES.items():
        all_courses.append((slug,c["title"],c["category"],c["level"],len(c["lessons"]),c["description"]))
    for slug,title,category,level,count,desc in all_courses:
        if cat!="All" and category!=cat: continue
        hay=(title+" "+category+" "+level+" "+desc).lower()
        if q and q not in hay: continue
        href="/courses" if slug=="python" else f"/courses/{slug}"
        cards.append(f'''<a class="card coursecard" href="{href}">
          <div class="courseicon">{html.escape(category[:1])}</div>
          <div class="eyebrow">{html.escape(category)} · {html.escape(level)}</div>
          <h2>{html.escape(title)}</h2><p>{html.escape(desc)}</p>
          <div class="coursemeta"><span>{count} lessons</span><span>Interactive</span><span>Projects</span></div>
          <strong>Start learning →</strong>
        </a>''')
    cats=["All","Programming","Web","Data","AI","Tools"]
    filters="".join(f'<a class="filter {"active" if cat==x else ""}" href="/courses?category={x}">{x}</a>' for x in cats)
    body=f'''<section class="cataloghero"><div class="eyebrow">THE LEARNING LIBRARY</div>
    <h1>Pick a skill.<br><span>Build something.</span></h1>
    <p>Not a pile of videos. Short lessons, browser labs, missions, projects and progress that follows you.</p>
    <form class="catalogsearch"><input name="q" value="{html.escape(request.args.get("q",""))}" placeholder="Search courses, topics, skills…"><button class="solid">Search</button></form>
    </section>
    <section class="catalog"><div class="filters">{filters}</div>
    <div class="cataloggrid">{"".join(cards) or '<div class="card"><h2>No courses found</h2><p>Try another search or category.</p></div>'}</div></section>'''
    return layout(body,"Course Library")

APP.view_functions["courses"]=catalog

def course_overview(slug):
    if slug not in COURSES: abort(404)
    c=COURSES[slug]; done=_progress(slug); total=len(c["lessons"]); pct=round(len(done)/total*100)
    lessons="".join(f'''<a class="lesson" href="/learn/{slug}/{i}">
      <span><span class="eyebrow">Lesson {i:02d}</span><br><strong>{html.escape(t)}</strong><br><small>{html.escape(d)}</small></span>
      <span class="check">{"✓" if i in done else "→"}</span></a>''' for i,(t,d) in enumerate(c["lessons"],1))
    body=f'''<section class="courseoverview"><a class="muted" href="/courses">← Course library</a>
    <div class="eyebrow" style="margin-top:35px">{html.escape(c["category"])} · {html.escape(c["level"])}</div>
    <h1>{html.escape(c["title"])}</h1><p class="lead">{html.escape(c["description"])}</p>
    <div class="progresscard"><div><strong>{len(done)}/{total} complete</strong><span>{pct}%</span></div><div class="bar"><i style="width:{pct}%"></i></div></div>
    <div class="lessonlist">{lessons}</div></section>'''
    return layout(body,c["title"])

@APP.get("/courses/<slug>")
def extra_course(slug): return course_overview(slug)

@APP.get("/learn/<slug>/<int:n>")
def extra_lesson(slug,n):
    if slug not in COURSES: abort(404)
    c=COURSES[slug]
    if n<1 or n>len(c["lessons"]): abort(404)
    title,desc=c["lessons"][n-1]; u=user(); done=n in _progress(slug)
    prev=f'/learn/{slug}/{n-1}' if n>1 else f'/courses/{slug}'
    nxt=f'/learn/{slug}/{n+1}' if n<len(c["lessons"]) else f'/courses/{slug}'
    if slug=="html-css":
        starter='''<div class="card">
  <h1>Build something.</h1>
  <p>Change this HTML and CSS, then refresh the preview.</p>
</div>

<style>
.card { padding: 24px; border-radius: 18px; font-family: system-ui; }
.card h1 { margin: 0 0 8px; }
</style>'''
        lab=f'''<div class="play"><div class="eyebrow">LIVE HTML/CSS LAB</div><textarea id="editor">{html.escape(starter)}</textarea><iframe id="preview" sandbox="allow-scripts"></iframe>
        <script>const e=document.getElementById("editor"),p=document.getElementById("preview");function preview(){{p.srcdoc=e.value}}e.addEventListener("input",preview);preview();</script></div>'''
    elif slug=="javascript":
        starter='''const name = "Learner";
document.querySelector("#output").textContent = "Hello, " + name + "!";'''
        lab=f'''<div class="play"><div class="eyebrow">JAVASCRIPT LAB</div><textarea id="editor">{html.escape(starter)}</textarea><button class="solid" onclick="runJS()">▶ Run JavaScript</button><div id="output" class="output">Output appears here.</div><script>function runJS(){{const out=document.getElementById("output");try{{const el=document.createElement("div");const fn=new Function("document","console",document.getElementById("editor").value);fn({{querySelector:()=>out}},console);}}catch(e){{out.textContent=e}}}}</script></div>'''
    else:
        starter=f"// {title}\n// Write your own answer or experiment here."
        lab=f'''<div class="play"><div class="eyebrow">PRACTICE LAB</div><p>Turn the lesson into a tiny experiment. Write notes, a query, a command sequence or pseudocode here.</p><textarea>{html.escape(starter)}</textarea></div>'''
    complete=f'''<form method="post" action="/api/course-progress/{slug}/{n}" class="actions"><input type="hidden" name="csrf" value="{csrf()}"><button class="solid" type="submit">{"✓ Completed" if done else "✓ Mark lesson complete"}</button></form>''' if u else '<a class="pill solid" href="/login">Log in to save progress</a>'
    body=f'''<section class="lessonpage"><a class="muted" href="/courses/{slug}">← {html.escape(c["title"])}</a>
    <div class="eyebrow" style="margin-top:30px">LESSON {n:02d} · {html.escape(c["category"])}</div><h1 style="font-size:56px">{html.escape(title)}</h1>
    <div class="lessonbody"><h3 class="lessonsection">What you will learn</h3><p>{html.escape(desc)}</p>
    <h3 class="lessonsection">Understand it</h3><p>Start with the idea, then immediately change something yourself. The goal is to make the concept usable, not just recognizable.</p>
    <div class="funbreak"><span class="eyebrow">MISSION</span><strong>Make one small change before moving on.</strong><p>Predict what will happen, try it, then explain the result in your own words.</p></div></div>
    {lab}{complete}<div class="actions"><a class="pill" href="{prev}">← Previous</a><a class="pill solid" href="{nxt}">Next →</a></div></section>'''
    return layout(body,title)

@APP.post("/api/course-progress/<slug>/<int:n>")
def extra_progress(slug,n):
    u=user()
    if not u or slug not in COURSES or n<1 or n>len(COURSES[slug]["lessons"]): return jsonify(error="unauthorized"),401
    require_csrf()
    con=db()
    con.execute("""INSERT INTO course_progress(user_id,course_slug,lesson_id,completed)
                   VALUES(?,?,?,1)
                   ON CONFLICT(user_id,course_slug,lesson_id) DO UPDATE SET completed=1,updated_at=CURRENT_TIMESTAMP""",(u["id"],slug,n))
    con.commit(); con.close()
    return redirect(request.referrer or f"/learn/{slug}/{n}")

# Replace the old dashboard with a cross-course learning dashboard.
def dashboard_v2():
    u=user()
    if not u: return redirect("/login")
    rows=[]
    for slug,c in [("python",{"title":"The Ultimate Python Course","total":47})]+[(s,{"title":x["title"],"total":len(x["lessons"])}) for s,x in COURSES.items()]:
        if slug=="python":
            con=db(); count=con.execute("SELECT COUNT(*) FROM progress WHERE user_id=? AND completed=1",(u["id"],)).fetchone()[0]; con.close()
        else: count=len(_progress(slug))
        pct=round(count/c["total"]*100)
        rows.append(f'''<a class="card" href="/courses/{slug if slug!="python" else ""}"><div class="eyebrow">{html.escape(c["title"])}</div><h2>{count}/{c["total"]}</h2><div class="bar"><i style="width:{pct}%"></i></div><p>{pct}% complete</p></a>''')
    return layout(f'<section class="course"><div class="eyebrow">YOUR LEARNING</div><h1 style="font-size:60px">Keep building, {html.escape(str(u["name"]))}.</h1><div class="grid">{"".join(rows)}</div></section>',"Dashboard")
APP.view_functions["dashboard"]=dashboard_v2
