from app import app
from flask import render_template
from app import db
from app.models.forms import addMateria
import wikipedia
import json
from ..models.tables import LearningObject

pages_found = None


# Lista objetos do Banco
@app.route("/index")
@app.route("/")
def index():
    instance_list = db.list("learning_object")
    return render_template('index.html', materias=instance_list)


# Pesquisa qual materia será adicionada
@app.route("/adicionar", methods=['POST', 'GET' ])
def adicionar():
    form = addMateria()
    global pages_found
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