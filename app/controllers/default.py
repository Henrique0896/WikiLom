from app import app
from flask import render_template
from app import db
from app.models.forms import campoPesquisa, filtroDeDados
import wikipedia
import json
from ..models.tables import LearningObject
from .keys import keys

pages_found = None
instance_list = db.list("learning_object")



# Lista objetos do Banco
@app.route("/index")
@app.route("/")
def index():
    global instance_list
    instance_list = db.list("learning_object")
    if len(list(instance_list)) != 0:
        i = 0
        pages = []
        for page in instance_list:
            pages.append([ page, str(i) ])
            i=i+1
    else:
        pages = None
    return render_template('index.html', materias=pages)


# Pesquisa qual materia será adicionada
@app.route("/adicionar", methods=['POST', 'GET' ])
def adicionar():
    form = campoPesquisa()
    global pages_found
    pages_found = None
    pages = None
    if form.validate_on_submit():
        pages_found = wikipedia.search(form.pesquisa.data)
        if len(list(pages_found)) != 0:
            i = 0
            pages = []
            for page in pages_found:
                pages.append([ page, str(i) ])
                i=i+1
        else:
            pass
    else:
        print(form.errors)

    return render_template('adicionar.html', form=form, pages=pages)



#Adiciona materia ao banco
@app.route("/adicionar/<pageNumber>", methods=['POST', 'GET' ])
def adicionarPage(pageNumber):
    global pages_found
    page_title = pages_found[int(pageNumber)]
    page = wikipedia.page(page_title)
    learning_object = (LearningObject(page))
    lom = json.dumps(learning_object.get_as_json(), indent=4)
    db.create("learning_object", learning_object)

    return render_template('adicionado.html', page_title=page_title)



#Deletar materia ao banco
@app.route("/excluir/<pageNumber>", methods=['DELETE', 'GET' ])
def excluirPage(pageNumber):
    global instance_list
    page_title = instance_list[int(pageNumber)]['geral']['titulo']
    db.delete("learning_object", instance_list[int(pageNumber)])

    return render_template('removido.html', page_title=page_title)



#Listar materia ao banco
@app.route("/listar/<pageNumber>", methods=[ 'GET' ])
def listarPage(pageNumber):
    global instance_list
    page = instance_list[int(pageNumber)]

    return render_template('listar.html', page=page)



# Pesquisar materia no banco
@app.route("/pesquisar", methods=['POST', 'GET' ])
def pesquisar():
    form = filtroDeDados()
    pages = None
    filtro = None
    if form.validate_on_submit():
        pages = []
        filtro = form.pesquisa.data
        campo = form.subject.data
        resultados = []
        for value in keys[campo].values():
            resultado = db.filter_by('learning_object', { value: filtro })
            if(resultado):
                resultados.append(resultado)
        for resultado in resultados:
            for materia in resultado:
                pages.append(materia['geral']['titulo'])
            
        print(pages)


        
    else:
        print(form.errors)
    return render_template('pesquisar.html', form=form, pages=pages, filtro=filtro)