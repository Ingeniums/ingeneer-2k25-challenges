
from flask import Flask
app = Flask(__name__)


    
@app.route("/")
def index():
    return "Admin panel - Not for public eyes! do not share this link with anyone!<br><br> <a href='/flag'>Flag</a>"


@app.route("/flag")
def flag():
    return open("flag.txt").read()


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)

