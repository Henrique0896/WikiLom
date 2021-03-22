from app import db
from app.models.util import get_most_used_words, get_images


class LearningObject(object):
    def __init__(self, wikipedia_obj):
        self.geral = {
            "id": wikipedia_obj.pageid,
            "titulo": wikipedia_obj.title,
            "idioma": "English",
            "descricao": wikipedia_obj.summary,
            "palavras_chave": get_most_used_words(wikipedia_obj.summary, 5),
            "cobertura": None,
            "estrutura": None,
            "nivel_de_agregacao": None,
        }
        self.ciclo_de_vida = {
            "versao": wikipedia_obj.revision_id,
            "status": None,
            "contribuinte": {
                "entidade": None,
                "data": None,
                "papel": None
            }
        }
        self.meta_metadados = {
            "identificador": {
                "catalogo": None,
                "entrada": None
            },
            "contribuinte": {
                "entidade": "Wikipedia",
                "data": None,
                "papel": None,
            },
            "esquema_de_metadados": "IEEE LOM",
            "idioma": "Português"
        }
        self.metadados_tecnicos = {
            "formato": "text/html",
            "tamanho": len(list(wikipedia_obj.content)),
            "localizacao": wikipedia_obj.url,
            "requisitos": None,
            "observacoes_de_Instalacoes": None,
            "outros_requisitos_de_sistema": None,
            "duracao": None
        }
        self.aspectos_educacionais = {
            "tipo_de_iteratividade": "Expositiva",
            "tipo_de_recurso_de_aprendizado": "Texto narrativo",
            "nivel_de_interatividade": "Pequena",
            "densidade_semantica": "Alta",
            "usuario_final": "Público geral",
            "contexto_de_aprendizagem": None,
            "idade_recomendada": "Adulto",
            "grau_de_dificuldade": None,
            "tempo_de_aprendizado": None,
            "descricao": None,
            "linguagem": "Português"
        }
        self.direitos = {
            "custo": 0.0,
            "direitos_autorais": "Domínio público",
            "descricao": None
        }
        self.relacoes = {
            "genero": "Fontes Externas",
            "recurso": {
                "referencias": wikipedia_obj.references,
                "links_externos": wikipedia_obj.links
            }
        }
        self.classificacao = {
            "finalidade": None,
            "diretorio": wikipedia_obj.url,
            "descricao": None,
            "palavra_chave": None
        }
        self.conteudo = {
            "data": None,
            "entidade": wikipedia_obj.content,
            "imagens": wikipedia_obj.images,
            "comentarios": None,
        }

    def get_as_json(self):
        return self.__dict__