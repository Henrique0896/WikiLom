from app import app
from flask import render_template, jsonify, Response, redirect, url_for
from app import db
from app.models.forms import campoPesquisa, filtroDeDados, updateGeral, loginForm, createAccountForm, profileForm
import wikipedia
import json
from ..models.tables import LearningObject, User
from .keys import keys
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
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
@login_required
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
@login_required
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
        pass

    return render_template('create/adicionar.html', form=form, pages=pages)


# Adiciona materia ao banco
@app.route("/adicionar/<pageNumber>", methods=['POST', 'GET'])
@login_required
def adicionarPage(pageNumber):
    global pages_found
    page_title = pages_found[int(pageNumber)]
    page = wikipedia.page(page_title)
    learning_object = (LearningObject(page))
    db.create("learning_object", learning_object)

    return render_template('create/adicionado.html', page_title=page_title)


# Deletar materia ao banco
@app.route("/excluir/<pageNumber>", methods=['DELETE', 'GET'])
@login_required
def excluirPage(pageNumber):
    global instance_list
    page_title = instance_list[int(pageNumber)]['geral']['titulo']
    db.delete("learning_object", instance_list[int(pageNumber)])

    return render_template('delete/removido.html', page_title=page_title)


# Listar materia ao banco
@app.route("/listar/<pageNumber>", methods=['GET'])
@login_required
def listarPage(pageNumber):
    global instance_list
    page = instance_list[int(pageNumber)]

    return render_template('read/listar.html', page=page, pageNumber=pageNumber)


# Pesquisar materia no banco
@app.route("/pesquisar", methods=['POST', 'GET'])
@login_required
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
        pass
    return render_template('filter/pesquisar.html', form=form, pages=pages, filtro=filtro)




