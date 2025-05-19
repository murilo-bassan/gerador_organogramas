from flask import Flask, render_template, request, send_file
from graphviz import Digraph
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        entradas = request.form['estrutura']
        hierarquia = {}

        for linha in entradas.strip().split('\n'):
            if ':' in linha:
                nivel, nomes = linha.split(':')
                hierarquia[nivel.strip()] = [n.strip() for n in nomes.split(',')]

        gerar_organograma(hierarquia)
        return send_file('static/organograma.png', mimetype='image/png')

    return render_template('index.html')

def gerar_organograma(hierarquia):
    dot = Digraph(comment='Organograma')
    for nivel, pessoas in hierarquia.items():
        for pessoa in pessoas:
            dot.node(pessoa, pessoa)

    niveis = list(hierarquia.values())
    for i in range(len(niveis) - 1):
        for chefe in niveis[i]:
            for subordinado in niveis[i + 1]:
                dot.edge(chefe, subordinado)

    dot.render('static/organograma', format='png', cleanup=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
