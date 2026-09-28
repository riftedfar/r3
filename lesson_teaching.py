"""Practical teaching layer for every course lesson."""\nMARKER = "## PRACTICAL EXAMPLE"\n\n
def _topic_pack(slug, title):
    """Return syntax, runnable example, output, and a topic explanation."""
    s = (slug or "").lower()
    t = (title or "").lower()

    # Universal concepts first: these make advanced/master lessons concrete.
    if any(x in t for x in ("print", "output", "console")):
        return ("print(value)" if "python" in s else "output(value)",
                'print("Hello")', "Hello",
                "The statement sends a value to the program's output. Change the value and run it again.")
    if any(x in t for x in ("variable", "assignment", "constant")):
        if s in ("python", "ai"):
            return ("name = value", 'name = "Maya"\nage = 17\nprint(name, age)', "Maya 17",
                    "The name is bound to a value. Reassignment changes what that name refers to.")
        return ("name = value", 'name = "Maya"\nprint(name)', "Maya",
                "A variable gives a value a reusable name. The exact declaration syntax depends on the language.")
    if any(x in t for x in ("function", "method", "procedure")):
        if s in ("python", "ai"):
            return ("def name(parameter):", 'def greet(name):\n    return "Hello, " + name\n\nprint(greet("Maya"))', "Hello, Maya",
                    "def creates a function, parameters receive input, and return sends a result to the caller.")
        if s in ("javascript", "js", "nodejs", "react"):
            return ("function name(parameter) { return value; }", 'function greet(name) { return "Hello, " + name; }\nconsole.log(greet("Maya"));', "Hello, Maya",
                    "A function groups reusable behavior; parameters receive inputs and return provides the result.")
        if s == "typescript":
            return ("function name(parameter: Type): ReturnType", 'function add(a: number, b: number): number { return a + b; }\nconsole.log(add(2, 3));', "5",
                    "TypeScript adds a compile-time contract to the function parameters and return value.")
        return ("name(parameters) -> result", "# Define the function using this language's syntax.\n# Call it with a small input.", "A result is produced",
                "A function packages a repeatable operation behind a name. Learn the parameter and return-value rules of the language.")
    if any(x in t for x in ("condition", "if", "switch", "branch", "decision")):
        if s in ("python", "ai"):
            return ("if condition:\n    ...\nelse:\n    ...", 'score = 82\nif score >= 80:\n    print("pass")\nelse:\n    print("retry")', "pass",
                    "The condition is evaluated first; only the matching indented branch runs.")
        return ("if (condition) { ... }", 'score = 82;\nif (score >= 80) {\n  console.log("pass");\n} else {\n  console.log("retry");\n}', "pass",
                "A conditional selects one path based on a Boolean expression. Adapt the syntax to the lesson's language.")
    if any(x in t for x in ("loop", "iteration", "for ", "while", "repeat")):
        if s in ("python", "ai"):
            return ("for item in iterable:", 'for level in range(1, 4):\n    print("Level", level)', "Level 1\nLevel 2\nLevel 3",
                    "The loop takes one item at a time from an iterable and executes the body for each item.")
        if s in ("javascript", "js", "typescript", "nodejs"):
            return ("for (const item of items) { ... }", 'for (const level of [1, 2, 3]) {\n  console.log("Level", level);\n}', "Level 1\nLevel 2\nLevel 3",
                    "The loop visits each value in the collection and runs the body once per value.")
        return ("for each item in collection", "# Use the language's loop syntax here.\n# Change the collection and observe the number of iterations.", "One result per item",
                "A loop repeats a block according to a collection, condition, or counter.")
    if any(x in t for x in ("class", "object-oriented", "oop", "inheritance", "interface", "struct")):
        if s in ("python", "ai"):
            return ("class Name:\n    ...", 'class Player:\n    def __init__(self, name):\n        self.name = name\n\nplayer = Player("Rex")\nprint(player.name)', "Rex",
                    "A class defines a type; constructing it creates an object whose state can be stored on the instance.")
        if s == "typescript":
            return ("interface User { name: string; age: number }", 'interface User { name: string; age: number }\nconst user: User = { name: "Maya", age: 17 };\nconsole.log(user.name);', "Maya",
                    "An interface describes an object shape at compile time; it does not validate external data at runtime.")
        return ("type/class Name { fields; methods; }", "# Define one small type with one field.\n# Create an instance and read the field.", "The field value is printed",
                "Types, classes, structs, or interfaces group related data and behavior according to the language's model.")
    if any(x in t for x in ("error", "exception", "failure", "resilience")):
        if s in ("python", "ai"):
            return ("try:\n    risky_operation()\nexcept ErrorType:\n    recover()", 'try:\n    number = int("abc")\nexcept ValueError:\n    print("invalid number")', "invalid number",
                    "The risky operation can raise an exception; a matching handler decides how the program recovers.")
        return ("try operation; handle the expected failure", "# Trigger one expected failure.\n# Handle it explicitly and keep unrelated failures visible.", "Expected failure handled",
                "Reliable code distinguishes expected failures from programming bugs and handles each at the correct boundary.")
    if any(x in t for x in ("test", "testing", "pytest", "unit test")):
        return ("assert actual == expected", 'def add(a, b):\n    return a + b\n\nassert add(2, 3) == 5\nprint("passed")', "passed",
                "A test states an expected behavior. If the assertion is false, the test reports a regression.")
    if any(x in t for x in ("json", "serialization", "deserialize")):
        if s in ("python", "ai"):
            return ("json.dumps(value) / json.loads(text)", 'import json\ndata = {"name": "Maya", "score": 95}\ntext = json.dumps(data)\nprint(json.loads(text)["score"])', "95",
                    "Serialization converts in-memory data into a transferable representation; deserialization reconstructs usable data.")
        return ("encode(value) / decode(text)", '{"name":"Maya","score":95}', "A structured object is encoded as data",
                "Serialization is a data boundary. Validate decoded data before trusting it.")
    if any(x in t for x in ("database", "sqlite", "sql", "query", "transaction", "repository")):
        return ("SELECT columns FROM table WHERE condition;", "SELECT name, score FROM students WHERE score >= 80 ORDER BY score DESC;", "Maya | 95\nSam | 88",
                "A query selects rows from structured data. Parameters should be used for untrusted input and transactions should group related writes.")
    if any(x in t for x in ("http", "api", "request", "network", "web service")):
        return ("GET /resource", 'GET /courses/3\nAccept: application/json', "200 OK\n{course data}",
                "An HTTP client sends a request; the server returns a status, headers, and a body. Production clients need timeouts and error handling.")
    if any(x in t for x in ("async", "concurrency", "coroutine", "thread", "goroutine", "parallel", "worker")):
        return ("start task -> wait/coordinate -> collect result", 'import asyncio\n\nasync def work():\n    await asyncio.sleep(0)\n    return "done"\n\nprint(asyncio.run(work()))', "done",
                "Asynchronous or concurrent work lets independent operations overlap or coordinate. Choose the model based on whether the work is I/O-bound or CPU-bound.")
    if any(x in t for x in ("list", "array", "slice", "collection", "vector")):
        if s in ("python", "ai"):
            return ("items = [value1, value2]", 'items = ["a", "b"]\nitems.append("c")\nprint(items)', "['a', 'b', 'c']",
                    "The collection stores ordered values; append adds a new item and indexing can read a particular position.")
        return ("items = [value1, value2]", 'items = ["a", "b"]\nitems.append("c")\nprint(items)', "a, b, c",
                "A collection stores multiple values. The exact operations differ by language, but the core idea is indexing and updating elements.")
    if any(x in t for x in ("map", "dictionary", "hash", "record")):
        return ("key -> value", 'scores = {"Maya": 95}\nprint(scores["Maya"])', "95",
                "A mapping associates a key with a value, allowing direct lookup by that key.")
    if any(x in t for x in ("type", "generic", "typing", "null safety", "ownership", "borrow", "lifetime")):
        if s == "typescript":
            return ("function first<T>(items: T[]): T", 'function first<T>(items: T[]): T { return items[0]; }\nconsole.log(first(["a", "b"]));', "a",
                    "The type parameter T preserves the relationship between the input element type and the returned element.")
        if s in ("python", "ai"):
            return ("def add(a: int, b: int) -> int:", 'def add(a: int, b: int) -> int:\n    return a + b\nprint(add(2, 3))', "5",
                    "Type annotations document expected types and help static analysis; normal Python does not enforce them automatically.")
        return ("value: Type", "# Declare one value using the language's type system.\n# Then pass it to the operation from this lesson.", "A typed value is produced",
                "A type system constrains or documents which values an operation can accept. Check whether the rule is compile-time or runtime.")
    if any(x in t for x in ("file", "filesystem", "path", "stream")):
        if s in ("python", "ai"):
            return ("Path(path).read_text()", 'from pathlib import Path\npath = Path("demo.txt")\npath.write_text("Hello")\nprint(path.read_text())', "Hello",
                    "A path identifies a filesystem location; the example writes text and reads it back.")
        return ("open(path) -> read/write -> close", "open demo.txt\nwrite: Hello\nread: Hello", "Hello",
                "File operations have a resource lifetime: open, perform the operation, then close or use an automatic resource manager.")
    if any(x in t for x in ("git", "branch", "commit", "merge", "version control")):
        return ("git add .\ngit commit -m \"message\"", 'git add .\ngit commit -m "Add lesson example"', "A commit is created",
                "Git stages changes and records them as commits. Branches are movable names pointing to commit history.")
    if any(x in t for x in ("flex", "grid", "responsive", "selector", "box model", "css", "styling")):
        return (".selector { property: value; }", ".cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }",
                "Three flexible columns are created.",
                "CSS selects elements and assigns declarations. Layout systems such as Grid and Flexbox determine how children are arranged.")
    if any(x in t for x in ("html", "semantic", "accessib", "form", "link", "image", "table", "markup")):
        return ("<element attribute=\"value\">content</element>", '<form>\n  <label>Email <input type="email" required></label>\n  <button type="submit">Send</button>\n</form>',
                "A labeled email field and submit button appear.",
                "HTML elements describe document structure and meaning; attributes add information or behavior. Semantic elements improve accessibility.")
    if any(x in t for x in ("docker", "container", "image", "compose")):
        return ("docker build -t name .", "docker build -t course-demo .\ndocker run --rm course-demo",
                "An image is built and a container runs it.",
                "An image packages an application and its filesystem/configuration; a container is a running instance of that image.")
    if any(x in t for x in ("linux", "bash", "shell", "terminal", "command", "permission")):
        return ("command [options] [arguments]", "printf '%s\\n' 'Hello, Linux!'", "Hello, Linux!",
                "A shell command receives arguments and writes output. Quoting, exit codes, permissions, and pipelines are core shell concepts.")
    # Course-specific starter fallback: still concrete, but never pretends a generic snippet is a full lesson.
    starters = {
        "java": ('class Main { public static void main(String[] args) { System.out.println("Hello, Java!"); } }', "Hello, Java!"),
        "kotlin": ('fun main() { println("Hello, Kotlin!") }', "Hello, Kotlin!"),
        "cpp": ('#include <iostream>\nint main() { std::cout << "Hello, C++!\\n"; }', "Hello, C++!"),
        "csharp": ('using System;\nclass Program { static void Main() { Console.WriteLine("Hello, C#!"); } }', "Hello, C#!"),
        "rust": ('fn main() { println!("Hello, Rust!"); }', "Hello, Rust!"),
        "swift": ('print("Hello, Swift!")', "Hello, Swift!"),
        "dart": ('void main() { print("Hello, Dart!"); }', "Hello, Dart!"),
        "php": ('<?php echo "Hello, PHP!"; ?>', "Hello, PHP!"),
        "ruby": ('puts "Hello, Ruby!"', "Hello, Ruby!"),
        "r": ('name <- "R"\nprint(paste("Hello,", name))', "Hello, R"),
        "go": ('package main\nimport "fmt"\nfunc main() { fmt.Println("Hello, Go!") }', "Hello, Go!"),
    }
    if s in starters:
        code, output = starters[s]
        return ("Use the language syntax for " + title + ".", code, output,
                "This is a minimal runnable starting point. Change one part related to the lesson and observe the result.")
    return ("Input -> operation -> output", "# Start with one small example for this topic.\nvalue = 10\nprint(value)", "10",
            "Break the concept into one input, one operation, and one observable result. Then change one assumption and test again.")


def example_for(slug, title):
    pack = _topic_pack(slug, title)
    return pack[1], pack[2]


def enrich_lessons(courses):\n    for course in courses:\n        for lesson in course.get("lessons", []):\n            body = lesson.get("body", "")\n            if MARKER in body: continue\n            code, output = example_for(course.get("slug", "python"), lesson.get("title", ""))\n            lesson["body"] = (\n                body.rstrip() + "\n\n" + MARKER + "\n" +\n                "### Syntax\nLearn the pattern first; then change it. The syntax is not something to memorize blindly.\n\n" +\n                "### Example\nEXAMPLE_CODE\n" + code + "\nEND_CODE\n\n" +\n                "### Output / Result\nOUTPUT\n" + output + "\nEND_OUTPUT\n\n" +\n                "### How It Works\n1. Read each line before running it.\n2. Identify the input, operation, and output.\n3. Predict what changes if you edit one value.\n4. Run it and explain the result in your own words.\n\n" +\n                "### Practice\nRewrite the example for a different value or use case, then create one small example without copying the original."\n            )\n    return courses