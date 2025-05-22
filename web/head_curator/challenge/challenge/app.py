from flask import Flask, request, render_template
import yaml

app = Flask(__name__)

TREASURY = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload_item():
    file=request.files['item_yaml']
    data=yaml.load(file.read(),Loader=yaml.UnsafeLoader)
    TREASURY.append(data)
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
