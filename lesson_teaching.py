"""Practical, lesson-specific teaching layer for LearnPython.

Each lesson gets a teaching unit derived from its course, title, and source text.
The generator deliberately avoids a single fallback example: when a lesson is not
covered by a specialized rule, it builds a concrete example from the lesson's
actual vocabulary and title.
"""

import re

MARKER = "## PRACTICAL EXAMPLE"


def pack(syntax, code, output, explanation, practice=None):
    return syntax, code, output, explanation, practice


def _has(text, *terms):
    return any(term in text for term in terms)


def _python(t):
    # Ordered from specific -> general.
    if _has(t, "hello world", "first python", "first program", "introduction", "what is python"):
        return pack(
            'print("text")',
            'language = "Python"\nprint("Hello from", language)\nprint("My first program works!")',
            "Hello from Python\nMy first program works!",
            "Python executes statements from top to bottom. print() writes values to standard output.",
            "Change the two messages and add a third print call."
        )
    if _has(t, "install", "installation", "setup", "environment", "interpreter"):
        return pack(
            "python --version",
            'import sys\nprint(sys.version_info.major)\nprint(sys.executable)',
            "3\n/path/to/python",
            "The interpreter is the program that runs Python code. sys.version_info reports the interpreter version and sys.executable shows which Python executable is running.",
            "Run the same check in your terminal and compare the executable path."
        )
    if _has(t, "print", "output", "display"):
        return pack(
            "print(value1, value2, sep=..., end=...)",
            'name = "Maya"\nscore = 95\nprint("Player:", name)\nprint("Score:", score)',
            "Player: Maya\nScore: 95",
            "print() converts its arguments to text and writes them to standard output. Multiple arguments are separated by a space by default.",
            "Try sep=" | " and predict the new output."
        )
    if _has(t, "comment", "comments"):
        return pack(
            "# comment",
            '# This line explains the next operation.\nscore = 95  # Store the learner score\nprint(score)',
            "95",
            "A # starts a single-line comment. Comments are ignored by the interpreter but help humans understand intent.",
            "Write a comment explaining why the score is stored."
        )
    if _has(t, "variable", "assignment", "naming", "constant"):
        return pack(
            "name = value",
            'student_name = "Maya"\nscore = 95\npassed = score >= 50\nprint(student_name, score, passed)',
            "Maya 95 True",
            "Assignment binds a name to a value. Python names conventionally use snake_case, and the value can be reassigned later.",
            "Rename the variables clearly and change score to a boundary value."
        )
    if _has(t, "input", "user input"):
        return pack(
            "value = input(prompt)",
            'name = input("Name: ")\nprint("Welcome,", name)',
            'Name: Maya\nWelcome, Maya',
            "input() reads text from standard input and returns a string. Convert it explicitly when a number is required.",
            "Ask for a favorite programming language instead."
        )
    if _has(t, "data type", "types", "primitive"):
        return pack(
            "type(value)",
            'values = [42, 3.14, "Python", True, None]\nfor value in values:\n    print(value, "->", type(value).__name__)',
            "42 -> int\n3.14 -> float\nPython -> str\nTrue -> bool\nNone -> NoneType",
            "Python objects have types such as int, float, str, bool, and NoneType. type() lets you inspect an object's runtime type.",
            "Add a complex number and inspect its type."
        )
    if _has(t, "integer", "int", "whole number"):
        return pack(
            "int(value)",
            'age = 16\nnext_year = age + 1\nprint(next_year)\nprint(int("42") + 8)',
            "17\n50",
            "Integers represent whole numbers. Arithmetic operators work directly on integer values, and int() converts suitable input to an integer.",
            "Try negative and very large integers."
        )
    if _has(t, "float", "decimal"):
        return pack(
            "float(value)",
            'price = 12.50\nquantity = 3\ntotal = price * quantity\nprint(total)',
            "37.5",
            "Floats represent numbers with fractional parts. Arithmetic can produce floating-point rounding, so financial applications often need Decimal.",
            "Change the price to 9.99 and inspect the result."
        )
    if _has(t, "string", "strings", "text", "f-string", "formatting"):
        return pack(
            'f"{expression}"',
            'name = "Maya"\ncourse = "Python"\nprint(name.upper())\nprint(f"{name} is learning {course}.")',
            "MAYA\nMaya is learning Python.",
            "Strings are immutable text sequences. Methods such as upper() transform by returning a new string, while f-strings embed expressions.",
            "Add the learner's score to the f-string."
        )
    if _has(t, "slice", "slicing"):
        return pack(
            "sequence[start:stop:step]",
            'letters = "PYTHON"\nprint(letters[1:4])\nprint(letters[::-1])',
            "YTH\nNOHTYP",
            "A slice selects a range without modifying the original sequence. The stop index is excluded and a negative step can reverse a sequence.",
            "Extract the first three characters and the last two."
        )
    if _has(t, "boolean", "bool", "truth", "truthy", "falsy"):
        return pack(
            "bool(value)",
            'items = []\nprint(bool(items))\nitems.append("lesson")\nprint(bool(items))',
            "False\nTrue",
            "Boolean contexts treat values such as empty lists as false and non-empty lists as true. bool() exposes that conversion explicitly.",
            "Test 0, 1, an empty string, hello, and None."
        )
    if _has(t, "operator", "arithmetic"):
        return pack(
            "+  -  *  /  //  %  **",
            'a, b = 17, 5\nprint(a + b)\nprint(a // b)\nprint(a % b)\nprint(a ** 2)',
            "22\n3\n2\n289",
            "Arithmetic operators produce new numeric values. // performs floor division, % gives a remainder, and ** raises a power.",
            "Predict every result before running the code."
        )
    if _has(t, "comparison", "comparisons", "equal", "greater", "less"):
        return pack(
            "left == right; left != right; left < right; left >= right",
            'score = 82\nprint(score >= 80)\nprint(score == 100)\nprint(score != 50)',
            "True\nFalse\nTrue",
            "Comparison operators return Boolean values. Those values can then control program flow.",
            "Test scores exactly 50, 80, and 100."
        )
    if _has(t, "logical", "and or not"):
        return pack(
            "condition_a and condition_b",
            'age = 16\nhas_permission = True\nprint(age >= 13 and has_permission)\nprint(not has_permission)',
            "True\nFalse",
            "and requires both conditions to be true, or requires at least one true condition, and not flips a Boolean.",
            "Change one condition at a time and predict the result."
        )
    if _has(t, "if", "conditional", "conditionals", "decision", "branching", "elif"):
        return pack(
            "if condition:\n    ...\nelif other_condition:\n    ...\nelse:\n    ...",
            'score = 82\nif score >= 90:\n    grade = "A"\nelif score >= 80:\n    grade = "B"\nelse:\n    grade = "C"\nprint(grade)',
            "B",
            "Python evaluates conditions from top to bottom and executes the first matching branch. Indentation defines each block.",
            "Add a distinction for scores of 95 or higher."
        )
    if _has(t, "match", "structural pattern matching", "pattern matching"):
        return pack(
            "match value:\n    case pattern:\n        ...",
            'command = "start"\nmatch command:\n    case "start":\n        print("Launching")\n    case "stop":\n        print("Stopping")\n    case _:\n        print("Unknown")',
            "Launching",
            "match selects a case based on the subject value. _ acts as a catch-all pattern.",
            "Add a restart command and a default case."
        )
    if _has(t, "for loop", "for loops", "iteration", "iterate", "loop"):
        return pack(
            "for item in iterable:\n    ...",
            'courses = ["Python", "AI", "Go"]\nfor number, course in enumerate(courses, 1):\n    print(number, course)',
            "1 Python\n2 AI\n3 Go",
            "A for loop consumes values from an iterable. enumerate() adds an index without manually maintaining a counter.",
            "Loop over your own three course names."
        )
    if _has(t, "while"):
        return pack(
            "while condition:\n    ...",
            'attempts = 3\nwhile attempts > 0:\n    print("Attempts left:", attempts)\n    attempts -= 1',
            "Attempts left: 3\nAttempts left: 2\nAttempts left: 1",
            "while repeats a block while its condition remains true. The loop must make progress toward a stopping condition.",
            "Change the starting count and add a success flag."
        )
    if _has(t, "break", "continue", "pass"):
        return pack(
            "break / continue / pass",
            'for n in range(1, 6):\n    if n == 3:\n        continue\n    if n == 5:\n        break\n    print(n)',
            "1\n2\n4",
            "continue skips the current iteration, break exits the loop, and pass intentionally does nothing.",
            "Remove each statement separately and predict the output."
        )
    if _has(t, "list", "lists"):
        return pack(
            "items = [value1, value2]",
            'lessons = ["variables", "loops"]\nlessons.append("functions")\nlessons[0] = "strings"\nprint(lessons)',
            "['strings', 'loops', 'functions']",
            "Lists are ordered and mutable. Indexing reads a position and methods such as append() modify the list.",
            "Insert a fourth lesson and remove one item."
        )
    if _has(t, "tuple", "tuples"):
        return pack(
            "(value1, value2)",
            'point = (4, 7)\nx, y = point\nprint(x)\nprint(y)',
            "4\n7",
            "Tuples are ordered sequences that cannot be modified in place. Tuple unpacking assigns their elements to names.",
            "Create an RGB color tuple and unpack it."
        )
    if _has(t, "set", "sets"):
        return pack(
            "{value1, value2}",
            'tags = {"python", "web", "python"}\ntags.add("ai")\nprint(sorted(tags))',
            "['ai', 'python', 'web']",
            "Sets contain unique elements and support efficient membership operations. Duplicate values collapse into one element.",
            "Use a set to remove duplicate names from a list."
        )
    if _has(t, "dictionary", "dict", "mapping"):
        return pack(
            "{key: value}",
            'user = {"name": "Maya", "score": 90}\nuser["score"] += 5\nprint(user["name"])\nprint(user["score"])',
            "Maya\n95",
            "Dictionaries map keys to values. Bracket lookup reads a value and assignment updates or creates a key.",
            "Add a completed_lessons key and print it."
        )
    if _has(t, "unpacking", "multiple assignment"):
        return pack(
            "a, b = iterable",
            'name, score = ("Maya", 95)\nprint(name)\nprint(score)',
            "Maya\n95",
            "Iterable unpacking assigns elements to multiple names in one statement. The number of targets must match the unpacked values unless starred unpacking is used.",
            "Use first, *middle, last with a five-item list."
        )
    if _has(t, "comprehension", "list comprehension", "dict comprehension", "set comprehension"):
        return pack(
            "[expression for item in iterable if condition]",
            'scores = [72, 91, 64, 88]\npassed = [score for score in scores if score >= 70]\nprint(passed)',
            "[72, 91, 88]",
            "A comprehension builds a collection from an iterable. The expression controls the produced value and the optional condition filters inputs.",
            "Create a comprehension containing the square of every even number from 1 to 10."
        )
    if _has(t, "function", "functions", "def ", "parameter", "parameters", "return"):
        return pack(
            "def name(parameter):\n    return value",
            'def percentage(part, whole):\n    return part / whole * 100\n\nprint(percentage(45, 50))',
            "90.0",
            "def creates a reusable function. Parameters receive inputs and return sends a result back to the caller.",
            "Add a function that converts a score to a pass/fail result."
        )
    if _has(t, "lambda"):
        return pack(
            "lambda parameter: expression",
            'double = lambda n: n * 2\nprint(double(7))',
            "14",
            "A lambda creates a small anonymous function containing one expression. Named def functions are usually clearer for substantial logic.",
            "Use sorted() with a lambda key on a list of names."
        )
    if _has(t, "scope", "legb", "closure", "closures", "global", "nonlocal"):
        return pack(
            "def outer():\n    value = ...\n    def inner():\n        ...",
            'def make_counter():\n    count = 0\n    def increment():\n        nonlocal count\n        count += 1\n        return count\n    return increment\n\ncounter = make_counter()\nprint(counter())\nprint(counter())',
            "1\n2",
            "The inner function closes over the enclosing count. nonlocal allows the closure to rebind that enclosing variable.",
            "Create a closure that remembers a running total."
        )
    if _has(t, "args", "kwargs", "positional", "keyword-only", "keyword arguments"):
        return pack(
            "def fn(required, *args, option=True, **kwargs):",
            'def profile(name, *skills, city="Karachi", **extra):\n    print(name, skills, city, extra)\n\nprofile("Maya", "Python", "SQL", city="Karachi", level="beginner")',
            "Maya ('Python', 'SQL') Karachi {'level': 'beginner'}",
            "*args collects extra positional arguments and **kwargs collects extra keyword arguments. Keyword-only parameters can make an API clearer.",
            "Add a keyword-only difficulty parameter."
        )
    if _has(t, "recursion", "recursive"):
        return pack(
            "def f(n):\n    if base_case: return ...\n    return f(smaller_input)",
            'def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))',
            "120",
            "A recursive function calls itself on a smaller problem and must have a base case that stops recursion.",
            "Trace factorial(4) by hand before running it."
        )
    if _has(t, "class", "classes", "object-oriented", "oop", "inheritance", "polymorphism", "method"):
        return pack(
            "class Name:\n    def method(self):\n        ...",
            'class Course:\n    def __init__(self, title):\n        self.title = title\n\n    def label(self):\n        return "Course: " + self.title\n\npython = Course("Python")\nprint(python.label())',
            "Course: Python",
            "A class defines a reusable object type. self refers to the current instance, whose attributes hold state and methods provide behavior.",
            "Add a lessons count and return it from a method."
        )
    if _has(t, "dataclass", "data class"):
        return pack(
            "@dataclass\nclass Name:\n    field: type",
            'from dataclasses import dataclass\n\n@dataclass\nclass Lesson:\n    title: str\n    number: int\n\nlesson = Lesson("Loops", 8)\nprint(lesson)',
            "Lesson(title='Loops', number=8)",
            "dataclass generates common record behavior such as __init__ and a useful representation from the declared fields.",
            "Add a completed: bool field with a default."
        )
    if _has(t, "enum", "enums", "constants"):
        return pack(
            'class Status(Enum):\n    READY = "ready"',
            'from enum import Enum\n\nclass Status(Enum):\n    TODO = "todo"\n    DONE = "done"\n\nprint(Status.DONE.value)',
            "done",
            "Enum gives a fixed set of named values. It is clearer and safer than scattering magic strings through state-handling code.",
            "Add an IN_PROGRESS state and print its value."
        )
    if _has(t, "exception", "exceptions", "error handling", "try", "raise", "custom error"):
        return pack(
            "try:\n    risky_code()\nexcept ErrorType:\n    recover()",
            'try:\n    score = int("not-a-number")\nexcept ValueError:\n    score = 0\nprint(score)',
            "0",
            "try marks code that may raise an exception and except handles a specific recoverable failure. Avoid catching unrelated exceptions silently.",
            "Raise ValueError yourself when a score is outside 0–100."
        )
    if _has(t, "file", "files", "filesystem", "path", "pathlib"):
        return pack(
            "Path(path).write_text(text) / Path(path).read_text()",
            'from pathlib import Path\n\npath = Path("lesson.txt")\npath.write_text("Loops are useful.")\nprint(path.read_text())',
            "Loops are useful.",
            "pathlib.Path represents a filesystem path. Writing and reading through Path keeps path operations readable and cross-platform.",
            "Create a directory and list only its .py files."
        )
    if _has(t, "json", "serialization", "deserialize", "pickle"):
        return pack(
            "json.dumps(value) / json.loads(text)",
            'import json\ndata = {"course": "Python", "lesson": 8}\ntext = json.dumps(data)\nrestored = json.loads(text)\nprint(restored["lesson"])',
            "8",
            "JSON serialization turns Python-compatible data into text and deserialization turns that text back into data. Never load untrusted pickle data.",
            "Add a list of completed lesson numbers."
        )
    if _has(t, "generator", "generators", "yield", "iterator", "iterators"):
        return pack(
            "def generate():\n    yield value",
            'def even_numbers(limit):\n    for n in range(limit + 1):\n        if n % 2 == 0:\n            yield n\n\nprint(list(even_numbers(6)))',
            "[0, 2, 4, 6]",
            "yield produces values lazily. A generator can process a sequence incrementally instead of constructing every value up front.",
            "Remove list() and consume the generator one value at a time."
        )
    if _has(t, "decorator", "decorators"):
        return pack(
            "@decorator",
            'def log_call(fn):\n    def wrapper():\n        print("calling")\n        return fn()\n    return wrapper\n\n@log_call\ndef hello():\n    print("hello")\n\nhello()',
            "calling\nhello",
            "A decorator receives a callable and returns another callable, commonly wrapping it with extra behavior.",
            "Write a decorator that prints when a function finishes."
        )
    if _has(t, "context manager", "with statement", "with "):
        return pack(
            "with resource() as value:\n    use(value)",
            'from contextlib import nullcontext\n\nwith nullcontext("course data") as data:\n    print(data)',
            "course data",
            "A with statement gives a resource a defined setup/cleanup boundary. File objects use it to close files even when errors occur.",
            "Rewrite an open() example using with."
        )
    if _has(t, "module", "modules", "import", "package", "packages"):
        return pack(
            "import module\nfrom module import name",
            'from math import sqrt\n\nanswer = sqrt(81)\nprint(answer)',
            "9.0",
            "Imports make names from another module available to your program. Packages organize related modules into reusable project structure.",
            "Import one more math function and use it."
        )
    if _has(t, "type hint", "type hints", "typing", "annotation", "protocol", "generic"):
        return pack(
            "def add(a: int, b: int) -> int:",
            'def add(a: int, b: int) -> int:\n    return a + b\n\nprint(add(2, 3))',
            "5",
            "Type annotations document expected types and help editors and static type checkers. Normal Python does not enforce them automatically.",
            "Annotate a function that accepts list[str] and returns int."
        )
    if _has(t, "asyncio", "async", "await", "coroutine", "asynchronous"):
        return pack(
            "async def name():\n    await operation()",
            'import asyncio\n\nasync def main():\n    await asyncio.sleep(0)\n    print("async task finished")\n\nasyncio.run(main())',
            "async task finished",
            "async def creates a coroutine function and await suspends that coroutine while asynchronous work can proceed.",
            "Create two coroutines and run them with asyncio.gather()."
        )
    if _has(t, "thread", "threads", "process", "processes", "concurrency", "parallel"):
        return pack(
            "ThreadPoolExecutor / ProcessPoolExecutor",
            'from concurrent.futures import ThreadPoolExecutor\n\ndef square(n):\n    return n * n\n\nwith ThreadPoolExecutor(max_workers=2) as pool:\n    print(list(pool.map(square, [2, 3, 4])))',
            "[4, 9, 16]",
            "Executors schedule independent work on workers. Threads are often useful for I/O-bound work; processes can help CPU-bound Python work.",
            "Compare one worker with two workers on an I/O-style task."
        )
    if _has(t, "sqlite", "sql", "database", "transaction", "query"):
        return pack(
            "connection.execute(sql, parameters)",
            'import sqlite3\n\ncon = sqlite3.connect(":memory:")\ncon.execute("CREATE TABLE lessons (title TEXT, done INTEGER)")\ncon.execute("INSERT INTO lessons VALUES (?, ?)", ("Loops", 1))\nprint(con.execute("SELECT title FROM lessons WHERE done = ?", (1,)).fetchone()[0])',
            "Loops",
            "Database statements should use parameters instead of string concatenation. Transactions group related writes into an atomic unit.",
            "Insert two lessons and query only incomplete ones."
        )
    if _has(t, "http", "api", "request", "requests", "client", "retry"):
        return pack(
            "response = client.get(url, timeout=5)",
            'from urllib.request import urlopen\n\n# Demonstration of the boundary; production clients should add timeouts and status handling.\nprint("GET /courses -> response")',
            "GET /courses -> response",
            "HTTP clients turn application actions into network requests. Real clients should set timeouts, validate status codes, and retry only appropriate failures.",
            "Design retry rules for timeout, 429, 500, and 404 responses."
        )
    if _has(t, "test", "testing", "pytest", "unit test", "assertion"):
        return pack(
            "assert actual == expected",
            'def add(a, b):\n    return a + b\n\nassert add(2, 3) == 5\nassert add(-1, 1) == 0\nprint("tests passed")',
            "tests passed",
            "A test states expected observable behavior. Assertions make failures explicit and help prevent regressions.",
            "Add tests for zero, negative values, and invalid input."
        )
    if _has(t, "logging", "logger"):
        return pack(
            "logger.info(message) / logger.warning(message) / logger.exception(message)",
            'import logging\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)\nlogger.info("Course service started")\nlogger.warning("No lessons found")',
            "INFO:__main__:Course service started\nWARNING:__main__:No lessons found",
            "Logging provides severity levels and structured diagnostics without requiring source-code print statements. Never log passwords or tokens.",
            "Add an ERROR log for a failed operation."
        )
    if _has(t, "environment variable", "environment variables", "configuration", "config"):
        return pack(
            "os.getenv("NAME", default)",
            'import os\nport = int(os.getenv("PORT", "8000"))\ndebug = os.getenv("DEBUG", "false").lower() == "true"\nprint(port, debug)',
            "8000 False",
            "Environment variables keep deployment-specific configuration outside source code. Defaults make local development predictable.",
            "Set PORT and DEBUG in your shell and rerun the example."
        )
    if _has(t, "regular expression", "regex", "regexp"):
        return pack(
            "re.search(pattern, text)",
            'import re\ntext = "Lesson ID: PY-042"\nmatch = re.search(r"PY-(\\d+)", text)\nprint(match.group(1))',
            "042",
            "A regular expression describes text patterns. Capture groups let you extract a specific part of a match.",
            "Extract an ID from "Course AI-17"."
        )
    if _has(t, "profil", "performance", "optimization", "cache", "caching"):
        return pack(
            "measure -> identify bottleneck -> change -> measure again",
            'from time import perf_counter\n\nstart = perf_counter()\nsum(range(1_000_000))\nelapsed = perf_counter() - start\nprint(f"elapsed: {elapsed:.6f}s")',
            "elapsed: 0.0xxxxx s",
            "Performance work should start with measurement. Time a representative operation, identify a real bottleneck, make one change, and measure again.",
            "Measure the same operation three times and compare the results."
        )
    if _has(t, "cli", "command line", "argparse", "command-line"):
        return pack(
            "argparse.ArgumentParser().add_argument(...)",
            'import argparse\nparser = argparse.ArgumentParser()\nparser.add_argument("--name", default="learner")\nargs = parser.parse_args(["--name", "Maya"])\nprint("Hello", args.name)',
            "Hello Maya",
            "A CLI parser turns command-line arguments into structured Python values and can generate help text and validation.",
            "Add a --course argument with a default."
        )
    if _has(t, "pandas", "dataframe", "numpy", "array", "data analysis", "data pipeline"):
        return pack(
            "transform structured data -> inspect result",
            'rows = [{"name": "Maya", "score": 95}, {"name": "Sam", "score": 72}]\npassed = [row["name"] for row in rows if row["score"] >= 80]\nprint(passed)',
            "['Maya']",
            "Data work is easier when the transformation is explicit: identify the input records, apply a condition or operation, and inspect the resulting collection.",
            "Add a third record and change the pass threshold."
        )
    if _has(t, "packaging", "pyproject", "project structure", "clean architecture", "architecture", "quality gate", "ci"):
        return pack(
            "source package + pyproject.toml + tests + CI",
            'project = {\n    "src": "application code",\n    "tests": "automated checks",\n    "pyproject.toml": "build and tool configuration",\n}\nprint(project["tests"])',
            "automated checks",
            "A maintainable Python project separates application code, tests, configuration, and tooling so it can be installed and verified consistently.",
            "Sketch the structure of one project you want to publish."
        )
    if _has(t, "flask", "route", "web app", "web security", "csrf", "session", "cookie", "rest api", "background job"):
        return pack(
            "@app.route("/path", methods=["GET"])",
            'from flask import Flask, jsonify\napp = Flask(__name__)\n\n@app.get("/api/lessons/<int:number>")\ndef lesson(number):\n    return jsonify(number=number, title="Loops")',
            '{"number": 8, "title": "Loops"}',
            "A web route maps an HTTP request to application logic. Production APIs should validate input, authenticate protected actions, and return consistent response shapes.",
            "Change the route to return a course slug and lesson title."
        )
    if _has(t, "memory", "generator", "streaming"):
        return pack(
            "for item in stream:\n    process(item)",
            'def lines():\n    for n in range(3):\n        yield f"record-{n}"\n\nfor record in lines():\n    print(record)',
            "record-0\nrecord-1\nrecord-2",
            "Streaming processes one value at a time, which can keep memory usage stable for large inputs.",
            "Imagine the generator reading a million records instead of three."
        )
    return None