# Editar Geral
@app.route("/editar/<pageNumber>", methods=['GET', 'POST'])
@login_required
def editarGeral(pageNumber):
    global instance_list
    page = instance_list[int(pageNumber)]
    
    form = updateGeral()

    if form.validate_on_submit():
        page['geral']['titulo'] = form.titulo.data
        page['geral']['idioma'] = form.idioma.data
        page['geral']['descricao'] = form.descricao.data
        page['geral']['palavras_chave'] = form.palavrasChave.data
        page['geral']['cobertura'] = form.cobertura.data
        page['geral']['estrutura'] = form.estrutura.data
        page['geral']['nivel_de_agregacao'] = form.nivelDeAgregacao.data
        
        page['ciclo_de_vida']['versao'] = form.versao.data
        page['ciclo_de_vida']['status'] = form.status.data
        page['ciclo_de_vida']['contribuinte']['entidade'] = form.entidade.data
        page['ciclo_de_vida']['contribuinte']['data'] = form.data.data
        page['ciclo_de_vida']['contribuinte']['papel'] = form.papel.data
        
        page['meta_metadados']['identificador']['catalogo'] = form.i_catalogo.data
        page['meta_metadados']['identificador']['entrada'] = form.i_entrada.data
        page['meta_metadados']['contribuinte']['entidade'] = form.c_entidade.data
        page['meta_metadados']['contribuinte']['data'] = form.c_data.data
        page['meta_metadados']['contribuinte']['papel'] = form.c_papel.data
        page['meta_metadados']['esquema_de_metadados'] = form.esquema_de_metadados.data
        page['meta_metadados']['idioma'] = form.m_idioma.data
        
        page['metadados_tecnicos']['formato'] = form.m_formato.data
        page['metadados_tecnicos']['tamanho'] = form.m_tamanho.data
        page['metadados_tecnicos']['localizacao'] = form.m_localizacao.data
        page['metadados_tecnicos']['requisitos'] = form.m_requisitos.data
        page['metadados_tecnicos']['observacoes_de_Instalacoes'] = form.m_observacoes_de_Instalacoes.data
        page['metadados_tecnicos']['outros_requisitos_de_sistema'] = form.m_outros_requisitos_de_sistema.data
        page['metadados_tecnicos']['duracao'] = form.m_duracao.data

        page['aspectos_educacionais']['tipo_de_iteratividade'] = form.ae_tipo_de_iteratividade.data
        page['aspectos_educacionais']['tipo_de_recurso_de_aprendizado'] = form.ae_tipo_de_recurso_de_aprendizado.data
        page['aspectos_educacionais']['nivel_de_interatividade'] = form.ae_nivel_de_interatividade.data
        page['aspectos_educacionais']['densidade_semantica'] = form.ae_densidade_semantica.data
        page['aspectos_educacionais']['usuario_final'] = form.ae_usuario_final.data
        page['aspectos_educacionais']['contexto_de_aprendizagem'] = form.ae_contexto_de_aprendizagem.data
        page['aspectos_educacionais']['idade_recomendada'] = form.ae_idade_recomendada.data
        page['aspectos_educacionais']['grau_de_dificuldade'] = form.ae_grau_de_dificuldade.data
        page['aspectos_educacionais']['tempo_de_aprendizado'] = form.ae_tempo_de_aprendizado.data
        page['aspectos_educacionais']['descricao'] = form.ae_descricao.data
        page['aspectos_educacionais']['linguagem'] = form.ae_linguagem.data

        page['direitos']['custo'] = form.d_custo.data
        page['direitos']['direitos_autorais'] = form.d_direitos_autorais.data
        page['direitos']['descricao'] = form.d_descricao.data

        page['relacoes']['genero'] = form.r_genero.data
        page['relacoes']['recurso']['referencias'] = form.r_recurso_referencias.data
        page['relacoes']['recurso']['links_externos'] = form.r_recurso_links_externos.data

        page['classificacao']['finalidade'] = form.c_finalidade.data
        page['classificacao']['diretorio'] = form.c_diretorio.data
        page['classificacao']['descricao'] = form.c_descricao.data
        page['classificacao']['palavra_chave'] = form.c_palavra_chave.data

        page['conteudo']['data'] = form.cont_data.data
        page['conteudo']['entidade'] = form.cont_entidade.data 
        page['conteudo']['imagens'] = form.cont_imagens.data
        page['conteudo']['comentarios'] = form.cont_comentarios.data
          
        db.update("learning_object", page)
        return redirect(url_for("listarPage", pageNumber=pageNumber))
    else:
        form.titulo.data = page['geral']['titulo']
        form.idioma.data = page['geral']['idioma']
        form.descricao.data = page['geral']['descricao']
        form.palavrasChave.data = page['geral']['palavras_chave']
        form.cobertura.data = page['geral']['cobertura']
        form.estrutura.data = page['geral']['estrutura']
        form.nivelDeAgregacao.data = page['geral']['nivel_de_agregacao']

        form.versao.data = page['ciclo_de_vida']['versao']
        form.status.data = page['ciclo_de_vida']['status']
        form.entidade.data = page['ciclo_de_vida']['contribuinte']['entidade']
        form.data.data = page['ciclo_de_vida']['contribuinte']['data']
        form.papel.data = page['ciclo_de_vida']['contribuinte']['papel']

        form.i_catalogo.data = page['meta_metadados']['identificador']['catalogo']
        form.i_entrada.data = page['meta_metadados']['identificador']['entrada']
        form.c_entidade.data = page['meta_metadados']['contribuinte']['entidade']
        form.c_data.data = page['meta_metadados']['contribuinte']['data']
        form.c_papel.data = page['meta_metadados']['contribuinte']['papel']
        form.esquema_de_metadados.data = page['meta_metadados']['esquema_de_metadados']
        form.m_idioma.data = page['meta_metadados']['idioma']

        form.m_formato.data = page['metadados_tecnicos']['formato']
        form.m_tamanho.data = page['metadados_tecnicos']['tamanho']
        form.m_localizacao.data = page['metadados_tecnicos']['localizacao']
        form.m_requisitos.data = page['metadados_tecnicos']['requisitos']
        form.m_observacoes_de_Instalacoes.data = page['metadados_tecnicos']['observacoes_de_Instalacoes']
        form.m_outros_requisitos_de_sistema.data = page['metadados_tecnicos']['outros_requisitos_de_sistema']
        form.m_duracao.data = page['metadados_tecnicos']['duracao']

        form.ae_tipo_de_iteratividade.data = page['aspectos_educacionais']['tipo_de_iteratividade']
        form.ae_tipo_de_recurso_de_aprendizado.data = page['aspectos_educacionais']['tipo_de_recurso_de_aprendizado']
        form.ae_nivel_de_interatividade.data = page['aspectos_educacionais']['nivel_de_interatividade']
        form.ae_densidade_semantica.data = page['aspectos_educacionais']['densidade_semantica']
        form.ae_usuario_final.data = page['aspectos_educacionais']['usuario_final']
        form.ae_contexto_de_aprendizagem.data = page['aspectos_educacionais']['contexto_de_aprendizagem']
        form.ae_idade_recomendada.data = page['aspectos_educacionais']['idade_recomendada']
        form.ae_grau_de_dificuldade.data = page['aspectos_educacionais']['grau_de_dificuldade']
        form.ae_tempo_de_aprendizado.data = page['aspectos_educacionais']['tempo_de_aprendizado']
        form.ae_descricao.data = page['aspectos_educacionais']['descricao']
        form.ae_linguagem.data = page['aspectos_educacionais']['linguagem']

        form.d_custo.data = page['direitos']['custo']
        form.d_direitos_autorais.data = page['direitos']['direitos_autorais']
        form.d_descricao.data = page['direitos']['descricao']

        form.r_genero.data = page['relacoes']['genero']
        form.r_recurso_referencias.data = page['relacoes']['recurso']['referencias']
        form.r_recurso_links_externos.data = page['relacoes']['recurso']['links_externos']

        form.c_finalidade.data = page['classificacao']['finalidade']
        form.c_diretorio.data = page['classificacao']['diretorio']
        form.c_descricao.data = page['classificacao']['descricao']
        form.c_palavra_chave.data = page['classificacao']['palavra_chave']

        form.cont_data.data = page['conteudo']['data']
        form.cont_entidade.data = page['conteudo']['entidade']
        form.cont_imagens.data = page['conteudo']['imagens']
        form.cont_comentarios.data = page['conteudo']['comentarios']

        

    return render_template('update/geral.html', page=page, form=form, pageNumber=pageNumber)


