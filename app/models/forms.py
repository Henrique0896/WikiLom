from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired

class campoPesquisa(FlaskForm): 
    pesquisa = StringField("pesquisa", validators=[DataRequired()])

class filtroDeDados(FlaskForm): 
    pesquisa = StringField("pesquisa", validators=[DataRequired()])
    subject = SelectField(u'Campo', choices=[('geral','Geral'), ('ciclo_de_vida','Ciclo de Vida'),
    ('meta_metadados','Meta Metadados'), ('metadados_tecnicos','Metadados Técnicos'),
    ('aspectos_educacionais','Aspectos Educacionais'), ('direitos','Direitos'),
    ('relacoes','Relações'), ('classificacao','Classificação'), ('conteudo','Conteúdo')])

class updateGeral(FlaskForm): 
    titulo = StringField("titulo", validators=[DataRequired()])
    idioma = StringField("idioma")
    descricao = StringField("descricao")
    palavrasChave = StringField("palavrasChave")
    cobertura = StringField("cobertura")
    estrutura = StringField("estrutura")
    nivelDeAgregacao = StringField("nivelDeAgregacao")

    versao = StringField("versao", validators=[DataRequired()])
    status = StringField("status")
    entidade = StringField("entidade")
    data = StringField("data")
    papel = StringField("papel")

    i_catalogo = StringField("i_catalogo")
    i_entrada = StringField("i_entrada")
    c_entidade = StringField("c_entidade")
    c_data = StringField("c_data")
    c_papel = StringField("c_papel")
    esquema_de_metadados = StringField("esquema_de_metadados")
    m_idioma = StringField("m_idioma")

    m_formato = StringField("m_formato")
    m_tamanho = StringField("m_tamanho")
    m_localizacao = StringField("m_localizacao")
    m_requisitos = StringField("m_requisitos")
    m_observacoes_de_Instalacoes = StringField("m_observacoes_de_Instalacoes")
    m_outros_requisitos_de_sistema = StringField("m_outros_requisitos_de_sistema")
    m_duracao = StringField("m_duracao")

    ae_tipo_de_iteratividade = StringField("ae_tipo_de_iteratividade")
    ae_tipo_de_recurso_de_aprendizado = StringField("ae_tipo_de_recurso_de_aprendizado")
    ae_nivel_de_interatividade = StringField("ae_nivel_de_interatividade")
    ae_densidade_semantica = StringField("ae_densidade_semantica")
    ae_usuario_final = StringField("ae_usuario_final")
    ae_contexto_de_aprendizagem = StringField("ae_contexto_de_aprendizagem")
    ae_idade_recomendada = StringField("ae_idade_recomendada")
    ae_grau_de_dificuldade = StringField("ae_grau_de_dificuldade")
    ae_tempo_de_aprendizado = StringField("ae_tempo_de_aprendizado")
    ae_descricao = StringField("ae_descricao")
    ae_linguagem = StringField("ae_linguagem")

    d_custo = StringField("d_custo")
    d_direitos_autorais = StringField("d_direitos_autorais")
    d_descricao = StringField("d_descricao")

    r_genero = StringField("r_genero")
    r_recurso_referencias = StringField("r_recurso_referencias")
    r_recurso_links_externos = StringField("r_recurso_links_externos")

    c_finalidade = StringField("c_finalidade")
    c_diretorio = StringField("c_diretorio")
    c_descricao = StringField("c_descricao")
    c_palavra_chave = StringField("c_palavra_chave")

    cont_data = StringField("cont_data")
    cont_entidade = StringField("cont_entidade")
    cont_imagens = StringField("cont_imagens")
    cont_comentarios = StringField("cont_comentarios")


class loginForm(FlaskForm): 
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class createAccountForm(FlaskForm): 
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    repeat_password = PasswordField("repeat_password", validators=[DataRequired()])

class profileForm(FlaskForm): 
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    current_password = PasswordField("current_password", validators=[DataRequired()])
    new_password = PasswordField("new_password", validators=[DataRequired()])
    repeat_new_password = PasswordField("repeat_new_password", validators=[DataRequired()])