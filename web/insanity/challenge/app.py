from flask import Flask, session, redirect, url_for, render_template, request
import sqlite3
from config import SECRET_KEY
import random 
import os 

app = Flask(__name__)
app.secret_key = SECRET_KEY

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'database.db')
    sql_path = os.path.join(os.path.dirname(__file__), 'db', 'init.sql')

    # Only init if db doesn't exist
    if not os.path.exists(db_path):
        print("[*] Initializing database...")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        with open(sql_path, 'r') as f:
            conn.executescript(f.read())
        conn.close()
        print("[+] Database initialized.")
    else:
        print("[*] Database already exists.")

def get_db():
    conn = sqlite3.connect("db/database.db")
    conn.row_factory = sqlite3.Row
    return conn
def filter_role_id(val):
        blacklist = [
            # SQLi basics
            "union", "insert", "update", "delete", "drop", "alter", "create", "--", ";",

            # File access / exfil
            "file",

            # MSSQL-specific
            "xp_cmdshell", "openrowset", "bulk insert", "sp_oacreate", "sp_makewebtask",

            # Oracle-specific
            "utl_http", "dbms_ldap", "dbms_pipe", "utl_inaddr", "dbms_xdb", "httpuritype",

            # Linux command execution (UDF or external tools)
            "sys_eval", "sys_exec", "wget", "curl", "ping", "nc", "bash", "sh",

            # Encoding tricks
            "char(", "ascii(", "hex(", "unhex(", "conv(", "cast(",

            # String building and DNS tricks
            "concat(", "concat_ws(", "group_concat(", "substring(",

            # Dangerous operators
            "@@", "@", "#","||", "+", "%00", "%"," "
        ]

        s = str(val).lower()
        for word in blacklist:
            if word in s:
                return False
        
        return True
@app.before_request
def set_session():
    if "id" not in session:
        session["id"] = 2
        session["username"] = "Neville"
        session["role_id"] = 1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    conn = get_db()
    role_id = session.get("role_id")
    if (not filter_role_id(role_id)):
        desc = "Hmmm what are you trying to do ?"
    else:
        try:
            query = f"SELECT description FROM roles WHERE id = {role_id}"
            print(query)
            cursor = conn.execute(query)
            result = cursor.fetchone()
            if (result) :
                if ("1ng3neer2k25" in result["description"]):
                    desc = "Hmmm what are you trying to do ?"
                else:
                    desc = result["description"]
            else:
                desc = "Unknown magical rank."
        except Exception as e:
            print(e)
            desc = "The Ministry is investigating this incident."
    return render_template("dashboard.html", role_description=desc)

@app.route("/wand", methods=["GET", "POST"])
def wand():
    conn = get_db()

    if request.method == "POST":
        owner = request.form.get("owner", "")
        wood = request.form.get("wood", "")
        core = request.form.get("core", "")
        length = request.form.get("length", "")
        conn.execute("INSERT INTO wands (owner, wood, core, length) VALUES (?, ?, ?, ?)", 
                     (owner, wood, core, length))
        conn.commit()

    cur = conn.execute("SELECT owner, wood, core, length FROM wands")
    all_wands = cur.fetchall()
    
    return render_template("wand.html", wands=all_wands)

@app.route("/sorting-hat", methods=["GET", "POST"])
def sorting_hat():
    conn = get_db()
    houses = ['Gryffindor', 'Slytherin', 'Ravenclaw', 'Hufflepuff']
    sorted_students = []

    if request.method == "POST":
        name = request.form.get("name", "")
        house = random.choice(houses)
        conn.execute("INSERT INTO sorting_hat (name, house) VALUES (?, ?)", (name, house))
        conn.commit()

    cur = conn.execute("SELECT name, house FROM sorting_hat")
    sorted_students = cur.fetchall()

    return render_template("sorting_hat.html", students=sorted_students)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