# Mostrar Documentação da API
@app.route("/doc-api", methods=['GET'])
@login_required
def documentacaoApi():

    return render_template('docApi.html')

#Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        error = None
        form = loginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            query = db.filter_by('users', {"email": email})
            if query:
                user_bd = query[0]
                is_pass_ok = check_password_hash(user_bd['password'], password)
                if is_pass_ok:
                    user = User(user_bd['name'], user_bd['email'], user_bd['password'])
                    login_user(user)
                    print(user.email)
                    return redirect(url_for("index"))
                else:
                    error = 1
            else:
                error = 1
        else:
            print("Não Validade")
        return render_template('login.html', form=form, error=error)
    else:
        return redirect(url_for("index"))


#Logout
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))




#Profile
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = profileForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        current_password = form.current_password.data
        new_password = form.new_password.data
        repeat_new_password = form.repeat_new_password.data
        # Saber se email é o mesmo
        query = db.filter_by('users', {"email": email})
        if query:
            user_bd = query[0]
            is_email_used = True
            is_email_same = (user_bd['email'] == current_user.email)
        else:
            is_email_used = False
            is_email_same = False
        if not is_email_used or is_email_same:
            #verificar se a senha atual é igual
            user_bd = db.filter_by('users', {"email": current_user.email})
            user_bd = user_bd[0]
            is_pass_ok = check_password_hash(user_bd['password'], current_password)
            if is_pass_ok:
                if new_password == repeat_new_password:
                    user_bd['name'] = name
                    user_bd['password'] = new_password
                    user_bd['email'] = email

                    
                    db.update("users", user_bd)
                    return redirect(url_for("index"))
                else:
                    error = 3 # Nova Senha Não coincide
            else:
                error = 2 #Senha atual está errada
        else:
            error = 1 #Email está em uso e não é o mesmo
    else:
        form.name.data = current_user.name
        form.email.data = current_user.email
    
    return render_template('profile.html', form=form, error=error)
    




#Criar Conta
@app.route("/createaccount", methods=['GET', 'POST'])
def createAccount():
    if not current_user.is_authenticated:
        error = None
        form = createAccountForm()
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            password2 = form.repeat_password.data
            query = db.filter_by('users', {"email": email})
            if not query:
                if password == password2:
                    user = User(name, email, password)
                    db.create("users", user)
                    login_user(user)
                    return redirect(url_for("index"))
                else:
                    error = 2 #Senhas são diferentes
            else:
                error = 1 #Email já cadastrado
        else:
            pass

        return render_template('register.html', form=form, error=error)
    else:
        return redirect(url_for("index"))
    


@app.errorhandler(404)
def errorPage(e):
    return render_template('404.html')
    


@app.errorhandler(401)
def page_not_found(e):
    return redirect(url_for("login"))
