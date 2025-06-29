from flask import Flask, render_template, request, redirect, url_for, session,flash
from casamento import get_casamento_details, get_catering, atualizar_catering, get_convidados, adicionar_convidado, get_musicos, adicionar_musico, adicionar_feedback, get_orcamento_final, atualizar_orcamento_final
from datetime import datetime
import os 

app = Flask(__name__)
app.secret_key = os.urandom(24) 

USERS= {'duarteperes4' : 'Duarteperes'}

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    print("Rota / acessada em", datetime.now())
    image_url = url_for('static', filename='images/casamento.jpg')
    print(f"URL da imagem gerada: {image_url}")
    return render_template('index.html', image_url=image_url)


# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    print("A tentar fazer logout...", session.get('logged_in'))
    session.clear()  
    print("Após logout, sessão:", session.get('logged_in'))
    flash('Saiste da sessão.', 'info')
    return redirect(url_for('login'))



# Rota para a página de detalhes do casamento
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
        data_atualizacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        atualizar_catering(menu, numero_convidados, observacoes, data_atualizacao)
        return redirect('/casamento')
    
    return render_template('casamento.html', casamento=casamento_info, catering=catering_info)

# Rota para a página de convidados
@app.route('/convidados', methods=['GET', 'POST'])
def convidados():
    from casamento import get_convidados, excluir_convidado
    convidados_list = get_convidados()
    if request.method == 'POST':
        convidado_id = request.form['convidado_id']
        if convidado_id:
            excluir_convidado(convidado_id)
            return redirect('/convidados')
    return render_template('convidados.html', convidados=convidados_list)




@app.route('/adicionar-convidado', methods=['GET', 'POST'])
def adicionar_convidado_page():
    if request.method == 'POST':
        nome = request.form['nome']
        restricoes = request.form['restricoes']
        confirmado = request.form['confirmado']
        adicionar_convidado(nome, restricoes, confirmado)
        return redirect('/convidados')
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
@app.route('/adicionar_musico', methods=['POST'])
def adicionar_musico():
    global musicos
    nome = request.form['nome']
    tipo = request.form['tipo']
    horario = request.form['horario']
    musicos.append({'nome': nome, 'tipo': tipo, 'horario': horario})
    return redirect(url_for('musicos'))

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
        data_atualizacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        atualizar_orcamento_final(catering, decoracao, fotografia, musica, outros, total, data_atualizacao)
        return redirect(url_for('orcamento_final'))
    return render_template('orcamento_final.html', orcamento=orcamento)


if __name__ == '__main__':
    app.run(debug=True)