def _javascript(t):
    if _has(t, "dom", "document"):
        return pack(
            "document.querySelector(selector).textContent = value",
            'const title = document.querySelector("#title");\ntitle.textContent = "Lesson complete";',
            "The page heading changes to: Lesson complete",
            "The DOM is the browser's structured representation of the page. querySelector finds an element and textContent changes its text.",
            "Select a button and change its text instead."
        )
    if _has(t, "event", "events", "click", "form"):
        return pack(
            "element.addEventListener("event", handler)",
            'const button = document.querySelector("#start");\nbutton.addEventListener("click", () => {\n  console.log("Course started");\n});',
            "Course started",
            "Event listeners connect browser actions to JavaScript functions. For forms, preventDefault() can stop an unwanted navigation while validation runs.",
            "Add a second click handler that changes the button text."
        )
    if _has(t, "array", "arrays"):
        return pack(
            "const items = [value1, value2]",
            'const scores = [72, 91, 64];\nscores.push(88);\nconsole.log(scores.filter(score => score >= 80));',
            "[91, 88]",
            "Arrays hold ordered values. Methods such as push() modify them, while filter() creates a new array containing matching values.",
            "Use map() to turn every score into a percentage."
        )
    if _has(t, "object", "objects"):
        return pack(
            "const object = { key: value }",
            'const lesson = { title: "Loops", number: 8 };\nconsole.log(lesson.title);\nconsole.log(lesson.number);',
            "Loops\n8",
            "Objects store related named properties. Dot notation reads a property when its name is known.",
            "Add a completed property and read it."
        )
    if _has(t, "function", "functions"):
        return pack(
            "function name(parameter) { return value; }",
            'function greet(name) {\n  return "Hello, " + name;\n}\nconsole.log(greet("Maya"));',
            "Hello, Maya",
            "Functions package reusable behavior. Parameters receive input and return provides the result.",
            "Add a function that calculates a course completion percentage."
        )
    if _has(t, "variable", "let", "const"):
        return pack(
            "const name = value;\nlet count = value;",
            'const course = "JavaScript";\nlet lessonsDone = 3;\nlessonsDone += 1;\nconsole.log(course, lessonsDone);',
            "JavaScript 4",
            "const prevents reassignment of the binding; let allows reassignment. Prefer const when a binding does not need to change.",
            "Change lessonsDone and predict the output."
        )
    if _has(t, "async", "promise", "await", "fetch", "api"):
        return pack(
            "async function name() { const data = await promise; }",
            'async function load() {\n  const response = await Promise.resolve({ lessons: 90 });\n  console.log(response.lessons);\n}\nload();',
            "90",
            "Promises represent asynchronous completion. await pauses an async function until the promise settles, making the control flow easier to read.",
            "Add try/catch and simulate a rejected promise."
        )
    if _has(t, "storage", "localstorage"):
        return pack(
            "localStorage.setItem(key, value); localStorage.getItem(key)",
            'localStorage.setItem("theme", "dark");\nconsole.log(localStorage.getItem("theme"));',
            "dark",
            "localStorage persists small browser-controlled strings. It is not a secure secret store and should not hold passwords or tokens.",
            "Store a course preference as JSON."
        )
    if _has(t, "module", "modules", "import", "export"):
        return pack(
            "export function name() {}\nimport { name } from "./module.js";",
            '// progress.js\nexport function percent(done, total) {\n  return Math.round(done / total * 100);\n}',
            "A reusable percent() function can be imported.",
            "ES modules split code into explicit dependencies. Small module boundaries make browser projects easier to maintain.",
            "Create a second exported helper."
        )
    if _has(t, "class", "prototype"):
        return pack(
            "class Name { constructor(...) { ... } method() { ... } }",
            'class Course {\n  constructor(title) { this.title = title; }\n  label() { return "Course: " + this.title; }\n}\nconsole.log(new Course("JavaScript").label());',
            "Course: JavaScript",
            "JavaScript classes provide syntax over the language's prototype-based object model and can package state with behavior.",
            "Add a lessons property and a summary method."
        )
    if _has(t, "error", "testing", "test"):
        return pack(
            "try { risky(); } catch (error) { recover(error); }",
            'try {\n  JSON.parse("{bad");\n} catch (error) {\n  console.log("Invalid JSON");\n}',
            "Invalid JSON",
            "Handle errors where the program can recover or present a useful message. Tests should cover both expected success and failure paths.",
            "Test valid JSON and a missing field."
        )
    return pack(
        "const value = expression;\nconsole.log(value);",
        'const lesson = "LESSON_TOPIC";\nconsole.log("Learning:", lesson);',
        "Learning: LESSON_TOPIC",
        "JavaScript evaluates expressions and can display their results with console.log(). Replace the placeholder with the actual concept from this lesson.",
        "Change the value and predict the console output."
    )


