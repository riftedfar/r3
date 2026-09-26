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

def from catalog_expansion import apply_expansion
COURSES = apply_expansion(COURSES)

_init_catalog_db():
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
    all_courses=[("python","The Ultimate Python Course","Programming","Intermediate",len(COURSE),"The complete Python path with browser code labs, projects and progress tracking.")]
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
    cats=["All","Programming","Web","Data","AI","Tools","Security"]
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
    for slug,c in [("python",{"title":"The Ultimate Python Course","total":len(COURSE)})]+[(s,{"title":x["title"],"total":len(x["lessons"])}) for s,x in COURSES.items()]:
        if slug=="python":
            con=db(); count=con.execute("SELECT COUNT(*) FROM progress WHERE user_id=? AND completed=1",(u["id"],)).fetchone()[0]; con.close()
        else: count=len(_progress(slug))
        pct=round(count/c["total"]*100)
        rows.append(f'''<a class="card" href="/courses/{slug if slug!="python" else ""}"><div class="eyebrow">{html.escape(c["title"])}</div><h2>{count}/{c["total"]}</h2><div class="bar"><i style="width:{pct}%"></i></div><p>{pct}% complete</p></a>''')
    return layout(f'<section class="course"><div class="eyebrow">YOUR LEARNING</div><h1 style="font-size:60px">Keep building, {html.escape(str(u["name"]))}.</h1><div class="grid">{"".join(rows)}</div></section>',"Dashboard")
APP.view_functions["dashboard"]=dashboard_v2

