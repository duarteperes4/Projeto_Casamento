from flask import Flask, render_template, request, redirect,url_for
from casamento import get_casamento_details

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/casamento')
def casamento():
    casamento_info = get_casamento_details()
    return render_template('casamento.html', casamento=casamento_info)

if __name__ == '__main__':
    app.run(debug=True)