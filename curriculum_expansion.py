"""Curriculum expansion pack for LearnPython.

Keeps the original lesson files intact while adding deeper modules and new tracks.
"""

def _lesson(title, focus, practice, mistake, level):
    return {
        "title": title,
        "body": (
            f"Chapter: {title}\n\n"
            f"In Plain English\n{focus}\n\n"
            "Why This Matters\n"
            f"{focus} This is the kind of idea that becomes useful when you build real software.\n\n"
            "Try It Yourself\n"
            f"{practice}\n\n"
            "Common Mistake\n"
            f"{mistake}\n\n"
            "Level Up\n"
            f"{level}"
        )
    }

def _append(slug, rows, courses):
    courses[slug]["lessons"].extend(_lesson(*row) for row in rows)

def extend_courses(courses):
    list_mode = isinstance(courses, list)
    if list_mode:
        courses = {c["slug"]: c for c in courses}
    _append("ai", [
        ("Data Cleaning & Preprocessing","Real datasets contain missing, duplicated, inconsistent, and noisy values. Cleaning is the process of deciding what those values mean and transforming data deliberately.","Take a messy table and write down five cleaning decisions before touching the data.","Deleting every unusual row instead of understanding why it is unusual.","Document each transformation and test whether it changes the distribution unexpectedly."),
        ("Features & Representations","Models need useful representations of information. A feature can be a raw value, a transformed value, or a representation created from several inputs.","Design five features for a house-price predictor and label which are available before prediction.","Using information that would only exist after the prediction happens.","Separate raw fields, derived features, and the target variable."),
        ("Supervised vs Unsupervised Learning","Supervised learning uses examples with targets; unsupervised learning searches for structure without target labels.","Classify five imaginary ML tasks as supervised or unsupervised and explain why.","Assuming clustering has a single correct answer like classification.","Describe what signal exists when labels are unavailable."),
        ("Decision Trees","A decision tree repeatedly splits data using conditions until it reaches useful predictions. Deep trees can memorize training examples.","Draw a small tree that classifies three types of users.","Making the tree deeper simply because it can be.","Compare a shallow tree with a deep tree and discuss overfitting."),
        ("Nearest Neighbors","A nearest-neighbor model predicts using examples that are close to a new example in feature space.","Choose the nearest examples for a new point on paper.","Ignoring feature scale when distance is calculated.","Normalize features before comparing distances."),
        ("Precision, Recall & F1","Precision measures how many predicted positives were correct; recall measures how many real positives were found. F1 combines them.","Choose an appropriate metric for spam, fraud, and a safety-screening example.","Using accuracy as the only metric for every problem.","Explain which kind of mistake is more expensive in each scenario."),
        ("Confusion Matrices","A confusion matrix counts true positives, true negatives, false positives, and false negatives.","Build a 2x2 confusion matrix from ten imaginary predictions.","Swapping the meaning of positive and negative.","Calculate precision and recall from your matrix."),
        ("Train, Validation & Test","Training fits a model, validation helps tune choices, and a final test set estimates performance on unseen data.","Design a split for a small dataset and explain what each split is for.","Repeatedly tuning against the final test set.","Keep the final test set untouched until the end."),
        ("Hyperparameters","Hyperparameters are choices made outside the learned parameters, such as tree depth or learning rate.","List three hyperparameters for a model and predict what changing each might do.","Calling every model setting a learned weight.","Change one hyperparameter at a time in an experiment."),
        ("Feature Leakage","Leakage happens when training data contains information that would not actually be available when making the prediction.","Find the leaked feature in a hypothetical future-event prediction dataset.","Using future information because it makes validation accuracy look better.","Ask exactly when every feature becomes available."),
        ("Prompt Engineering","Useful prompts specify the task, context, constraints, examples, and desired output format.","Rewrite a vague request into a structured prompt and test it against three edge cases.","Assuming longer prompts are automatically better.","Keep only instructions that measurably improve the result."),
        ("RAG Systems","Retrieval-augmented generation retrieves relevant source material and gives it to a generative model at runtime.","Design a course Q&A system using document chunks and retrieval.","Stuffing an entire knowledge base into every prompt.","Evaluate retrieval quality separately from generation quality."),
        ("AI Evaluation","A serious AI system needs repeatable test cases and failure categories rather than one impressive demo.","Create ten tests for an AI study assistant and classify possible failures.","Judging the system only from normal questions.","Include ambiguous, adversarial, and out-of-domain inputs."),
        ("Model Safety Boundaries","Models can propose actions, but authorization and validation should live outside the model.","Design approval checks for an assistant that can send messages or modify files.","Allowing model output to directly trigger privileged actions.","Put validation and permission checks between the model and every sensitive tool."),
        ("AI Product Architecture","An AI product can contain UI, API, model, retrieval, storage, logging, and evaluation components.","Draw a small architecture for an AI study helper.","Putting every responsibility into one giant endpoint.","Give each component a clear input, output, and failure path."),
        ("AI Project Review","A final review should examine accuracy, privacy, cost, security, and failure behavior.","Audit a fictional AI product against those five categories.","Checking only whether the model produces an answer.","Write a launch checklist with measurable tests.")
    ], courses)

    _append("go", [
        ("Pointers","Pointers hold addresses and let functions work with the original value when mutation is appropriate.","Write a function that updates a struct through a pointer.","Using pointers everywhere without a reason.","Compare value and pointer receivers."),
        ("Methods","Methods attach behavior to named types and can use value or pointer receivers.","Give a Player type methods for damage and healing.","Turning every helper into a method.","Keep behavior on a type when it improves the domain model."),
        ("Packages","Packages divide a Go program into meaningful responsibilities.","Split a small application into model and service packages.","Creating tiny packages with no useful boundary.","Name packages after their responsibility."),
        ("Go Modules","go.mod records the module path and dependencies for a project.","Initialize a module and inspect its dependency information.","Copying a module file from another project blindly.","Understand the module path before importing your own packages."),
        ("Testing","The standard testing package supports focused unit tests and table-driven test cases.","Write tests for normal, boundary, and invalid inputs.","Testing only the easiest example.","Make edge cases first-class test cases."),
        ("JSON","encoding/json converts Go values to and from JSON used by APIs and files.","Marshal a struct and unmarshal it back.","Ignoring malformed JSON errors.","Check decoding errors before using the result."),
        ("HTTP Clients","net/http lets Go programs call web services and inspect responses.","Design a GET request that checks status and closes its response body.","Ignoring network errors or response cleanup.","Set timeouts and handle non-success status codes."),
        ("HTTP Servers","Go's standard library can serve routes and JSON without a large framework.","Create a health endpoint and a JSON endpoint.","Doing every piece of business logic inside the handler.","Separate validation, business logic, and response formatting."),
        ("Context","context.Context carries cancellation, deadlines, and request-scoped values through work.","Pass a context into a simulated slow operation.","Using context as global mutable state.","Propagate cancellation to downstream work."),
        ("Concurrency Patterns","Worker pools, fan-out, fan-in, and bounded concurrency are reusable patterns for parallel work.","Sketch a worker pool for processing jobs.","Launching unlimited goroutines for untrusted input.","Bound concurrency and collect failures explicitly."),
        ("Mutexes & Shared State","A mutex protects shared mutable state when multiple goroutines can access it.","Protect a shared counter from concurrent writes.","Assuming concurrent writes are automatically safe.","Identify the critical section before adding synchronization."),
        ("Benchmarks & Profiling","Performance work should be driven by measurements rather than guesses.","Compare two implementations with a benchmark plan.","Optimizing before identifying a bottleneck.","Measure first, then change one thing."),
        ("Project Structure","A Go project can separate commands, internal packages, domain code, and reusable libraries.","Sketch the structure of a medium-sized CLI.","Copying an enterprise layout into a tiny script.","Keep the architecture proportional to the project."),
        ("CLI Design","Good command-line tools have predictable arguments, help text, errors, and exit behavior.","Design commands for a task manager.","Making every option a confusing positional argument.","Write examples a new user can copy."),
        ("Production Checklist","Production Go services need configuration, logging, health checks, graceful shutdown, and reproducible builds.","Create a release checklist for a small service.","Hard-coding secrets or assuming local configuration exists.","Separate configuration, observability, and shutdown concerns.")
    ], courses)

    _append("typescript", [
        ("Literal Types & Discriminated Unions","Literal types restrict values to known choices, while discriminated unions make application states explicit.","Create loading, success, and error states with a discriminant.","Using broad strings for a fixed set of states.","Make illegal states difficult to represent."),
        ("Readonly & Immutability","Readonly types express values that should not be changed through a particular reference.","Mark a configuration object readonly and test what the compiler rejects.","Assuming readonly is deep runtime freezing.","Distinguish compile-time constraints from runtime behavior."),
        ("Utility Types","Partial, Pick, Omit, Record, and related helpers transform existing types without rewriting them.","Create an update type from a full User type.","Using Partial when every field should actually be required.","Choose the smallest transformation that matches the API."),
        ("Mapped Types","Mapped types generate related types from the keys of another type.","Create a validation-state type from a Course type.","Building clever types nobody can understand.","Prefer readable types over type tricks."),
        ("Conditional Types","Conditional types let reusable type definitions adapt to their inputs.","Create a type that unwraps a Promise-like value conceptually.","Using advanced types when a normal alias is clearer.","Start with a concrete problem before introducing complexity."),
        ("Type Guards","Type guards combine runtime checks with TypeScript narrowing.","Write an isUser function that checks an unknown value.","Trusting a type assertion without checking the value.","Return false for malformed data."),
        ("Declaration Files","Declaration files describe JavaScript APIs to TypeScript.","Inspect the idea behind a small .d.ts file.","Assuming declarations validate runtime data.","Treat declarations as compile-time contracts only."),
        ("tsconfig","tsconfig controls strictness, module behavior, target output, and other compiler decisions.","Turn on strict mode and inspect the new errors.","Copying a config without understanding it.","Change one setting at a time and observe the effect."),
        ("Node.js with TypeScript","TypeScript can power scripts and servers outside the browser.","Design a typed CLI script.","Using browser-only APIs in a Node runtime.","Understand the runtime before selecting libraries."),
        ("Runtime API Validation","Static interfaces disappear at runtime, so external JSON still needs validation.","Design validation for an API response.","Casting unknown JSON directly to a trusted interface.","Validate at the application boundary."),
        ("Result Types","A Result union can represent success or expected failure explicitly.","Create a Result<T> type with ok and error states.","Throwing every expected failure.","Model recoverable failures explicitly."),
        ("Testing TypeScript","Tests verify runtime behavior while types protect compile-time contracts.","Write tests for a formatter and invalid input.","Testing only that TypeScript compiles.","Include boundary and malformed inputs."),
        ("Application Architecture","Separating UI, domain logic, API clients, and infrastructure reduces coupling.","Draw four layers for a course application.","Putting network calls into every UI component.","Give each layer one responsibility."),
        ("Performance","TypeScript types mostly disappear at runtime; JavaScript execution still determines performance.","Identify which operations in a TS file actually execute.","Assuming TypeScript itself makes code faster.","Measure runtime behavior separately from type checking."),
        ("Safe Refactoring","Compiler errors can guide large changes when types are precise.","Rename a field and follow every compiler error to completion.","Suppressing errors with any.","Fix the boundary first and work inward."),
        ("TypeScript Capstone Review","A final audit checks unsafe any, API boundaries, tests, and maintainability.","Audit a project file by file.","Counting type annotations instead of evaluating their usefulness.","Remove unnecessary any and document deliberate exceptions.")
    ], courses)

    _append("html", [
        ("Document Outline","A clear heading hierarchy and section structure creates a logical reading order.","Audit the headings on a real page.","Choosing headings only for visual size.","Use one clear main heading and logical sections."),
        ("HTML Attributes","Attributes add metadata, behavior, relationships, and state to elements.","Find five useful attributes on a page and explain each.","Adding attributes without understanding their semantics.","Look up each attribute's intended role."),
        ("Audio & Video","Media elements can provide controls, captions, and fallback behavior.","Design a video element with controls and captions.","Autoplaying media unexpectedly.","Provide controls and captions."),
        ("Responsive Images","srcset, sizes, and picture let a page choose an appropriate image asset.","Design image sources for phone and desktop.","Serving a huge image to every device.","Choose sources based on actual display needs."),
        ("Accessible Tables","Tables should describe relationships between data values using captions and headers.","Build a course comparison table.","Using tables as a layout mechanism.","Use table headers and captions for data tables."),
        ("Form Controls","The correct input type improves validation, semantics, and mobile usability.","Build a registration form with useful input types.","Using text inputs for every field.","Use email, password, number, date, and autocomplete appropriately."),
        ("Form Validation","Native constraints can catch simple mistakes before submission.","Add required, min, max, and pattern where useful.","Treating browser validation as a security boundary.","Validate again on the server."),
        ("Dialog & Disclosure","Native details, summary, and dialog patterns can replace unnecessary custom behavior.","Build an FAQ using details and summary.","Recreating native interactions manually.","Start with semantic browser features."),
        ("Accessibility Tree","Semantic HTML becomes structured information for assistive technology.","Compare a real button with a clickable div conceptually.","Using divs for every interactive control.","Prefer native interactive elements."),
        ("Keyboard Navigation","Interactive controls should be reachable and usable without a mouse.","Tab through a page and record every interactive element.","Removing focus outlines without replacement.","Keep a clear focus treatment."),
        ("SEO Foundations","Titles, descriptions, headings, and useful content give pages a clear purpose.","Write metadata for a course lesson.","Keyword stuffing.","Describe what the page actually provides."),
        ("Open Graph Basics","Metadata can improve link previews when pages are shared.","Design title, description, and image metadata.","Assuming every platform renders previews identically.","Test representative share links."),
        ("Security-Minded HTML","Untrusted content becomes dangerous when inserted as markup or used in unsafe links.","Identify an unsafe innerHTML pattern.","Trusting user input because it looks harmless.","Escape by default and sanitize when HTML is required."),
        ("Web Components Overview","Custom elements and shadow DOM can package reusable browser-native UI.","Sketch a custom course-card element.","Using custom elements for every tiny component.","Choose the simplest abstraction that fits."),
        ("HTML Project Audit","A proper audit checks semantics, accessibility, metadata, and document structure.","Audit a landing page using a checklist.","Checking only visual appearance.","Test structure, keyboard behavior, and metadata."),
        ("HTML Capstone","Build a complete accessible course landing page from scratch.","Create navigation, sections, media, a form, and footer.","Adding libraries before understanding the markup.","Finish semantics and accessibility before styling.")
    ], courses)

    _append("css", [
        ("Cascade Layers","Cascade layers group styles so large projects need less specificity fighting.","Design layers for reset, base, components, and utilities.","Adding specificity every time a rule loses.","Use a predictable layer hierarchy."),
        ("Advanced Combinators","Child, sibling, and descendant selectors describe relationships in markup.","Style only direct card children.","Writing fragile selector chains.","Use classes for reusable component contracts."),
        ("Positioning","Static, relative, absolute, fixed, and sticky positioning solve different problems.","Build a sticky header and positioned badge.","Absolutely positioning an entire page.","Use normal document flow first."),
        ("Stacking Contexts","z-index interacts with stacking contexts created by properties such as position and transforms.","Debug a modal that appears behind another element.","Using huge random z-index numbers.","Inspect the stacking context before changing numbers."),
        ("Typography","Font size, line height, weight, width, and spacing strongly affect readability.","Create a small type scale for a course site.","Using tiny line heights for a dense look.","Optimize for reading first."),
        ("Color Systems","Design tokens make backgrounds, surfaces, text, borders, and accents consistent.","Define a small color token system.","Choosing every color independently.","Reuse tokens and check contrast."),
        ("Container Queries","Container queries let components respond to their available space rather than only the viewport.","Make a reusable card grid adapt to its container.","Assuming viewport breakpoints solve every component problem.","Use container queries when the component is reused in different layouts."),
        ("Modern Sizing","clamp, min, max, minmax, and fluid units reduce brittle fixed sizing.","Create a fluid heading and responsive grid.","Hard-coding many device widths.","Let content and constraints drive the size."),
        ("Logical Properties","Block and inline properties make layouts less tied to physical directions.","Replace left/right spacing with logical equivalents.","Mixing physical and logical properties inconsistently.","Use logical properties in reusable components."),
        ("Form States","Good forms show focus, invalid, disabled, checked, and selected states clearly.","Style a complete form state set.","Making invalid fields visible only by color.","Combine state styling with accessible text and focus."),
        ("CSS Accessibility","CSS should preserve focus visibility, readable contrast, and reduced-motion preferences.","Add visible focus and reduced-motion rules.","Removing outlines just because they look different.","Replace default focus with an equally visible alternative."),
        ("Dark Mode","Custom properties make theme switching easier to maintain.","Create light and dark design tokens.","Hard-coding colors throughout every component.","Keep components dependent on semantic tokens."),
        ("Component Architecture","Reusable style contracts keep large CSS codebases predictable.","Design a naming and variant strategy for buttons and cards.","Creating hundreds of one-off selectors.","Define a component's structure and variants."),
        ("CSS Debugging","DevTools exposes computed styles, box dimensions, layout information, and matched selectors.","Trace a broken margin or overflowing grid.","Changing random values until the page looks right.","Inspect computed styles and layout boxes."),
        ("CSS Performance","Large effects and continuous layout changes can hurt responsiveness.","Identify expensive effects in a hypothetical UI.","Animating everything continuously.","Prefer efficient transforms and measure when necessary."),
        ("CSS Capstone Review","A final audit checks typography, spacing, states, responsiveness, overflow, and motion.","Test a design at narrow, normal, and wide widths.","Checking only one viewport.","Eliminate horizontal scrolling and inaccessible states.")
    ], courses)

    courses["javascript"] = {
        "slug":"javascript","title":"JavaScript Foundations","tag":"JS",
        "description":"Go from browser basics to DOM, events, storage, APIs, async code, modules, testing, and a complete web app.",
        "lessons":[
            _lesson("JavaScript in the Browser","JavaScript runs alongside HTML and CSS and can read and change the document.","Open DevTools and run a tiny console expression.","Treating JavaScript as markup.","Change one value and observe the result."),
            _lesson("Variables & Values","Use const and let with strings, numbers, booleans, null, and undefined.","Create a small learner profile from primitive values.","Using let when the binding never changes.","Prefer const by default."),
            _lesson("Conditions","if, else, comparison, and logical operators let programs choose behavior.","Build a score-to-rank function.","Confusing assignment with comparison.","Test boundary values."),
            _lesson("Loops","for, while, and array iteration methods repeat work over data.","Transform a list of scores.","Creating an infinite loop.","Give every loop a clear stopping condition."),
            _lesson("Functions","Functions package reusable behavior with parameters and return values.","Build a reusable formatter.","Making functions depend on hidden globals.","Pass required inputs explicitly."),
            _lesson("Arrays & Objects","Arrays represent collections while objects represent structured records.","Create a small course catalog.","Mutating data accidentally.","Use deliberate updates."),
            _lesson("DOM Basics","The DOM is the browser's structured representation of the page.","Build a counter by changing one text node.","Replacing the whole page unnecessarily.","Update the smallest necessary element."),
            _lesson("Events","Events connect user actions such as clicks and form submissions to code.","Build an interactive button.","Forgetting preventDefault on forms.","Handle events at the correct boundary."),
            _lesson("Local Storage","localStorage can persist small pieces of browser-controlled state.","Save a theme preference.","Storing passwords or secrets in localStorage.","Treat browser storage as user-controlled."),
            _lesson("Fetch & APIs","fetch requests data and promises represent asynchronous completion.","Design loading, success, and error states for an API request.","Assuming every response is successful.","Check status and validate data."),
            _lesson("Async & Await","async and await make promise-based flows easier to read.","Rewrite a promise chain using async/await.","Ignoring rejected promises.","Use try/catch around expected failures."),
            _lesson("Modules","ES modules split JavaScript into importable files.","Separate API and UI responsibilities.","Putting the whole application in one file.","Create clear module boundaries."),
            _lesson("Classes & Prototypes","Classes provide syntax for prototype-based objects and can package reusable behavior.","Create a Course class.","Using classes for every object.","Choose the simplest useful abstraction."),
            _lesson("Error Handling","Errors should be handled where the program can recover or communicate safely.","Design an API failure state.","Catching errors and silently hiding them.","Keep useful diagnostic context."),
            _lesson("Testing Browser Code","Tests verify runtime behavior while manual testing explores actual interaction.","List tests for a score calculator and a form.","Testing only the happy path.","Include invalid and boundary inputs."),
            _lesson("JavaScript Capstone","Combine state, DOM, events, storage, and an API into one browser project.","Build a quiz, tracker, dashboard, or mini game.","Adding features before the core loop works.","Ship the smallest complete version first.")
        ]
    }

    courses["sql"] = {
        "slug":"sql","title":"SQL & Databases","tag":"SQL",
        "description":"Learn relational database thinking, queries, joins, aggregation, indexes, transactions, schema design, and application data modeling.",
        "lessons":[
            _lesson("Database Thinking","Tables, rows, columns, keys, and relationships form the basic relational model.","Design tables for users, courses, and progress.","Putting every field into one giant table.","Identify entities and relationships first."),
            _lesson("SELECT","SELECT reads the columns and rows you request.","Write queries that return only required fields.","Selecting every column by habit.","Choose the smallest useful projection."),
            _lesson("WHERE & Filtering","WHERE filters rows using comparisons and logical expressions.","Find active learners from a sample table.","Using = NULL.","Use IS NULL and test NULL behavior."),
            _lesson("ORDER BY & LIMIT","Sorting and limiting makes results predictable and manageable.","Find the newest ten records.","Forgetting that ordering matters before presenting results.","Always specify order when order matters."),
            _lesson("INSERT, UPDATE & DELETE","Write operations change persistent data and therefore deserve extra care.","Plan an update and identify which rows it will affect.","Running UPDATE without a WHERE clause.","Preview affected rows before destructive changes."),
            _lesson("Aggregates","COUNT, SUM, AVG, MIN, and MAX summarize rows.","Calculate completion counts.","Ignoring NULL behavior in aggregates.","Know what each aggregate counts."),
            _lesson("GROUP BY","GROUP BY creates summaries for each category or key.","Count lessons per course.","Selecting columns that are neither grouped nor aggregated.","Make the grouping logic explicit."),
            _lesson("JOINs","JOIN combines related tables using keys.","Join users to progress records.","Accidentally multiplying rows.","Understand the relationship cardinality."),
            _lesson("Constraints & Indexes","Constraints protect data quality while indexes speed common access paths.","Add unique and foreign-key rules to a schema.","Adding indexes without a query need.","Index based on actual access patterns."),
            _lesson("Transactions","Transactions group related writes into an atomic unit.","Model two changes that must succeed together.","Assuming separate statements are automatically atomic.","Define the transaction boundary."),
            _lesson("Normalization","Normalization reduces unnecessary duplication and update anomalies.","Split repeated category data into a related table.","Over-normalizing a tiny system.","Balance integrity with practical access."),
            _lesson("Migrations","Schema changes should be planned and applied predictably.","Plan adding a new nullable field.","Editing production schemas manually without a migration.","Make changes reproducible."),
            _lesson("Query Planning","Databases choose execution strategies and indexes based on the query.","Compare an indexed lookup with a full scan conceptually.","Optimizing without measuring.","Inspect important query plans."),
            _lesson("Application Data Modeling","A good schema makes application code simpler and safer.","Design the data model for a course platform.","Mixing stable course content with mutable user state.","Separate content from progress."),
            _lesson("Database Security","Parameterized queries, least privilege, and protected credentials reduce risk.","Identify an SQL injection vulnerability.","Concatenating user input into SQL.","Bind parameters."),
            _lesson("SQL Capstone","Design and query a small production-style relational schema.","Build a course-progress database design.","Skipping constraints because the application validates input.","Make important invariants database-enforced.")
        ]
    }

    courses["git-github"] = {
        "slug":"git-github","title":"Git & GitHub","tag":"GIT",
        "description":"Learn version control, branches, remotes, pull requests, conflict resolution, releases, and safe collaboration.",
        "lessons":[
            _lesson("Why Git Exists","Git records snapshots and relationships between versions of a project.","Explain what a commit represents.","Thinking Git is only cloud backup.","Use history to understand how a change happened."),
            _lesson("Your First Repository","The working tree, staging area, and repository are different states.","Initialize a repository and inspect status.","Committing generated files by accident.","Use a sensible .gitignore."),
            _lesson("Commits","Small focused commits create useful history.","Split two unrelated changes into separate commits.","Messages like 'stuff'.","Describe the intent of each commit."),
            _lesson("Branches","Branches isolate work from the main line.","Create a feature branch conceptually.","Making every change directly on main.","Use branches for isolated changes."),
            _lesson("Merging","Merging combines histories and may require conflict resolution.","Merge a feature branch.","Ignoring conflict markers.","Read both versions before resolving."),
            _lesson("Remote Repositories","Push and pull synchronize work with a remote repository.","Connect a local project to GitHub conceptually.","Pushing secrets or generated artifacts.","Review status before pushing."),
            _lesson("Pull Requests","Pull requests provide review and a controlled integration point.","Write a focused PR description.","Opening giant unrelated PRs.","Keep diffs focused."),
            _lesson("Undoing Mistakes","Git has different recovery tools for different repository states.","Plan how to unstage, restore, and recover history safely.","Running destructive reset commands blindly.","Inspect state before choosing a command."),
            _lesson(".gitignore & Secrets","Generated files and credentials should not be committed.","Create a safe ignore list for a Python project.","Assuming deleting a secret from the latest commit is enough.","Rotate leaked credentials."),
            _lesson("Team Workflow","A repeatable branch-review-merge process reduces accidental conflicts.","Simulate a feature branch workflow.","Working from a stale branch.","Sync before major changes."),
            _lesson("Rebase Basics","Rebase replays commits onto a different base and can clean local history.","Describe what changes during a rebase.","Rebasing shared history carelessly.","Use rebase deliberately."),
            _lesson("Conflict Resolution","Conflicts are a normal result of overlapping changes.","Resolve a small text conflict on paper.","Choosing one side without reading it.","Run tests after resolving."),
            _lesson("Tags & Releases","Tags identify meaningful versions of source history.","Plan a version tag for a release.","Tagging arbitrary commits.","Tag releases with clear meaning."),
            _lesson("Git Debugging","log, diff, blame, and bisect concepts can help trace regressions.","Find which change could have introduced a bug.","Reading only the newest commit.","Use history to narrow the search."),
            _lesson("GitHub Project Hygiene","README files, issues, PRs, and workflows communicate how a project works.","Write a repository README outline.","Leaving setup instructions stale.","Test setup instructions from a clean clone."),
            _lesson("Git Capstone","Take a project through branch, commit, PR, review, release, and recovery workflows.","Practice the complete lifecycle.","Memorizing commands without understanding repository state.","Explain why each command is used.")
        ]
    }

    return list(courses.values()) if list_mode else courses
