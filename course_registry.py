"""Single catalog entry point for LearnPython.
Every new course has its own module; existing courses also have isolated adapter modules.
"""
import importlib.util
from pathlib import Path

LEGACY=["python","ai","go","typescript","html","css","dart","kotlin","java","cpp","csharp","rust","swift","php","ruby","r","bash-linux","react","nodejs","docker","flutter"]
NEW=["python-web","fastapi","django","flask","postgresql","mysql","redis","mongodb","dsa","algorithms","system-design","rest-api","graphql","ci-cd","kubernetes","terraform","aws-cloud","azure-cloud","gcp-cloud","networking","operating-systems","computer-architecture","compilers","distributed-systems","software-testing","qa-automation","devops","sre-observability","secure-coding","cryptography"]

def _load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    if not spec or not spec.loader:
        raise ImportError("Cannot load course module: "+str(path))
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def load_courses(python_course,legacy_courses):
    root=Path(__file__).resolve().parent/"courses"
    out=[]
    for slug in LEGACY:
        course=({"slug":"python","title":"Python","tag":"PYTHON","description":"The complete Python learning path.","lessons":python_course} if slug=="python" else next((c for c in legacy_courses if c.get("slug")==slug),None))
        if course:
            course=dict(course)
            course["course_file"]="courses/legacy_"+slug+".py"
            out.append(course)
    for slug in NEW:
        course=dict(_load(root/(slug+".py"),"learnpython_course_"+slug).COURSE)
        course["course_file"]="courses/"+slug+".py"
        out.append(course)
    return out

def extra_courses(python_course,legacy_courses):
    return [c for c in load_courses(python_course,legacy_courses) if c["slug"]!="python"]