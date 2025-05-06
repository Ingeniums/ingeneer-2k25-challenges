from flask import Flask, request, render_template_string

app = Flask(__name__)
BLACKLIST = ['.', '[', ']', '\\x5f']

def is_blacklisted(name):
    for char in BLACKLIST:
        if char in name:
            print(char)
            return True
    return False


@app.route('/')
def index():
    return '''
    <html>
    <head>
       
        <title>Hogwarts Terminal</title>
        <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative&display=swap" rel="stylesheet">
        <style>
            body {
                background: url('https://wallpaperaccess.com/full/562419.jpg') no-repeat center center fixed;
                background-size: cover;
                color: #fceec7;
                font-family: 'Cinzel Decorative', cursive;
                text-align: center;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }
            input[type="text"] {
                padding: 10px;
                border: 2px solid #dab88b;
                border-radius: 5px;
                width: 300px;
                font-size: 16px;
                background-color: rgba(0,0,0,0.5);
                color: #fceec7;
            }
            input[type="submit"] {
                padding: 10px 20px;
                background-color: #5d4037;
                color: #fceec7;
                border: none;
                border-radius: 5px;
                margin-left: 10px;
                cursor: pointer;
            }
            .container {
                background-color: rgba(0, 0, 0, 0.6);
                padding: 30px;
                display: inline-block;
                
                border: 2px solid #dab88b;
                border-radius: 15px;
            }
        </style>
    </head>
    <body>
        <!-- This is a flask -->
        <div class="container">
            <h1>Congrats!!! you passed the secret portal !</h1>
            <p>Now welcome to the Room of Requirement</p>
            <p>Whisper your name into the spellbook…</p>
            <form method="get" action="/greet">
                <input type="text" name="name" placeholder="e.g. Hermione Granger">
                <input type="submit" value="Cast Spell">
            </form>
        </div>
    </body>
    </html>
    '''



@app.route('/greet')
def greet():
    name = request.args.get('name', '')
    blacklisted = is_blacklisted(name)
    if blacklisted:
        return render_template_string(f"<h2>⚠️ Forbidden characters detected! ⚠️</h2><br><p>the blacklist is:{', '.join(BLACKLIST)} </p>")
    
    len_args  = len(request.args)
    if len_args > 2:
        return render_template_string(f"<h2>⚠️ Too many arguments! ⚠️</h2><br><p>Only two arguments are allowed.</p>")
    template = """
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative&display=swap" rel="stylesheet">
        <style>
            body {
                background: url('https://wallpaperaccess.com/full/562419.jpg') no-repeat center center fixed;
                background-size: cover;
                color: #fceec7;
                font-family: 'Cinzel Decorative', cursive;
                text-align: center;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }
            input[type="text"] {
                padding: 10px;
                border: 2px solid #dab88b;
                border-radius: 5px;
                width: 300px;
                font-size: 16px;
                background-color: rgba(0,0,0,0.5);
                color: #fceec7;
            }
            input[type="submit"] {
                padding: 10px 20px;
                background-color: #5d4037;
                color: #fceec7;
                border: none;
                border-radius: 5px;
                margin-left: 10px;
                cursor: pointer;
            }
            .container {
                background-color: rgba(0, 0, 0, 0.6);
                padding: 30px;
                display: inline-block;
                
                border: 2px solid #dab88b;
                border-radius: 15px;
            }
        </style>
    </head>
    <body>
        {{7 * 7}}
        <div class="container"> 
            <h2>✨ The spell greets you: """ + name + """ ✨</h2>
        </div>
    </body>
    """
    return render_template_string(template)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)