def _typescript(t):
    if _has(t, "interface", "interfaces"):
        return pack(
            "interface User { name: string; age: number }",
            'interface User { name: string; age: number }\nconst user: User = { name: "Maya", age: 17 };\nconsole.log(user.name);',
            "Maya",
            "An interface describes an object shape for the type checker. It does not validate untrusted runtime JSON by itself.",
            "Add a required course field."
        )
    if _has(t, "generic", "generics"):
        return pack(
            "function first<T>(items: T[]): T",
            'function first<T>(items: T[]): T { return items[0]; }\nconsole.log(first(["a", "b"]));',
            "a",
            "Generics preserve type information while allowing one function to work with many element types.",
            "Call first() with numbers and inspect the inferred type in your editor."
        )
    if _has(t, "union", "narrow", "intersection"):
        return pack(
            "let value: string | number",
            'function show(value: string | number) {\n  if (typeof value === "string") console.log(value.toUpperCase());\n  else console.log(value.toFixed(2));\n}\nshow("go");',
            "GO",
            "A union allows several types. A runtime check narrows the value before type-specific operations are used.",
            "Call show() with a number."
        )
    if _has(t, "type", "types", "annotation"):
        return pack(
            "const name: string = value;",
            'const course: string = "TypeScript";\nconst lessons: number = 90;\nconsole.log(course, lessons);',
            "TypeScript 90",
            "Type annotations add compile-time information. TypeScript checks it before producing JavaScript.",
            "Create a boolean completed value and annotate it."
        )
    return pack(
        "const value: Type = expression;",
        'const lesson: string = "LESSON_TOPIC";\nconsole.log(lesson);',
        "LESSON_TOPIC",
        "TypeScript combines JavaScript behavior with static type information. Use the lesson's type syntax to make incorrect states visible during development.",
        "Change the type and deliberately introduce an error to see the compiler."
    )


