import html, json, os, re
from pathlib import Path

os.environ.setdefault("DATABASE_PATH", "/tmp/learnpython-build.db")
from app import COURSE
from additional_courses import COURSES

OUT=Path("site"); OUT.mkdir(exist_ok=True)
ALL=[{"slug":"python","title":"Python","tag":"PYTHON","description":"The complete beginner-to-builder Python path: syntax, data, functions, files, errors, OOP, modules, projects and more.","lessons":[{"title":x["title"],"part":x.get("part","Python"),"body":x["body"]} for x in COURSE]}]+COURSES

def esc(x): return html.escape(str(x))
def shell(body,title="LearnPython"):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · LearnPython</title><meta name="description" content="Interactive coding courses with browser labs and local progress."><link rel="stylesheet" href="/assets/styles.css"></head><body><header><a class="logo" href="/">Learn<span>Python</span></a><nav><a href="/courses/">Courses</a><a href="/dashboard/">Dashboard</a><a class="btn" href="/courses/">Start learning</a></nav></header><main>{body}</main><footer>LearnPython · Learn → practice → build · Static on GitHub Pages</footer><script src="/assets/app.js"></script></body></html>'''
def card(c):
    return f'<a class="card" href="/courses/{esc(c["slug"])}/"><span class="tag">{esc(c["tag"])}</span><h2>{esc(c["title"])}</h2><p>{esc(c["description"])}</p><div class="meta">{len(c["lessons"])} lessons <span>Free</span></div><b class="btn primary">Open course →</b></a>'
def course_json():
    return json.dumps([{"slug":c["slug"],"title":c["title"],"tag":c["tag"],"description":c["description"],"lessons":[{"title":x["title"],"part":x.get("part",""),"body":x["body"]} for x in c["lessons"]]} for c in ALL],ensure_ascii=False)
def lesson_body(text):
    lines=str(text).replace("\r","").split("\n"); out=[]; buf=[]
    headings={"In Plain English","Why This Matters","Try It Yourself","Common Mistake","Level Up","OUTPUT","Part Recap","Quick Check"}
    def flush():
        if buf: out.append("<p>"+esc("\n".join(buf))+"</p>"); buf.clear()
    for line in lines:
        if line.startswith("<PARSED TEXT"): continue
        s=line.strip()
        if s in headings: flush(); out.append("<h2>"+esc(s)+"</h2>")
        elif re.match(r"^(python|python3|>>>|def |class |import |from |print\(|for |while |if |elif |else:)",s):
            flush(); out.append("<pre>"+esc(line)+"</pre>")
        elif not s: flush()
        else: buf.append(line)
    flush(); return "".join(out)
def index():
    return shell(f'''<section class="hero"><div><span class="eyebrow">INTERACTIVE CODE SCHOOL</span><h1>Learn code.<br>Actually build.</h1><p>Choose a path, learn one idea at a time, practice in your browser, track what you've finished, and build projects.</p><div class="actions"><a class="btn primary" href="/courses/">Explore courses →</a></div></div><div class="terminal"><small>~/learnpython</small><pre>course = choose("your path")
learn(course)
practice(course)
build(project)

# no gatekeeping. just build.</pre></div></section><section class="section"><span class="eyebrow">COURSE LIBRARY</span><h2>Pick what you want to learn.</h2><input id="search" class="search" placeholder="Search Python, AI, web, Go…"><div id="cards" class="grid">{"".join(card(c) for c in ALL)}</div></section><section class="section path"><div><b>01 · Learn</b><p>Short explanations without textbook fog.</p></div><div><b>02 · Practice</b><p>Interactive browser labs while the idea is fresh.</p></div><div><b>03 · Break it</b><p>Make mistakes, read errors, fix them.</p></div><div><b>04 · Build</b><p>Projects that turn knowledge into skill.</p></div></section>''',"LearnPython — Interactive Code School")
def courses_page():
    return shell(f'''<section class="libraryhero"><span class="eyebrow">LEARNPYTHON ACADEMY</span><h1>Choose your path.</h1><p>Start from zero and switch tracks whenever you want.</p><input id="search" class="search" placeholder="Search the library…"><div class="filters"><button class="filter active" data-filter="ALL">All</button><button class="filter" data-filter="PYTHON">Python</button><button class="filter" data-filter="AI">AI</button><button class="filter" data-filter="GO">Go</button><button class="filter" data-filter="TS">TypeScript</button><button class="filter" data-filter="HTML">HTML</button><button class="filter" data-filter="CSS">CSS</button></div><div id="cards" class="grid">{"".join(card(c) for c in ALL)}</div></section>''',"Course Library")
