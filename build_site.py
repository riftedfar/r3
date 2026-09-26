import json, os, re, runpy
ROOT=os.path.dirname(os.path.abspath(__file__))
SITE=os.path.join(ROOT,"site"); os.makedirs(SITE,exist_ok=True)
source=open(os.path.join(ROOT,"app.py"),encoding="utf-8").read()
m=re.search(r"COURSE\s*=\s*json\.loads\(r?'''(.*?)'''\)",source,re.S)
if not m: raise RuntimeError("Could not find COURSE in app.py")
python_course=json.loads(m.group(1))
extra=runpy.run_path(os.path.join(ROOT,"additional_courses.py"))["COURSES"]
for c in extra:
    for i,l in enumerate(c.get("lessons",[]),1): l.setdefault("n",i)
courses=[{"slug":"python","title":"The Ultimate Python Course","tag":"PYTHON","description":"A complete Python path from setup and fundamentals to practical development, projects, debugging and reference material.","lessons":python_course}]+extra
open(os.path.join(SITE,"courses.json"),"w",encoding="utf-8").write(json.dumps(courses,ensure_ascii=False,separators=(",",":")))
print("Built",len(courses),"courses and",sum(len(c["lessons"]) for c in courses),"lessons")