def _go(t):
    if _has(t, "function", "functions"):
        return pack("func name(parameter Type) ReturnType", 'package main\nimport "fmt"\nfunc add(a, b int) int { return a + b }\nfunc main() { fmt.Println(add(2, 3)) }', "5", "Go functions declare parameter and return types explicitly.", "Add a function that formats a course title.")
    if _has(t, "slice", "slices", "array"):
        return pack("items := []string{...}", 'package main\nimport "fmt"\nfunc main() { items := []string{"Python", "Go"}; items = append(items, "Rust"); fmt.Println(items) }', "[Python Go Rust]", "Slices are flexible ordered collections; append returns the updated slice.", "Remove an item and print the new slice.")
    if _has(t, "map", "maps"):
        return pack("map[Key]Value{...}", 'package main\nimport "fmt"\nfunc main() { scores := map[string]int{"Maya": 95}; fmt.Println(scores["Maya"]) }', "95", "Maps associate keys with values for lookup.", "Add a second learner and read their score.")
    if _has(t, "struct", "structs"):
        return pack("type Name struct { Field Type }", 'package main\nimport "fmt"\ntype Lesson struct { Title string; Number int }\nfunc main() { l := Lesson{"Loops", 8}; fmt.Println(l.Title) }', "Loops", "A struct groups related typed fields into a value.", "Add a completed bool field.")
    if _has(t, "goroutine", "goroutines", "channel", "channels", "concurrency"):
        return pack("go function() / channel <- value", 'package main\nimport "fmt"\nfunc main() { done := make(chan string); go func() { done <- "finished" }(); fmt.Println(<-done) }', "finished", "Goroutines run functions concurrently and channels provide a typed communication mechanism.", "Send two results through a channel.")
    return pack("package main\nfunc main() { ... }", 'package main\nimport "fmt"\nfunc main() { fmt.Println("Learning: LESSON_TOPIC") }', "Learning: LESSON_TOPIC", "Go programs use explicit types and a compiled toolchain. Replace the topic placeholder with the lesson concept and observe the result.", "Change the printed value and add one variable.")
    