def course_page(c):
    rows="".join(f'<a class="lesson" href="/learn/{esc(c["slug"])}/{i}/"><span class="num">{i}</span><span><b>{esc(x["title"])}</b><small>{esc(x.get("part","Learn · practice · build"))}</small></span><em>Lesson →</em></a>' for i,x in enumerate(c["lessons"],1))
    return shell(f'''<section class="coursehero"><a class="muted" href="/courses/">← Course library</a><span class="eyebrow">{esc(c["tag"])}</span><h1>{esc(c["title"])}</h1><p>{esc(c["description"])}</p><a class="btn primary" href="/learn/{esc(c["slug"])}/1/">Start lesson 1 →</a></section><section class="section"><span class="eyebrow">CURRICULUM</span><h2>{len(c["lessons"])} lessons</h2>{rows}</section>''',f'{c["title"]} Course')
def lesson_page(c,i):
    x=c["lessons"][i-1]; starter='print("Hello, Python!")\nprint("Change this code and run it.")' if c["slug"]=="python" else '# Experiment here\nprint("Hello, learner!")'
    lab=f'''<section class="lab"><div class="sectionhead"><div><span class="eyebrow">BROWSER LAB</span><h2>Build. Run. Break. Fix.</h2></div><span>+5 XP / run</span></div><p>This lab runs locally in your browser. Nothing you type is sent to LearnPython.</p><textarea id="code">{esc(starter)}</textarea><div class="actions"><button class="btn primary" id="run">▶ Run</button><button class="btn" id="reset">↻ Reset</button><button class="btn" id="complete">✓ Complete lesson</button></div><pre id="out">Ready.</pre></section>'''
    return shell(f'''<section class="lessonpage"><a class="muted" href="/courses/{esc(c["slug"])}/">← {esc(c["title"])} course</a><span class="eyebrow">{esc(x.get("part","LESSON"))}</span><h1>Lesson {i}: {esc(x["title"])}</h1><article class="lessonbody">{lesson_body(x["body"])}</article>{lab}<div class="actions"><a class="btn" href="/courses/{esc(c["slug"])}/">Course index</a>{f'<a class="btn primary" href="/learn/{esc(c["slug"])}/{i+1}/">Next lesson →</a>' if i<len(c["lessons"]) else ""}</div><script>window.LESSON={{slug:{json.dumps(c["slug"])},index:{i},starter:{json.dumps(starter)}}};</script></section>''',f'Lesson {i}: {x["title"]}')
(Path("site/index.html")).write_text(index(),encoding="utf-8")
Path("site/courses").mkdir(parents=True,exist_ok=True); Path("site/courses/index.html").write_text(courses_page(),encoding="utf-8")
Path("site/dashboard").mkdir(parents=True,exist_ok=True); Path("site/dashboard/index.html").write_text(shell('<section class="section"><span class="eyebrow">YOUR LEARNING SPACE</span><h1>Keep going.</h1><p>Your progress is stored locally on this device. No account or password is required.</p><div id="progress"></div><a class="btn primary" href="/courses/">Choose a course →</a></section>',"Dashboard"),encoding="utf-8")
for c in ALL:
    d=Path("site/courses")/c["slug"]; d.mkdir(parents=True,exist_ok=True); (d/"index.html").write_text(course_page(c),encoding="utf-8")
    for i in range(1,len(c["lessons"])+1):
        p=Path("site/learn")/c["slug"]/str(i); p.mkdir(parents=True,exist_ok=True); (p/"index.html").write_text(lesson_page(c,i),encoding="utf-8")
a=Path("site/assets"); a.mkdir(parents=True,exist_ok=True)
a.joinpath("course-data.json").write_text(course_json(),encoding="utf-8")
print(f"Generated {len(ALL)} courses / {sum(len(c["lessons"]) for c in ALL)} lessons")
