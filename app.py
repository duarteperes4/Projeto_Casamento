from flask import Flask, render_template, request, redirect,url_for
from casamento import get_casamento_details, get_catering, atualizar_catering, get_convidados, adicionar_convidado, get_musicos,adicionar_musico, adicionar_feedback,get_orcamento_final,atualizar_orcamento_final
from datetime import datetime

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/casamento', methods=['GET', 'POST'])
def casamento():
    casamento_info = get_casamento_details()
    catering_info = get_catering()
    if casamento_info is None or catering_info is None:
        return "Erro ao carregar detalhes do casamento ou catering.", 500
    
    if request.method == 'POST':
        menu = request.form['menu']
        numero_convidados = int(request.form['numero_convidados'])
        observacoes = request.form['observacoes']
        data_atualizacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Ex: 2025-06-06 16:43:00
        atualizar_catering(menu, numero_convidados, observacoes, data_atualizacao)
        return redirect('/casamento')  # Recarrega a página com os novos dados
    
    return render_template('casamento.html', casamento=casamento_info, catering=catering_info)


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



# Rota para a página de DJ's e músicos
@app.route('/musicos')
def musicos():
    musicos_list = get_musicos()
    try:
        return render_template('musicos.html', musicos=musicos_list if musicos_list else [])
    except Exception as e:
        return f"Erro ao carregar o template 'musicos.html': {str(e)}", 500

# Rota para adicionar um novo DJ/músico
@app.route('/adicionar-musico', methods=['GET', 'POST'])
def adicionar_musico_route():
    if request.method == 'POST':
        nome = request.form['nome']
        tipo = request.form['tipo']
        horario = request.form['horario']
        adicionar_musico(nome, tipo, horario)
        return redirect(url_for('musicos'))
    return render_template('adicionar_musico.html')


@app.route('/wedding-planners', methods=['GET', 'POST'])
def wedding_planners():
    if request.method == 'POST':
        nome = request.form['nome']
        comentario = request.form['comentario']
        data_envio = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        adicionar_feedback(nome, comentario, data_envio)
        return redirect(url_for('index'))  
    return render_template('wedding_planners.html')


@app.route('/orcamento-final', methods=['GET', 'POST'])
def orcamento_final():
    orcamento = get_orcamento_final()
    if request.method == 'POST':
        catering = float(request.form.get('catering', 0.0))
        decoracao = float(request.form.get('decoracao', 0.0))
        fotografia = float(request.form.get('fotografia', 0.0))
        musica = float(request.form.get('musica', 0.0))
        outros = float(request.form.get('outros', 0.0))
        total = catering + decoracao + fotografia + musica + outros
        data_atualizacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Ex: 2025-06-06 16:16:00
        atualizar_orcamento_final(catering, decoracao, fotografia, musica, outros, total, data_atualizacao)
        return redirect(url_for('orcamento_final'))
    return render_template('orcamento_final.html', orcamento=orcamento)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)