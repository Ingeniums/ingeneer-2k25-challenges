from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view_spellbook')
def view_spellbook():
    book = request.args.get('book', 'necronomicon/content.txt')
    
    try:
        book_path = os.path.join('spellbooks', book)
        
        with open(book_path, 'r') as file:
            content = file.read()
        
        book_titles = {
            'necronomicon': 'The Necronomicon',
            'grimoire': 'Grimorium Verum',
            'shadows': 'Codex of Shadows',
            'secrets': 'Chamber\'s Secrets'
        }
        
        book_name = book_titles.get(book, book.capitalize())
        
        return render_template('spellbook_details.html', book_name=book_name, book_id=book, content=content)
    
    except Exception as e:
        return f"This spellbook appears to be missing from the archives. Perhaps it's been... borrowed."
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)