# LearnPython

Interactive learning platform for **The Ultimate Python Course**.

## Run locally
```bash
python -m venv .venv
# activate it
pip install -r requirements.txt
python app.py
```

## Production
Set a long random `SECRET_KEY`, use HTTPS, `COOKIE_SECURE=1`, and run:
```bash
gunicorn app:APP
```

Learner Python code executes in the browser with Pyodide rather than on the server.
