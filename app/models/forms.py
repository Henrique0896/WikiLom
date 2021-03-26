from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class campoPesquisa(FlaskForm): 
    pesquisa = StringField("pesquisa", validators=[DataRequired()])

class filtroDeDados(FlaskForm): 
    pesquisa = StringField("pesquisa", validators=[DataRequired()])
    subject = SelectField(u'Campo', choices=[('geral','Geral'), ('ciclo_de_vida','Ciclo de Vida'), ('meta_metadados','Meta Metadados'), ('metadados_tecnicos','Metadados Técnicos'), ('aspectos_educacionais','Aspectos Educacionais'), ('direitos','Direitos'), ('relacoes','Relações'), ('classificacao','Classificação'), ('conteudo','Conteúdo')])