def home_v2():
    cards=[]
    for slug,x in list(COURSES.items())[:5]:
        cards.append(f'<a class="card" href="/courses/{slug}"><div class="eyebrow">{html.escape(x["category"])} · {html.escape(x["level"])}</div><h2>{html.escape(x["title"])}</h2><p>{html.escape(x["description"])}</p><strong>{len(x["lessons"])} lessons →</strong></a>')
    return layout(f'''<section class="hero"><div><div class="eyebrow">INTERACTIVE LEARNING PLATFORM</div><h1>Learn.<br><span>Build. Ship.</span></h1><p>Choose a skill, learn it in short lessons, practice immediately, and build projects that prove you can actually use it.</p><div class="actions"><a class="pill solid" href="/courses">Explore all courses</a><a class="pill" href="/register">Create free account</a></div></div><div class="terminal"><div class="dots">● ● ●</div><div class="code" style="margin-top:20px">learn("HTML")
practice()
build("your idea")
ship()

→ skill unlocked</div></div></section>
<section class="section"><div class="eyebrow">COURSE LIBRARY</div><h2>Start with a path.</h2><div class="grid">{"".join(cards)}</div></section>
<section class="section"><div class="card"><div class="eyebrow">WHY THIS FEELS DIFFERENT</div><h2>Learn by doing.</h2><p>Interactive browser labs, missions, progress tracking, searchable courses and project-focused lessons — all in one place.</p></div></section>''',"Learn · Build · Ship")
APP.view_functions["home"]=home_v2
# Expanded learning tracks. These append to the original catalog without
# changing the existing course routing or interactive labs.
_EXTRA_LESSONS = {
"html-css":[
("Accessibility","Use semantic structure, labels, focus states, alt text, contrast, and keyboard navigation so your UI works for more people."),
("Typography & spacing","Choose readable type scales, line heights, spacing systems, and consistent visual hierarchy."),
("Positioning","Understand static, relative, absolute, fixed, and sticky positioning and when each is appropriate."),
("CSS variables","Create reusable design tokens for colors, spacing, radii, and typography."),
("Pseudo classes","Use :hover, :focus, :checked, :disabled, :nth-child and related states cleanly."),
("Pseudo elements","Create decorative UI with ::before and ::after without adding unnecessary markup."),
("Forms & validation UI","Style usable form controls, error states, help text, and success states."),
("Cards & component patterns","Build reusable visual patterns instead of one-off CSS for every section."),
("Animations","Use keyframes, transitions, reduced-motion preferences, and purposeful movement."),
("Performance basics","Keep images, fonts, CSS, and layout work efficient as pages grow."),
("Debugging CSS","Use browser developer tools, computed styles, box-model inspection, and responsive emulation."),
("Multi-page site","Connect multiple semantic pages with shared navigation and consistent components.")
],
"javascript":[
("Modern syntax","Use destructuring, spread, optional chaining, nullish coalescing, and template literals."),
("Scope & closures","Understand lexical scope, closures, and why callbacks can remember values."),
("Array methods","Use map, filter, reduce, find, some, every, and sort for data transformations."),
("Modules","Split JavaScript into modules with explicit imports and exports."),
("Promises","Understand pending, fulfilled, rejected, and promise chaining."),
("Async/await","Write readable asynchronous code with try/catch and predictable control flow."),
("Error handling","Design useful errors and handle failures at the right boundary."),
("Fetch deeply","Handle status codes, JSON parsing, timeouts, and API failures."),
("State management","Separate application state from rendering and user events."),
("DOM architecture","Build small components without turning one click handler into the whole app."),
("Forms","Validate input, show errors, and prevent duplicate submissions."),
("Web storage","Use localStorage and sessionStorage deliberately and safely."),
("Web APIs","Explore URL, Clipboard, History, and other browser APIs."),
("Security in browser apps","Avoid XSS, unsafe HTML insertion, leaked secrets, and trusting client input."),
("Testing JavaScript","Test pure functions and important UI behavior."),
("Project architecture","Organize a growing browser app into modules, state, views, and services.")
],
"sql":[
("Primary & foreign keys","Model identity and relationships with stable keys."),
("Normalization","Reduce duplication while keeping schemas practical."),
("NULL","Understand missing values and three-valued logic."),
("Subqueries","Use nested queries when they make a problem clearer."),
("CTEs","Break complex SQL into named query stages."),
("CASE","Create conditional values directly in queries."),
("Window functions","Rank, compare, and aggregate rows without collapsing them."),
("Transactions","Group related changes so database state stays consistent."),
("ACID","Understand atomicity, consistency, isolation, and durability."),
("Indexes","Choose indexes from actual query patterns instead of indexing everything."),
("Query plans","Read execution plans and identify expensive operations."),
("Pagination","Design stable LIMIT/OFFSET and cursor-based pagination."),
("Views","Create reusable query interfaces for common reporting logic."),
("Security","Use parameterized queries and least-privilege database access."),
("Backups & migrations","Plan schema changes and recovery before production needs them."),
("Database project","Design a complete schema and query layer for a small application.")
],
"git-github":[
("Git internals","Understand commits, trees, blobs, refs, and why Git can move branches cheaply."),
("Staging area","Use the index deliberately instead of committing every working-tree change."),
("Interactive staging","Stage selected hunks to create focused commits."),
("Rebase","Understand when and why to replay commits onto a new base."),
("Cherry-pick","Move a specific commit between lines of development."),
("Stash","Temporarily shelve work without creating a permanent commit."),
("Bisect","Find the commit that introduced a regression efficiently."),
("Tags & releases","Mark stable versions and publish useful release notes."),
("GitHub Actions","Automate tests, linting, and deployment from repository events."),
("Branch protection","Use reviews and required checks to protect important branches."),
("Secrets","Store deployment credentials in GitHub secrets instead of source code."),
("Code review","Review behavior, edge cases, security, and maintainability rather than formatting alone."),
("Issue tracking","Turn bugs and feature ideas into actionable issues."),
("Open-source workflow","Understand forks, pull requests, licenses, and contribution guides."),
("Monorepos","Organize multiple related applications and packages in one repository."),
("Recovery lab","Practice restoring deleted work with reflog and safe Git commands.")
],
"ai-ml":[
("Linear models","Build intuition for features, weights, predictions, and loss."),
("Decision trees","Understand recursive splits and interpretable rules."),
("Clustering","Group unlabeled examples using similarity."),
("Feature engineering","Turn raw inputs into useful model features."),
("Data leakage","Learn how accidental future information can make evaluation meaningless."),
("Cross-validation","Estimate model performance more reliably."),
("Precision & recall","Choose metrics based on the consequences of false positives and negatives."),
("Confusion matrices","Inspect classification errors instead of staring at one accuracy number."),
("Model pipelines","Keep preprocessing and modeling steps reproducible."),
("Embeddings in practice","Use vector similarity for retrieval and recommendations."),
("Retrieval augmented generation","Combine document retrieval with generation while tracking source context."),
("Prompt evaluation","Build test cases for prompts and compare outputs systematically."),
("AI application architecture","Separate UI, model calls, retrieval, validation, and persistence."),
("AI security","Consider prompt injection, data leakage, unsafe tools, and permission boundaries."),
("AI cost control","Use caching, batching, model selection, and bounded context intentionally."),
("AI capstone","Design, evaluate, document, and test a small end-to-end AI feature.")
],
"ai":[
("AI history","Trace major ideas from symbolic systems to modern machine learning."),
("Probability intuition","Understand uncertainty, distributions, and why predictions are rarely absolute."),
("Supervised learning","Use labeled examples for classification and regression."),
("Unsupervised learning","Find structure when labels are unavailable."),
("Deep learning","Understand layers, representations, and gradient-based training."),
("Transformers","Learn the high-level architecture behind modern language models."),
("Attention","Understand how token relationships influence representations."),
("Tokens & context","See why tokenization and context windows affect model behavior."),
("Prompt engineering","Build prompts with role, context, constraints, examples, and evaluation."),
("Embeddings","Represent text for semantic comparison and retrieval."),
("Vector databases","Understand storing and searching embedding vectors."),
("RAG systems","Build the conceptual pipeline from documents to retrieval to answer."),
("Agents","Combine models, tools, state, validation, and bounded loops."),
("Evaluation","Create representative test sets and score AI behavior."),
("Safety","Design guardrails, permissions, validation, and human confirmation."),
("AI project","Ship a small AI feature with tests, failure cases, and documentation.")
],
"go":[
("Pointers","Understand addresses, pointers, and when pointer receivers are useful."),
("Methods","Attach behavior to types with clear method sets."),
("Packages","Organize Go code into reusable packages with deliberate APIs."),
("Modules","Use go.mod and dependency versions for reproducible projects."),
("Interfaces in practice","Use small interfaces at dependency boundaries."),
("File I/O","Read and write files while handling errors correctly."),
("JSON","Marshal and unmarshal structured data safely."),
("HTTP clients","Call APIs with timeouts, status handling, and decoding."),
("HTTP servers","Build handlers, routes, middleware, and JSON responses."),
("Testing","Write table-driven tests and benchmark important code."),
("Generics","Use type parameters where they remove duplication without obscuring design."),
("Context","Propagate cancellation, deadlines, and request-scoped values."),
("Goroutine lifecycle","Prevent leaks by defining ownership and shutdown."),
("Channels","Coordinate workers with bounded communication."),
("Worker pools","Control concurrent jobs and collect results."),
("Go capstone","Build a tested CLI or HTTP service with clean package boundaries.")
],
"typescript":[
("Type inference","Let TypeScript infer obvious types while keeping important public contracts explicit."),
("Literal types","Use literal values to model constrained states."),
("Discriminated unions","Represent state machines and API responses safely."),
("Type guards","Narrow unknown values with reusable runtime checks."),
("Generics","Write reusable functions and data structures without falling back to any."),
("Utility types","Use Partial, Pick, Omit, Record, and related helpers thoughtfully."),
("Readonly data","Prevent accidental mutation with readonly types."),
("Classes","Use classes when object identity and behavior genuinely belong together."),
("Modules","Design import/export boundaries that keep projects maintainable."),
("Async TypeScript","Type promises, async functions, and API results."),
("Runtime validation","Remember that compile-time types do not validate external JSON."),
("API clients","Create typed wrappers around HTTP endpoints."),
("DOM apps","Build a typed interactive browser application."),
("Node.js","Use TypeScript for scripts and server-side programs."),
("Testing","Test business logic and important integration boundaries."),
("TypeScript capstone","Build a typed app with API data, validation, tests, and clean architecture.")
],
"html":[
("Document structure","Build a full semantic document with a clear hierarchy."),
("Metadata","Use title, description, viewport, language, and social metadata correctly."),
("Text semantics","Choose headings, emphasis, quotes, lists, and code elements by meaning."),
("Navigation","Create accessible links and navigation structures."),
("Images","Use alt text, responsive images, figure, and captions."),
("Audio & video","Embed media with controls, captions, and fallbacks."),
("Tables","Build accessible tabular data with headers and scope."),
("Forms","Use labels, fieldsets, legends, input types, and validation attributes."),
("Buttons vs links","Choose controls based on whether the action navigates or performs an action."),
("Accessibility","Design keyboard, screen-reader, and focus-friendly markup."),
("SEO basics","Structure pages so search engines and users can understand them."),
("Embeds","Understand iframe security and sandboxing."),
("Web components","Explore custom elements and reusable markup."),
("HTML security","Avoid unsafe attributes and understand trust boundaries."),
("Performance","Keep markup lean and loading behavior intentional."),
("HTML project","Build a complete accessible multi-section page.")
],
"css":[
("Cascade","Understand origins, specificity, inheritance, and source order."),
("Specificity","Keep selectors predictable instead of fighting specificity wars."),
("Units","Choose px, rem, em, %, vw, vh, and newer responsive units appropriately."),
("Colors","Use modern color functions and accessible contrast."),
("Typography","Build readable type scales and responsive text."),
("Flexbox","Master alignment, wrapping, gaps, and flexible sizing."),
("Grid","Build responsive two-dimensional layouts."),
("Container queries","Style components based on their available space."),
("Responsive patterns","Use fluid layouts instead of device-specific hacks."),
("Positioning","Control overlays, sticky navigation, and anchored UI."),
("Transforms","Use transforms for visual movement without unexpected layout changes."),
("Animations","Build performant motion and respect reduced-motion preferences."),
("Transitions","Create responsive interaction states."),
("Architecture","Use naming and component conventions that scale."),
("Theming","Build light/dark themes with CSS variables."),
("CSS capstone","Build and polish a responsive component library.")
]
}
for _slug, _items in _EXTRA_LESSONS.items():
    if _slug in COURSES:
        COURSES[_slug]["lessons"].extend(_items)
    else:
        _title = {"ai":"AI Fundamentals","go":"Go (Golang)","typescript":"TypeScript","html":"HTML","css":"CSS"}[_slug]
        _category = "AI" if _slug=="ai" else ("Programming" if _slug in ("go","typescript") else "Web")
        COURSES[_slug] = {
            "title": _title,
            "level": "Beginner",
            "category": _category,
            "description": "A practical, project-driven course with short lessons, exercises, and a clear path from fundamentals to real applications.",
            "lessons": _items
        }