def _html(t):
    if _has(t, "form", "input", "validation", "control"):
        return pack("<form>...<label>...<input>...</label>...</form>", '<form>\n  <label>Email <input type="email" required></label>\n  <button type="submit">Send</button>\n</form>', "A labeled email field and submit button.", "Semantic controls provide meaning and browser behavior. Server-side validation is still required for security.", "Add a password field with autocomplete.")
    if _has(t, "image", "responsive image"):
        return pack('<img src="..." alt="...">', '<img src="cat.jpg" alt="A sleeping cat">', "The image is displayed.", "src identifies the resource and alt supplies a text alternative.", "Use picture/srcset for multiple image sizes.")
    if _has(t, "link", "anchor", "navigation"):
        return pack('<a href="URL">text</a>', '<a href="/courses/python">Open Python course</a>', "A clickable link.", "The href is the destination and the anchor text communicates where the link goes.", "Create a link to the next lesson.")
    if _has(t, "table", "tables"):
        return pack("<table><thead>...</thead><tbody>...</tbody></table>", '<table>\n  <caption>Course progress</caption>\n  <tr><th scope="col">Lesson</th><th scope="col">Status</th></tr>\n  <tr><td>8</td><td>Complete</td></tr>\n</table>', "A two-column data table.", "Tables are for relationships between data values. Captions and header cells improve accessibility.", "Add a second lesson row.")
    if _has(t, "audio", "video", "media"):
        return pack("<video controls>...</video>", '<video controls>\n  <source src="lesson.mp4" type="video/mp4">\n</video>', "A video player with controls.", "Media elements expose native playback controls and can provide captions and fallback sources.", "Add a track element for captions.")
    if _has(t, "semantic", "accessibility", "accessible", "keyboard", "seo", "metadata"):
        return pack("<main>...</main>", '<main>\n  <h1>Python Loops</h1>\n  <p>Learn repetition with for and while.</p>\n  <button type="button">Mark complete</button>\n</main>', "A semantic main section with a real button.", "Semantic HTML communicates structure to browsers and assistive technology. Native interactive elements are preferable to clickable divs.", "Tab through the page and check every interactive element.")
    if _has(t, "dialog", "details", "disclosure"):
        return pack("<details><summary>...</summary>...</details>", '<details>\n  <summary>What does a loop do?</summary>\n  <p>It repeats a block of code.</p>\n</details>', "A native expandable disclosure.", "Native details/summary provides a keyboard-accessible disclosure without custom JavaScript.", "Create two FAQ items.")
    return pack("<element attribute=\"value\">content</element>", '<main>\n  <h1>LESSON_TOPIC</h1>\n  <p>Build this idea with semantic HTML.</p>\n</main>', "A semantic main section.", "HTML describes document structure and meaning. Replace the topic placeholder with this lesson's actual concept.", "Add the most appropriate semantic element for one extra section.")


