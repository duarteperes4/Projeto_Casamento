from flask import Flask, render_template, request, redirect,url_for
from casamento import get_casamento_details, get_convidados, adicionar_convidado

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/casamento')
def casamento():
    casamento_info = get_casamento_details()
    return render_template('casamento.html', casamento=casamento_info)

# Rota para a página de convidados (lista)
@app.route('/convidados')
def convidados():
    convidados_list = get_convidados()
    return render_template('convidados.html', convidados=convidados_list)

# Rota para adicionar um novo convidado
@app.route('/adicionar-convidado', methods=['GET', 'POST'])
def adicionar_convidado_route():
    if request.method == 'POST':
        nome = request.form['nome']
        restricoes = request.form['restricoes']
        confirmado = request.form['confirmado']
        adicionar_convidado(nome, restricoes, confirmado)
        return redirect(url_for('convidados'))
    return render_template('adicionar_convidado.html')

if __name__ == '__main__':
    app.run(debug=True)