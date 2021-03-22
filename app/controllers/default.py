from app import app
from flask import render_template
from app import db
from app.models.forms import addMateria
import wikipedia

instance_list = db.list("learning_object")

           

@app.route("/index")
@app.route("/")
def index():
    instance_list = db.list("learning_object")
    return render_template('index.html', materias=instance_list)


@app.route("/adicionar", methods=['POST', 'GET' ])
def adicionar():
    form = addMateria()
    pages_found = None
    if form.validate_on_submit():
        pages_found = wikipedia.search(form.pesquisa.data)
        if len(list(pages_found)) == 0:
            pages_found = None
        else:
            pass
    else:
        print(form.errors)
   
    return render_template('adicionar.html', form=form, pages_found=pages_found)