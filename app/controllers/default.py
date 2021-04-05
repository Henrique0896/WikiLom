from app import app
from flask import render_template, jsonify, Response
from app import db
from app.models.forms import campoPesquisa, filtroDeDados, updateGeral
import wikipedia
import json
from ..models.tables import LearningObject
from .keys import keys
from bson import json_util

pages_found = None
instance_list = db.list("learning_object")


# ----------------- API ------------

# READ
@app.route("/api/lista", methods=['GET'])
def lista():
    query = db.filter_by('learning_object', {})
    if (len(query) < 1):
        return ({"success :": False, "message": "Nao existe nenhum registro para a consulta"})
    return Response(json.dumps(query, default=json_util.default, ensure_ascii=False), content_type="application/json; charset=utf-8")


# READ TITLES
@app.route("/api/titulos", methods=['GET'])
def titulos():
    query = db.filter_by('learning_object', {})
    r = []
    if (len(query) < 1):
        return ({"success :": False, "message": "Nao existe nenhum registro para a consulta"})
    for i in query:
        r.append(i["geral"]["titulo"])
    return Response(json.dumps(r, default=json_util.default, ensure_ascii=False), content_type="application/json; charset=utf-8")


# FILTRO
@app.route("/api/consulta/<campo>/<filtro>", methods=['GET'])
def consulta(campo, filtro):
    resultado = []
    if (campo not in keys):
        return ({"success": False, "message": "Campo inexistente"})
    for value in keys[campo].values():
        query = db.filter_by('learning_object', {value: filtro})
        resultado.append(json.dumps(query, default=json_util.default,
                         ensure_ascii=False)) if (len(query)) != 0 else None
    if (len(resultado) < 1):
        return ({"success :": False, "message": "Nao existe nenhum registro para a consulta"})
    return Response(resultado, content_type="application/json; charset=utf-8")


# CREATE
@app.route("/api/add/<page>/<pagination>", methods=['GET', 'POST'])
def add(page, pagination):
    pages = []
    for i in [wikipedia.search(page)[int(pagination)]] if str.isdigit(pagination) else wikipedia.search(page):
        if len(db.filter_by('learning_object', {"geral.titulo": i})) < 1:
            page = wikipedia.page(i)
            learning_object = (LearningObject(page))
            lom = json.dumps(learning_object.get_as_json(),
                             default=json_util.default, ensure_ascii=False)
            db.create("learning_object", learning_object)
            pages.append(lom)
    return Response({"success": True}, content_type="application/json; charset=utf-8")


# DELETE
@app.route("/api/delete/<title>/", methods=['GET', 'POST'])
def delete(title):
    page = db.filter_by('learning_object', {"geral.titulo": title})
    if (len(page) < 1):
        return {"success": "false", "msg": "Não existe nenhuma pagina salva com este titulo"}
    else:
        db.delete("learning_object", page[0])
    return Response({"success": True}, content_type="application/json; charset=utf-8")


# UPDATE
@app.route("/api/update/<title>/<prop>/<data>", methods=['GET', 'POST'])
def update(title, prop, data):
    try:
        page = db.filter_by('learning_object', {"geral.titulo": title})
        ref = page[0]
        if (len(page) < 1):
            return {"success": "false", "msg": "Não existe nenhuma pagina salva com este titulo"}
        ls = str.split(prop, ".")
        if( len(ls) == 2 ):
            fst = ls.pop()
            for i in ls:
                ref = ref[i]
            ref[fst] = data
            page[0][ls[0]] = ref
        elif( len(ls) == 3 ):
            fst = ls.pop()
            for i in ls:
                ref = ref[i]
            ref[fst] = data
            page[0][ls[0]][ls[1]] = ref
        else: raise Exception

        db.update("learning_object", page[0])
        return Response({"success": True}, content_type="application/json; charset=utf-8")
    except:
        return Response({"success": False}, content_type="application/json; charset=utf-8")



# ------------ ROTAS -------------


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
            pages.append([page, str(i)])
            i = i+1
    else:
        pages = None
    return render_template('index.html', materias=pages)


# Pesquisa qual materia será adicionada
@app.route("/adicionar", methods=['POST', 'GET'])
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
                pages.append([page, str(i)])
                i = i+1
        else:
            pass
    else:
        print(form.errors)

    return render_template('adicionar.html', form=form, pages=pages)


# Adiciona materia ao banco
@app.route("/adicionar/<pageNumber>", methods=['POST', 'GET'])
def adicionarPage(pageNumber):
    global pages_found
    page_title = pages_found[int(pageNumber)]
    page = wikipedia.page(page_title)
    learning_object = (LearningObject(page))
    lom = json.dumps(learning_object.get_as_json(), indent=4)
    db.create("learning_object", learning_object)

    return render_template('adicionado.html', page_title=page_title)


# Deletar materia ao banco
@app.route("/excluir/<pageNumber>", methods=['DELETE', 'GET'])
def excluirPage(pageNumber):
    global instance_list
    page_title = instance_list[int(pageNumber)]['geral']['titulo']
    db.delete("learning_object", instance_list[int(pageNumber)])

    return render_template('removido.html', page_title=page_title)


# Listar materia ao banco
@app.route("/listar/<pageNumber>", methods=['GET'])
def listarPage(pageNumber):
    global instance_list
    page = instance_list[int(pageNumber)]

    return render_template('listar.html', page=page, pageNumber=pageNumber)


# Pesquisar materia no banco
@app.route("/pesquisar", methods=['POST', 'GET'])
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
            resultado = db.filter_by('learning_object', {value: filtro})
            if(resultado):
                resultados.append(resultado)
        for resultado in resultados:
            for materia in resultado:
                pages.append(materia['geral']['titulo'])
    else:
        print(form.errors)
    return render_template('pesquisar.html', form=form, pages=pages, filtro=filtro)




# Editar Geral
@app.route("/editar/geral/<pageNumber>", methods=['GET', 'POST'])
def editarGeral(pageNumber):
    global instance_list
    page = instance_list[int(pageNumber)]
    
    form = updateGeral()
    

    if form.validate_on_submit():
        print("VALIDADO")
        page['geral']['titulo'] = form.titulo.data
        db.update("learning_object", page)
        return render_template('listar.html', page=page, pageNumber=pageNumber)
    else:
        form.titulo.data = page['geral']['titulo']
        form.idioma.data = page['geral']['idioma']
        form.descricao.data = page['geral']['descricao']
        form.palavrasChave.data = page['geral']['palavras_chave']
        form.cobertura.data = page['geral']['cobertura']
        form.estrutura.data = page['geral']['estrutura']
        form.nivelDeAgregacao.data = page['geral']['nivel_de_agregacao']
        print(form.errors)

    return render_template('geral.html', page=page, form=form)