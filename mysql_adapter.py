import os, time, re, sqlite3
import pymysql
from pymysql.cursors import DictCursor

class _Cursor:
    def __init__(self, cur): self._cur = cur
    def fetchone(self): return self._cur.fetchone()
    def fetchall(self): return self._cur.fetchall()
    @property
    def rowcount(self): return self._cur.rowcount
    @property
    def lastrowid(self): return self._cur.lastrowid

class MySQLCompat:
    def __init__(self, conn): self._conn = conn
    def _sql(self, sql):
        s = sql.strip()
        s = re.sub(r"ON CONFLICT\\(user_id,lesson_id\\) DO UPDATE SET completed=1,updated_at=CURRENT_TIMESTAMP",
                   "ON DUPLICATE KEY UPDATE completed=VALUES(completed),updated_at=CURRENT_TIMESTAMP", s, flags=re.I)
        s = s.replace("INSERT OR REPLACE", "REPLACE")
        s = s.replace("?", "%s")
        return s
    def execute(self, sql, args=()):
        cur = self._conn.cursor()
        cur.execute(self._sql(sql), tuple(args))
        return _Cursor(cur)
    def executescript(self, script):
        for stmt in script.split(";"):
            stmt = stmt.strip()
            if stmt:
                self.execute(stmt)
    def commit(self): self._conn.commit()
    def rollback(self): self._conn.rollback()
    def close(self): self._conn.close()

def _connect():
    host = os.environ["MYSQLHOST"]
    port = int(os.environ.get("MYSQLPORT", "3306"))
    user = os.environ["MYSQLUSER"]
    password = os.environ["MYSQLPASSWORD"]
    database = os.environ["MYSQLDATABASE"]
    for attempt in range(30):
        try:
            return pymysql.connect(host=host, port=port, user=user, password=password,
                                   database=database, charset="utf8mb4",
                                   cursorclass=DictCursor, autocommit=False,
                                   connect_timeout=5, read_timeout=10, write_timeout=10)
        except Exception as e:
            if attempt == 29:
                raise
            time.sleep(2)

def _schema(con):
    con.executescript("""
    CREATE TABLE IF NOT EXISTS users(
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      email VARCHAR(254) UNIQUE NOT NULL,
      name VARCHAR(255) NOT NULL,
      password TEXT NOT NULL,
      is_admin TINYINT DEFAULT 0,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ;
    CREATE TABLE IF NOT EXISTS progress(
      user_id BIGINT NOT NULL,
      lesson_id INT NOT NULL,
      completed TINYINT DEFAULT 0,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY(user_id,lesson_id),
      CONSTRAINT fk_progress_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ;
    CREATE TABLE IF NOT EXISTS auth_limits(
      bucket VARCHAR(255) PRIMARY KEY,
      window_start BIGINT NOT NULL,
      attempts INT NOT NULL
    )
    ;
    CREATE TABLE IF NOT EXISTS migration_meta(
      name VARCHAR(100) PRIMARY KEY,
      completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ;
    """)

def _migrate_sqlite(con):
    path = os.environ.get("DATABASE_PATH", "course.db")
    if not os.path.exists(path):
        return
    marker = con.execute("SELECT name FROM migration_meta WHERE name=?", ("sqlite_v1",)).fetchone()
    if marker:
        return
    try:
        src = sqlite3.connect(path)
        src.row_factory = sqlite3.Row
        users = src.execute("SELECT id,email,name,password,is_admin,created_at FROM users").fetchall()
        for u in users:
            con.execute(
                "INSERT INTO users(id,email,name,password,is_admin,created_at) VALUES(?,?,?,?,?,?) "
                "ON DUPLICATE KEY UPDATE email=VALUES(email),name=VALUES(name),password=VALUES(password),is_admin=VALUES(is_admin)",
                (u["id"],u["email"],u["name"],u["password"],u["is_admin"],u["created_at"])
            )
        progress = src.execute("SELECT user_id,lesson_id,completed,updated_at FROM progress").fetchall()
        for p in progress:
            con.execute(
                "INSERT INTO progress(user_id,lesson_id,completed,updated_at) VALUES(?,?,?,?) "
                "ON DUPLICATE KEY UPDATE completed=VALUES(completed),updated_at=VALUES(updated_at)",
                (p["user_id"],p["lesson_id"],p["completed"],p["updated_at"])
            )
        limits = src.execute("SELECT bucket,window_start,attempts FROM auth_limits").fetchall()
        for a in limits:
            con.execute(
                "INSERT INTO auth_limits(bucket,window_start,attempts) VALUES(?,?,?) "
                "ON DUPLICATE KEY UPDATE window_start=VALUES(window_start),attempts=VALUES(attempts)",
                (a["bucket"],a["window_start"],a["attempts"])
            )
        src.close()
        con.execute("INSERT INTO migration_meta(name) VALUES(?)", ("sqlite_v1",))
        con.commit()
        print(f"[LearnPython] migrated {len(users)} users and {len(progress)} progress rows from SQLite to MySQL")
    except Exception as e:
        con.rollback()
        print("[LearnPython] SQLite migration skipped:", repr(e))

def install(mod):
    con = MySQLCompat(_connect())
    _schema(con)
    _migrate_sqlite(con)
    con.commit()
    mod.db = lambda: MySQLCompat(_connect())
    mod.DB = "mysql"
    print("[LearnPython] MySQL database connected and schema ready")
