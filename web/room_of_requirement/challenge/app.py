from flask import Flask, Response, render_template, request, redirect, url_for, session, flash
from jinja2.sandbox import SandboxedEnvironment
import traceback
from functools import wraps

app = Flask(__name__)
app.secret_key = "c7f_s3cr3t_k3y_d0nt_l34k_m3"

users = {
    "user": {"password": "userpass", "is_admin": False},
    "admin": {"password": "", "is_admin": True}
}

def useless():
    return

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or not users.get(session['username'], {}).get('is_admin', False):
            flash('Admin access required')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def get():
    return render_template("index.html")

@app.route("/render", methods=['POST'])
def post():
    try:
        html = request.get_json()["html"]
    except:
        return Response("Invalid JSON", status=400)
    
    env = SandboxedEnvironment()
    env.globals = {'useless': useless}

    try:
        return env.from_string(html).render()
    except Exception as e:
        print(traceback.format_exc())
        return '<p style="color: #bf9b30;">Something Went Wrong!</p>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] != "" and users[username]['password'] == password:
            session['username'] = username
            session['is_admin'] = users[username]['is_admin']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/admin')
@admin_required
def admin_panel():
    return render_template('admin.html', FLAG=open('flag.txt').read())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)