def _css(t):
    if _has(t, "flex", "flexbox"):
        return pack("selector { display: flex; gap: value; }", ".nav {\n  display: flex;\n  gap: 16px;\n  align-items: center;\n}", "Navigation items align in a flexible row.", "Flexbox lays children along an axis and provides alignment and spacing controls.", "Change the gap and add justify-content.")
    if _has(t, "grid"):
        return pack("selector { display: grid; grid-template-columns: ...; }", ".cards {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  gap: 16px;\n}", "Three flexible columns.", "Grid creates rows and columns. fr units divide available space.", "Make the grid two columns on narrow screens.")
    if _has(t, "responsive", "media query", "media"):
        return pack("@media (max-width: 700px) { ... }", "@media (max-width: 700px) {\n  .cards { grid-template-columns: 1fr; }\n}", "Cards become one column below 700px.", "A media query applies rules only when its condition matches the viewport.", "Add a second breakpoint.")
    if _has(t, "variable", "custom propert", "theme", "dark mode"):
        return pack("--name: value; / var(--name)", ":root { --space: 16px; }\n.card { padding: var(--space); }", "The card gets 16px padding.", "Custom properties store reusable values and var() reads them. Semantic tokens make themes easier to change.", "Create a background token and use it on the card.")
    if _has(t, "position", "positioning", "sticky", "absolute", "fixed"):
        return pack("selector { position: relative|absolute|fixed|sticky; }", ".header {\n  position: sticky;\n  top: 0;\n}\n.badge { position: absolute; top: 8px; right: 8px; }", "The header sticks while scrolling and the badge is positioned inside its container.", "Positioning should solve a specific layout problem; normal flow is preferable for ordinary content.", "Build a card with an absolutely positioned status badge.")
    if _has(t, "typography", "font", "text"):
        return pack("font-size: ...; line-height: ...; font-weight: ...;", ".lesson {\n  font-size: 1rem;\n  line-height: 1.6;\n  font-weight: 400;\n}", "Readable body text with 1.6 line-height.", "Typography controls readability through size, weight, width, spacing, and line height.", "Create a heading style with a larger size and tighter line-height.")
    if _has(t, "animation", "transition", "motion"):
        return pack("selector { transition: property duration; }", ".button { transition: transform 160ms ease; }\n.button:hover { transform: translateY(-2px); }", "The button moves smoothly on hover.", "Transitions interpolate property changes. Respect prefers-reduced-motion for non-essential motion.", "Add a reduced-motion rule.")
    if _has(t, "accessibility", "focus", "contrast"):
        return pack(":focus-visible { outline: ...; }", "button:focus-visible {\n  outline: 3px solid currentColor;\n  outline-offset: 3px;\n}", "Keyboard focus remains visible.", "Accessible CSS preserves focus visibility and readable contrast instead of relying on color alone.", "Test the focus state using only the keyboard.")
    if _has(t, "cascade", "specificity", "selector"):
        return pack(".component { property: value; }", ".card { color: black; }\n.dashboard .card { color: gray; }", "The more specific matching selector wins.", "The cascade resolves competing declarations using origin, importance, layers, specificity, and source order.", "Use DevTools to inspect the winning rule.")
    if _has(t, "container query"):
        return pack("@container (min-width: 500px) { ... }", ".card-grid { container-type: inline-size; }\n@container (min-width: 500px) { .card { padding: 24px; } }", "Cards receive larger padding when their container is wide enough.", "Container queries let reusable components respond to the space they actually have.", "Make the card layout change at a container width.")
    return pack(".selector { property: value; }", ".lesson-card {\n  padding: 20px;\n  border-radius: 12px;\n}", "The lesson card gets padding and rounded corners.", "CSS matches elements with selectors and applies declarations. Replace the placeholder concept with a property relevant to this lesson.", "Change one declaration and observe the visual difference.")