# Extend the original courses with deeper project and engineering topics.
for _slug, _items in {
"html-css":[("Design systems","Create reusable spacing, typography, component, and state rules."),
("Landing-page architecture","Break a polished landing page into semantic sections and reusable patterns."),
("Dashboard layout","Build a responsive dashboard with navigation, cards, tables, and empty states."),
("Portfolio build","Create a responsive developer portfolio with accessible navigation and project sections."),
("Final web project","Plan, build, audit, and publish a complete responsive website.")],
"javascript":[("Event delegation","Handle dynamic lists efficiently with event delegation."),
("Debouncing & throttling","Control expensive input and scroll handlers."),
("Modules at scale","Organize services, components, utilities, and shared types."),
("Frontend security","Treat DOM insertion, URLs, and user data as untrusted."),
("Final browser project","Build a complete app with state, persistence, APIs, error handling, and tests.")],
"sql":[("Advanced joins","Use multiple joins while keeping relationships and result cardinality clear."),
("Recursive queries","Understand hierarchical data and recursive CTEs."),
("Concurrency","Reason about simultaneous transactions and consistency."),
("Migrations","Make schema changes reproducible across environments."),
("Final database project","Design a production-style schema, queries, indexes, and migration plan.")],
"git-github":[("CI quality gates","Run tests and checks automatically before merging."),
("Deployment workflow","Connect repository changes to safe application deployments."),
("Semantic commits","Write history that communicates intent and supports release automation."),
("Repository security","Audit secrets, permissions, dependencies, and workflows."),
("Final Git workflow","Run a realistic feature from issue to branch, PR, review, merge, and release.")],
"ai-ml":[("Feature pipelines","Keep preprocessing and training transformations consistent."),
("Hyperparameters","Understand what training settings change and how to evaluate them."),
("Model debugging","Inspect errors by slice instead of trusting aggregate metrics."),
("Serving models","Separate training code from inference and application serving."),
("Final ML project","Build, evaluate, document, and serve a small model responsibly.")]
}.items():
    if _slug in COURSES:
        COURSES[_slug]["lessons"].extend(_items)


