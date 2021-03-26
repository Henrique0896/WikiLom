#Neste dict vão ser salvas todas as keys de acordo com cada campo do formato LOM para poderem
#ser recuperadas e possibilitar filtragem no banco. AS keys serão chamadas em controllers.default

keys = {
    "geral":{
        0: "geral.id",
        1: "geral.titulo",
        2: "geral.idioma",
        3: "geral.descricao",
        4: "geral.palavras_chave",
        5: "geral.cobertura",
        6: "geral.estrutura",
        7: "geral.nivel_de_agregacao"
    },
    "ciclo_de_vida":{
        0: "ciclo_de_vida.versao",
        1: "ciclo_de_vida.status",
        2: "ciclo_de_vida.contribuinte.entidade",
        3: "ciclo_de_vida.contribuinte.data",
        4: "ciclo_de_vida.contribuinte.papel"
    },
    "meta_metadados":{
        0: "meta_metadados.identificador.catalogo",
        1: "meta_metadados.identificador.entrada",
        2: "meta_metadados.contribuinte.entidade",
        3: "meta_metadados.contribuinte.data",
        4: "meta_metadados.contribuinte.papel",
        5: "meta_metadados.esquema_de_metadados",
        6: "meta_metadados.idioma"
    },
    "metadados_tecnicos":{
        0: "metadados_tecnicos.formato",
        1: "metadados_tecnicos.tamanho",
        2: "metadados_tecnicos.localizacao",
        3: "metadados_tecnicos.requisitos",
        4: "metadados_tecnicos.observacoes_de_Instalacoes",
        5: "metadados_tecnicos.outros_requisitos_de_sistema",
        6: "metadados_tecnicos.duracao"
    },
     "aspectos_educacionais":{
        0: "aspectos_educacionais.tipo_de_iteratividade",
        1: "aspectos_educacionais.tipo_de_recurso_de_aprendizado",
        2: "aspectos_educacionais.nivel_de_interatividade",
        3: "aspectos_educacionais.densidade_semantica",
        4: "aspectos_educacionais.usuario_final",
        5: "aspectos_educacionais.contexto_de_aprendizagem",
        6: "aspectos_educacionais.idade_recomendada",
        7: "aspectos_educacionais.grau_de_dificuldade",
        8: "aspectos_educacionais.tempo_de_aprendizado",
        9: "aspectos_educacionais.descricao",
        10: "aspectos_educacionais.linguagem"
    },
    "direitos":{
        0: "direitos.custo",
        1: "direitos.direitos_autorais",
        2: "direitos.descricao"
    },
    "relacoes":{
        0: "relacoes.genero",
        1: "relacoes.recurso.referencias",
        2: "relacoes.recurso.links_externos"
    },
    "classificacao":{
        0: "classificacao.finalidade",
        1: "classificacao.diretorio",
        2: "classificacao.descricao",
        3: "classificacao.palavra_chave"
    },
       "conteudo":{
        0: "conteudo.data",
        1: "conteudo.entidade",
        2: "conteudo.imagens",
        3: "conteudo.comentarios"
       }
}
        