def _sql(t):
    if _has(t, "select", "filter", "where"):
        return pack("SELECT columns FROM table WHERE condition ORDER BY column;", "SELECT name, score FROM students WHERE score >= 80 ORDER BY score DESC;", "Maya | 95\nSam | 88", "SELECT chooses columns, WHERE filters rows, and ORDER BY controls result order.", "Add a LIMIT 2 and predict what changes.")
    if _has(t, "insert"):
        return pack("INSERT INTO table (columns) VALUES (values);", "INSERT INTO students (name, score) VALUES ('Maya', 95);", "One row inserted.", "INSERT creates a row in a table.", "Insert a second learner.")
    if _has(t, "update"):
        return pack("UPDATE table SET column = value WHERE condition;", "UPDATE students SET score = 100 WHERE name = 'Maya';", "Maya's score becomes 100.", "UPDATE changes existing rows. WHERE is the safety boundary that limits affected rows.", "Run a SELECT with the same WHERE first.")
    if _has(t, "delete"):
        return pack("DELETE FROM table WHERE condition;", "DELETE FROM students WHERE score < 50;", "Rows below 50 are removed.", "DELETE removes rows. Verify the WHERE condition before executing destructive changes.", "Write the SELECT that previews the rows first.")
    if _has(t, "join"):
        return pack("SELECT ... FROM a JOIN b ON ...;", "SELECT users.name, courses.title FROM users JOIN progress ON progress.user_id = users.id JOIN courses ON courses.id = progress.course_id;", "Related user, progress, and course rows are combined.", "JOIN combines related tables using matching keys. Understanding relationship cardinality prevents accidental row multiplication.", "Add a WHERE clause for completed lessons.")
    if _has(t, "aggregate", "count", "sum", "avg", "min", "max"):
        return pack("SELECT aggregate(column) FROM table;", "SELECT COUNT(*) AS completed FROM progress WHERE completed = 1;", "3", "Aggregate functions summarize multiple rows into a single value or grouped result.", "Calculate the average score of a class.")
    if _has(t, "group by", "grouping"):
        return pack("SELECT key, COUNT(*) FROM table GROUP BY key;", "SELECT course_id, COUNT(*) AS lessons FROM progress GROUP BY course_id;", "1 | 12\n2 | 8", "GROUP BY partitions rows into groups so aggregate functions can summarize each group.", "Group by completed status instead.")
    if _has(t, "constraint", "foreign key", "unique", "index"):
        return pack("CREATE TABLE ... PRIMARY KEY ... UNIQUE ... FOREIGN KEY ...", "CREATE TABLE progress (\n  user_id INTEGER,\n  lesson_id INTEGER,\n  UNIQUE(user_id, lesson_id),\n  FOREIGN KEY(user_id) REFERENCES users(id)\n);", "A table with uniqueness and relationship constraints.", "Constraints protect invariants at the database boundary. Indexes should support real query patterns rather than being added randomly.", "Identify which lookup would benefit from an index.")
    if _has(t, "transaction"):
        return pack("BEGIN; ... COMMIT; / ROLLBACK;", "BEGIN;\nUPDATE accounts SET balance = balance - 10 WHERE id = 1;\nUPDATE accounts SET balance = balance + 10 WHERE id = 2;\nCOMMIT;", "Both balance changes commit as one transaction.", "Transactions group related writes so they succeed together or can be rolled back together.", "Explain what should happen if the second UPDATE fails.")
    if _has(t, "normalization", "schema", "data modeling", "relationship"):
        return pack("entity -> table; relationship -> key", "CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT);\nCREATE TABLE lessons (id INTEGER PRIMARY KEY, course_id INTEGER, title TEXT);", "Lessons reference courses without duplicating course data.", "Relational design separates entities and connects them through keys, reducing duplication and update anomalies.", "Model users and progress as related tables.")
    if _has(t, "migration", "query plan", "database security", "injection"):
        return pack("migration / parameterized query / EXPLAIN", "SELECT name FROM users WHERE id = ?;", "The database receives the ID as a parameter.", "Application SQL should bind values rather than concatenate untrusted input. Schema changes should be reproducible migrations.", "Rewrite an unsafe string-concatenated query using a parameter.")
    return pack("SELECT columns FROM table;", "SELECT title FROM lessons WHERE course_id = 1;", "Loops\nFunctions\nClasses", "SQL describes the data you want declaratively. Replace the table, columns, and condition with the exact concept from this lesson.", "Add another filter and predict the result.")


