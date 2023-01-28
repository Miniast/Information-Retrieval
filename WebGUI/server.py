import webbrowser
from search import search
from flask import Flask, render_template, request
from flask_cors import CORS

# app = Flask(__name__, static_folder='./web_client/dist/static', template_folder='./web_client/dist', static_url_path='')
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api', methods=['GET', 'POST'])
def search_text():
    if request.method == 'POST':
        text = request.get_json()
        res = search(text['text'])
        return {'data': res}
    else:
        return 'Hallo World'


if __name__ == '__main__':
    # webbrowser.open('http://localhost:5000')
    app.run()
