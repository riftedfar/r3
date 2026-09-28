"""Topic-aware practical teaching layer for every lesson."""

MARKER = "## PRACTICAL EXAMPLE"


def pack(syntax, code, output, explanation):
    return syntax, code, output, explanation


def example_for(slug, title):
    s = (slug or "").lower()
    t = (title or "").lower()

    # Python is the main course and also powers many AI examples.
    if s in {"python", "python-course", "ai"}:
        if "print" in t or "output" in t:
            return pack("print(value)",
                        'print("Hello")\nname = "Maya"\nprint("Hello,", name)',
                        "Hello\nHello, Maya",
                        "print sends values to standard output. Strings can be literal values or values stored in variables.")
        if any(x in t for x in ("variable", "assignment", "constant")):
            return pack("name = value",
                        'name = "Maya"\nage = 17\nprint(name, age)',
                        "Maya 17",
                        "A name is bound to an object. Assignment with = creates or changes that binding.")
        if any(x in t for x in ("string", "text", "f-string", "format")):
            return pack('f"Hello {name}"',
                        'name = "Python"\nprint(name.upper())\nprint(f"Hello, {name}!")',
                        "PYTHON\nHello, Python!",
                        "Strings are text sequences. Methods such as upper transform them, while f-strings insert expressions into text.")
        if any(x in t for x in ("boolean", "bool", "truth")):
            return pack("condition and condition",
                        'age = 16\nhas_ticket = True\nprint(age >= 13 and has_ticket)',
                        "True",
                        "Boolean expressions produce True or False. and, or, and not combine Boolean values.")
        if any(x in t for x in ("comparison", "equal", "greater", "less")):
            return pack("left == right",
                        'score = 82\nprint(score >= 80)\nprint(score == 100)',
                        "True\nFalse",
                        "Comparison operators compare values and return a Boolean result.")
        if "list" in t:
            return pack("items = [value1, value2]",
                        'items = ["a", "b"]\nitems.append("c")\nprint(items[0])\nprint(items)',
                        "a\n['a', 'b', 'c']",
                        "Lists are ordered and mutable. append adds an item and indexing reads a position.")
        if "tuple" in t:
            return pack("(value1, value2)",
                        "point = (4, 7)\nprint(point[0])",
                        "4",
                        "A tuple is an ordered sequence commonly used for a fixed group of values.")
        if "set" in t:
            return pack("{value1, value2}",
                        "numbers = {1, 2, 2, 3}\nprint(sorted(numbers))",
                        "[1, 2, 3]",
                        "A set stores unique values, so the duplicate 2 is kept only once.")
        if any(x in t for x in ("dictionary", "dict", "mapping")):
            return pack("{key: value}",
                        'user = {"name": "Maya", "score": 90}\nprint(user["name"])\nuser["score"] += 5\nprint(user["score"])',
                        "Maya\n95",
                        "A dictionary maps keys to values. Lookup uses a key and assignment can update its value.")
        if any(x in t for x in ("conditional", "if ", "decision", "branch", "match")):
            return pack("if condition:\n    ...\nelse:\n    ...",
                        'score = 82\nif score >= 80:\n    print("pass")\nelse:\n    print("retry")',
                        "pass",
                        "Python evaluates the condition first and executes only the matching indented branch.")
        if any(x in t for x in ("loop", "iteration", "for ", "while")):
            return pack("for item in iterable:",
                        'for level in range(1, 4):\n    print("Level", level)',
                        "Level 1\nLevel 2\nLevel 3",
                        "The loop takes values from an iterable. range(1, 4) produces 1, 2, and 3.")
        if any(x in t for x in ("function", "def ", "parameter", "return")):
            return pack("def name(parameter):",
                        'def greet(name):\n    return "Hello, " + name\n\nprint(greet("Maya"))',
                        "Hello, Maya",
                        "def creates a function. Parameters receive input and return sends a result back to the caller.")
        if "lambda" in t:
            return pack("lambda parameter: expression",
                        "double = lambda x: x * 2\nprint(double(5))",
                        "10",
                        "A lambda creates a small anonymous function containing one expression.")
        if any(x in t for x in ("class", "object-oriented", "oop", "inheritance")):
            return pack("class Name:",
                        'class Player:\n    def __init__(self, name):\n        self.name = name\n\nplayer = Player("Rex")\nprint(player.name)',
                        "Rex",
                        "A class defines a type. Creating an instance calls its initializer, which stores state on self.")
        if any(x in t for x in ("exception", "error handling", "try", "raise", "resilience")):
            return pack("try:\n    risky_operation()\nexcept ErrorType:\n    recover()",
                        'try:\n    number = int("abc")\nexcept ValueError:\n    print("invalid number")',
                        "invalid number",
                        "try runs code that may fail; except handles a matching exception. Do not hide unrelated errors.")
        if any(x in t for x in ("file", "filesystem", "path")):
            return pack("Path(path).read_text()",
                        'from pathlib import Path\npath = Path("demo.txt")\npath.write_text("Hello")\nprint(path.read_text())',
                        "Hello",
                        "A Path represents a filesystem location. The example writes text and reads it back.")
        if any(x in t for x in ("json", "serialization", "deserialize")):
            return pack("json.dumps(value) / json.loads(text)",
                        'import json\ndata = {"name": "Maya", "score": 95}\ntext = json.dumps(data)\nprint(json.loads(text)["score"])',
                        "95",
                        "dumps converts Python data to JSON text; loads converts JSON text back to Python data.")
        if "comprehension" in t:
            return pack("[expression for item in iterable if condition]",
                        "squares = [n * n for n in range(5)]\nprint(squares)",
                        "[0, 1, 4, 9, 16]",
                        "A comprehension builds a collection from an iterable using a compact expression.")
        if any(x in t for x in ("generator", "yield")):
            return pack("yield value",
                        'def countdown(n):\n    while n:\n        yield n\n        n -= 1\nprint(list(countdown(3)))',
                        "[3, 2, 1]",
                        "yield pauses a generator and produces values lazily instead of creating the whole sequence immediately.")
        if "decorator" in t:
            return pack("@decorator",
                        'def log_call(fn):\n    def wrapper():\n        print("calling")\n        return fn()\n    return wrapper\n\n@log_call\ndef hello():\n    print("hello")\nhello()',
                        "calling\nhello",
                        "A decorator receives a callable and returns a wrapped callable with additional behavior.")
        if any(x in t for x in ("asyncio", "async", "await", "coroutine")):
            return pack("async def name():\n    await operation()",
                        'import asyncio\n\nasync def main():\n    await asyncio.sleep(0)\n    print("done")\n\nasyncio.run(main())',
                        "done",
                        "async def creates a coroutine function and await pauses it while other asynchronous work can run.")
        if any(x in t for x in ("type hint", "typing", "annotation", "protocol", "generic")):
            return pack("def add(a: int, b: int) -> int:",
                        'def add(a: int, b: int) -> int:\n    return a + b\nprint(add(2, 3))',
                        "5",
                        "Type annotations document expected types and help static analysis; normal Python does not enforce them automatically.")
        if "enum" in t:
            return pack("class Status(Enum):",
                        'from enum import Enum\nclass Status(Enum):\n    READY = "ready"\nprint(Status.READY.value)',
                        "ready",
                        "An Enum represents a fixed set of named choices.")
        if any(x in t for x in ("test", "pytest", "unit test")):
            return pack("assert actual == expected",
                        'def add(a, b):\n    return a + b\n\nassert add(2, 3) == 5\nprint("passed")',
                        "passed",
                        "A test states expected behavior. A failing assertion identifies a regression.")
        if any(x in t for x in ("sqlite", "database", "sql", "transaction")):
            return pack("connection.execute(sql, parameters)",
                        'import sqlite3\ncon = sqlite3.connect(":memory:")\ncon.execute("CREATE TABLE users (name TEXT)")\ncon.execute("INSERT INTO users VALUES (?)", ("Maya",))\nprint(con.execute("SELECT name FROM users").fetchone()[0])',
                        "Maya",
                        "Database code should parameterize values instead of concatenating untrusted input into SQL.")
        return pack("def demo(value):\n    ...",
                    'def demo(value):\n    print("Value:", value)\n\ndemo(10)',
                    "Value: 10",
                    "Start with the smallest runnable version of the concept. Change one input, rerun it, and observe exactly what changed.")

    if s in {"javascript", "js", "nodejs", "react"}:
        if "function" in t or "method" in t:
            return pack("function name(parameter) { return value; }",
                        'function greet(name) { return "Hello, " + name; }\nconsole.log(greet("Maya"));',
                        "Hello, Maya",
                        "Functions package reusable behavior. Parameters receive input and return provides the result.")
        if any(x in t for x in ("array", "list")):
            return pack("const items = [value1, value2];",
                        'const items = ["a", "b"];\nitems.push("c");\nconsole.log(items);',
                        '["a","b","c"]',
                        "Arrays are ordered collections; push adds an element at the end.")
        if any(x in t for x in ("async", "promise", "await")):
            return pack("async function name() { await promise; }",
                        'async function main() {\n  const value = await Promise.resolve(42);\n  console.log(value);\n}\nmain();',
                        "42",
                        "await pauses an async function until a Promise settles, then resumes with its result.")
        return pack("const name = value;",
                    'const name = "JavaScript";\nconsole.log(name);',
                    "JavaScript",
                    "const creates a binding that cannot be reassigned. console.log displays the value.")

    if s == "typescript":
        if any(x in t for x in ("generic",)):
            return pack("function first<T>(items: T[]): T",
                        'function first<T>(items: T[]): T { return items[0]; }\nconsole.log(first(["a", "b"]));',
                        "a",
                        "T preserves the element type so one function can work safely with many types.")
        if "interface" in t:
            return pack("interface User { name: string; age: number }",
                        'interface User { name: string; age: number }\nconst user: User = { name: "Maya", age: 17 };\nconsole.log(user.name);',
                        "Maya",
                        "An interface describes an object shape at compile time; it does not validate runtime JSON.")
        if any(x in t for x in ("union", "narrow")):
            return pack("let value: string | number",
                        'function show(v: string | number) {\n  if (typeof v === "string") console.log(v.toUpperCase());\n  else console.log(v.toFixed(2));\n}\nshow("go");',
                        "GO",
                        "A union permits several types; a runtime check narrows the value before type-specific operations.")
        return pack("const name: string = value;",
                    'const name: string = "TypeScript";\nconsole.log(name);',
                    "TypeScript",
                    "Type annotations add compile-time information. They are removed when TypeScript is compiled to JavaScript.")

    if s == "go":
        if "function" in t: return pack("func add(a, b int) int", 'package main\nimport "fmt"\nfunc add(a, b int) int { return a + b }\nfunc main() { fmt.Println(add(2, 3)) }', "5", "A Go function declares parameters and a return type explicitly.")
        if "slice" in t: return pack("items := []string{...}", 'package main\nimport "fmt"\nfunc main() { items := []string{"a", "b"}; items = append(items, "c"); fmt.Println(items) }', "[a b c]", "Slices are flexible ordered collections; append adds an element.")
        if "map" in t: return pack("map[Key]Value{...}", 'package main\nimport "fmt"\nfunc main() { scores := map[string]int{"Maya": 95}; fmt.Println(scores["Maya"]) }', "95", "Maps associate keys with values for lookup.")
        return pack("package main\nfunc main() { ... }", 'package main\nimport "fmt"\nfunc main() { fmt.Println("Hello, Go!") }', "Hello, Go!", "Go programs start from package main and execute func main.")

    if s == "html":
        if "form" in t: return pack("<form>...</form>", '<form>\n  <label>Email <input type="email" required></label>\n  <button type="submit">Send</button>\n</form>', "A labeled email field and submit button.", "Labels identify controls; input types and required add native browser constraints.")
        if "image" in t: return pack('<img src="..." alt="...">', '<img src="cat.jpg" alt="A sleeping cat">', "The image is displayed.", "src identifies the resource and alt provides a text alternative.")
        if "link" in t: return pack('<a href="URL">text</a>', '<a href="/courses">View courses</a>', "A clickable link.", "href supplies the destination and the anchor text explains the link.")
        return pack("<element attribute=\"value\">content</element>", '<main>\n  <h1>My Course</h1>\n  <p>Learn by building.</p>\n</main>', "A semantic main section.", "HTML elements describe structure and meaning; nesting expresses relationships between content.")

    if s == "css":
        if "flex" in t: return pack("selector { display: flex; }", ".nav {\n  display: flex;\n  gap: 16px;\n  align-items: center;\n}", "Items align in a flexible row.", "Flexbox lays children along a main axis and provides alignment and spacing controls.")
        if "grid" in t: return pack("selector { display: grid; }", ".cards {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  gap: 16px;\n}", "Three flexible columns.", "Grid creates rows and columns; fr units divide available space.")
        if "responsive" in t or "media" in t: return pack("@media (max-width: 700px) { ... }", "@media (max-width: 700px) {\n  .cards { grid-template-columns: 1fr; }\n}", "Cards become one column.", "A media query applies rules only when its viewport condition matches.")
        if "variable" in t or "custom propert" in t: return pack("--name: value; / var(--name)", ":root { --space: 16px; }\n.card { padding: var(--space); }", "The card gets 16px padding.", "Custom properties store reusable values and var() reads them.")
        return pack(".selector { property: value; }", ".card {\n  padding: 20px;\n  border-radius: 12px;\n}", "The card gets padding and rounded corners.", "A selector chooses elements and declarations set their CSS properties.")

    if s in {"sql", "mysql", "postgresql"} or "database" in s:
        if "insert" in t: return pack("INSERT INTO table (columns) VALUES (values);", "INSERT INTO students (name, score) VALUES ('Maya', 95);", "One row inserted.", "INSERT creates a row in a table.")
        if "update" in t: return pack("UPDATE table SET column = value WHERE condition;", "UPDATE students SET score = 100 WHERE name = 'Maya';", "Matching rows updated.", "UPDATE changes existing rows; WHERE limits which rows are affected.")
        if "delete" in t: return pack("DELETE FROM table WHERE condition;", "DELETE FROM students WHERE score < 50;", "Matching rows deleted.", "DELETE removes rows; always verify the WHERE condition.")
        if "join" in t: return pack("SELECT ... FROM a JOIN b ON ...;", "SELECT users.name, orders.total FROM users JOIN orders ON orders.user_id = users.id;", "Related rows are combined.", "JOIN combines rows from related tables using a matching condition.")
        return pack("SELECT columns FROM table WHERE condition;", "SELECT name, score FROM students WHERE score >= 80 ORDER BY score DESC;", "Maya | 95\nSam | 88", "SELECT chooses columns, WHERE filters rows, and ORDER BY controls result order.")

    if s == "git":
        if "branch" in t: return pack("git switch -c <branch>", "git switch -c feature/login\ngit status", "A new branch is created and selected.", "Branches are movable names pointing to commit history.")
        if "commit" in t: return pack("git add <files>\ngit commit -m \"message\"", 'git add .\ngit commit -m "Add lesson example"', "A commit is created.", "git add stages changes; git commit records the staged snapshot.")
        if "merge" in t: return pack("git switch main\ngit merge <branch>", "git switch main\ngit merge feature/login", "The feature history is merged.", "merge combines histories and may require conflict resolution.")
        return pack("git status / git log", "git status\ngit log --oneline -5", "Working-tree state and recent commits.", "status shows changes; log shows commit history.")

    if s in {"bash-linux", "bash"}:
        if "permission" in t: return pack("chmod MODE file", "touch script.sh\nchmod u+x script.sh\nls -l script.sh", "The owner execute permission is enabled.", "chmod changes permission bits; u+x adds execute permission for the owner.")
        if "pipe" in t: return pack("command1 | command2", "printf '%s\\n' 'a\\nb\\nc' | grep b", "b", "A pipe sends standard output from one command to standard input of another.")
        return pack("command [options] [arguments]", "printf '%s\\n' 'Hello, Linux!'", "Hello, Linux!", "Shell commands receive arguments and write output. Quoting and exit codes matter.")

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
    }
    if s in starters:
        code, output = starters[s]
        return pack("Use the language syntax for this concept.", code, output,
                    "Start from the smallest runnable form, then change the part connected to the lesson topic and observe the result.")

    return pack("Input -> operation -> output",
                "# Start with one small example for this topic.\nvalue = 10\nprint(value)",
                "10",
                "Break the lesson into one concrete input, one operation, and one observable result. Then change one assumption and test again.")


def enrich_lessons(courses):
    """Append a practical teaching unit to every lesson exactly once."""
    for course in courses:
        slug = course.get("slug", "")
        for lesson in course.get("lessons", []):
            body = lesson.get("body", "")
            if MARKER in body:
                continue
            title = lesson.get("title", "this topic")
            syntax, code, output, explanation = example_for(slug, title)
            lesson["body"] = (
                body.rstrip()
                + "\n\n" + MARKER
                + "\n### What You Are Learning\n"
                + "This turns " + title + " into a concrete skill: understand the syntax, run the example, trace the result, then change it.\n\n"
                + "### Syntax\n" + syntax + "\n\n"
                + "### Example\nEXAMPLE_CODE\n" + code + "\nEND_CODE\n\n"
                + "### Output / Result\nOUTPUT\n" + output + "\nEND_OUTPUT\n\n"
                + "### How It Works\n" + explanation + "\n\n"
                + "1. Read the syntax before copying the example.\n"
                + "2. Identify the input, operation, and result.\n"
                + "3. Change one value or line and predict the new result.\n"
                + "4. Run it and explain why the result changed.\n\n"
                + "### Practice\n"
                + "Rebuild the " + title + " example from memory, then make one useful variation of your own."
            )
    return courses