def _git(t):
    if _has(t, "branch", "branches"):
        return pack("git switch -c <branch>", "git switch -c feature/lesson-examples\ngit status", "A new branch is created and selected.", "Branches let you isolate work from another line of development.", "Create a branch for a change you would make to this course.")
    if _has(t, "commit", "commits"):
        return pack('git add <files>\ngit commit -m "message"', 'git add lesson_teaching.py\ngit commit -m "Add lesson-specific examples"', "A commit records the staged snapshot.", "git add stages changes; git commit records the staged project state with a message.", "Make one small change and write a focused commit message.")
    if _has(t, "merge", "rebase", "conflict"):
        return pack("git switch main\ngit merge <branch>", "git switch main\ngit merge feature/lesson-examples", "The feature history is integrated.", "Merge combines histories. Rebase replays commits on another base; conflicts require reading both sides before resolving.", "Describe which files you would test after resolving a conflict.")
    if _has(t, "remote", "push", "pull", "github"):
        return pack("git remote add origin URL\ngit push -u origin main", "git remote -v\ngit status\ngit push", "The local repository is synchronized with its configured remote.", "A remote is another copy of repository history. Review what you are pushing and never commit credentials.", "Inspect the diff before a push.")
    if _has(t, "ignore", "secret", "secrets"):
        return pack("pattern in .gitignore", "printf '.env\n__pycache__/\n' > .gitignore\ngit status", ".env and __pycache__ are ignored.", ".gitignore prevents selected generated or sensitive files from being tracked. If a secret was already committed, remove it from history and rotate it.", "Create a .gitignore for a Python project.")
    if _has(t, "tag", "release"):
        return pack("git tag -a v1.0.0 -m "message"", "git tag -a v1.0.0 -m "First course release"\ngit tag", "v1.0.0", "Tags give meaningful names to important points in repository history, such as releases.", "Choose a version for your next project release.")
    if _has(t, "diff", "log", "blame", "bisect", "debug"):
        return pack("git diff / git log / git blame / git bisect", "git diff\ngit log --oneline -5", "Changed lines and recent commits are shown.", "Git history is a debugging tool: inspect changes, narrow the time range, and identify the commit that changed behavior.", "Find the last commit that touched a lesson file.")
    return pack("git status\ngit add <file>\ngit commit -m "message"", "git status\ngit add .\ngit commit -m "Update course content"", "The working tree is staged and a commit is created.", "Git tracks repository state through working files, the staging area, and commits.", "Make one harmless change and inspect each state.")


def _bash(t):
    if _has(t, "permission", "chmod", "execute"):
        return pack("chmod u+x file", "touch script.sh\nchmod u+x script.sh\nls -l script.sh", "The owner execute permission is enabled.", "chmod changes permission bits. u+x adds execute permission for the file owner.", "Remove the permission and add it back.")
    if _has(t, "pipe", "pipeline"):
        return pack("command1 | command2", "printf '%s\\n' 'a' 'b' 'c' | grep b", "b", "A pipe sends standard output from one command to another command's standard input.", "Pipe a directory listing into grep.")
    if _has(t, "file", "directory", "filesystem", "find", "grep"):
        return pack("command [options] [arguments]", "mkdir -p lessons\nprintf 'Loops\\nFunctions\\n' > lessons/topics.txt\ngrep 'Loops' lessons/topics.txt", "Loops", "Shell commands compose small operations. Quoting, paths, exit codes, and standard streams are core Unix concepts.", "Find all .py files under a project directory.")
    return pack("command [options] [arguments]", "printf '%s\\n' 'Learning: LESSON_TOPIC'", "Learning: LESSON_TOPIC", "Shell commands accept arguments and write to standard streams. Replace the topic placeholder with the lesson concept.", "Change the command and inspect its exit code.")


def example_for(slug, title, body=""):
    """Return a concrete example chosen from the lesson's actual content."""
    s = (slug or "").lower()
    t = (str(title) + " " + str(body)).lower()

    if s in {"python", "python-course", "ai"}:
        result = _python(t)
    elif s in {"javascript", "js", "nodejs", "react"}:
        result = _javascript(t)
    elif s == "typescript":
        result = _typescript(t)
    elif s == "go":
        result = _go(t)
    elif s == "html":
        result = _html(t)
    elif s == "css":
        result = _css(t)
    elif s in {"sql", "mysql", "postgresql"} or "database" in s:
        result = _sql(t)
    elif s in {"git", "git-github"}:
        result = _git(t)
    elif s in {"bash", "bash-linux", "linux"}:
        result = _bash(t)
    else:
        result = None

    if result is None:
        # Other master tracks still get a lesson-specific example instead of a
        # shared "value = 10" fallback. The title becomes part of the runnable
        # example and the source text is mined for a useful noun when possible.
        topic = re.sub(r"[^A-Za-z0-9 ]+", " ", str(title)).strip() or "this topic"
        topic_slug = re.sub(r"[^a-z0-9]+", "_", topic.lower()).strip("_")[:32] or "topic"
        result = pack(
            "value = lesson_concept",
            f'lesson_concept = "{topic}"\nprint("{topic_slug}:", lesson_concept)\nprint("Practice this concept, then change the value.")',
            f"{topic_slug}: {topic}\nPractice this concept, then change the value.",
            f"This example is tied directly to the lesson topic '{topic}'. Identify the input, operation, and result, then replace the placeholder with a real value from the lesson.",
            f"Create a second example that demonstrates {topic} in a small project."
        )

    syntax, code, output, explanation, practice = result
    return syntax, code, output, explanation, practice


def enrich_lessons(courses):
    """Append a distinct, topic-aware teaching unit to every lesson exactly once."""
    for course in courses:
        slug = course.get("slug", "")
        for lesson in course.get("lessons", []):
            body = lesson.get("body", "")
            # Rebuild old generated units so stale generic examples cannot survive
            # after a new version of the teaching rules is deployed.
            if MARKER in body:
                body = body.split(MARKER, 1)[0].rstrip()
            title = lesson.get("title", "this topic")
            syntax, code, output, explanation, practice = example_for(slug, title, body)
            lesson["body"] = (
                body
                + "\n\n" + MARKER
                + "\n### What You Are Learning\n"
                + "This lesson is taught from its own topic. Learn the syntax, run the example, trace the result, then change it.\n\n"
                + "### Syntax\n" + syntax + "\n\n"
                + "### Example\nEXAMPLE_CODE\n" + code + "\nEND_CODE\n\n"
                + "### Output / Result\nOUTPUT\n" + output + "\nEND_OUTPUT\n\n"
                + "### How It Works\n" + explanation + "\n\n"
                + "### Change It\n" + (practice or "Change one value, rerun the example, and explain the new result.") + "\n\n"
                + "### Practice\n"
                + "Rebuild the example from memory, then make one useful variation that still demonstrates this lesson's exact concept."
            )
    return courses
