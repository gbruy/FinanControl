import plotly.express as px
from app.models import Transacao

def gerar_grafico_despesas_mensais(usuario_id):
    transacoes = Transacao.query.filter_by(usuario_id=usuario_id).all()

    #Calcular valores mensai
    despesas_mensais = {}
    for t in transacoes:
        if t.tipo == 'Despesa':
            mes = t.data.strftime('%b')
            despesas_mensais[mes] = despesas_mensais.get(mes, 0) + t.valor

    meses = list(despesas_mensais.keys())
    valores_despesas = list(despesas_mensais.values())


    #criar grafico de barras
    fig = px.bar(
        x=meses,
        y=valores_despesas,
        title = "Total de despesas por Mes",
        labels={'x': 'Meses', 'y': 'Valores'}
    )
    return fig.to_html(full_html=False)

def gerar_grafico_receitas_por_categoria(usuario_id):
    transacoes = Transacao.query.filter_by(usuario_id=usuario_id).all()

    #Calcular receitas por categorias e mes 
    dados_receitas = {}
    for t in transacoes:
        if t.tipo == 'Receita' and t.categoria:
            mes = t.data.strftime('%b')
            categoria_nome = t.categoria.nome
            if mes not in dados_receitas:
                dados_receitas[mes] = {}
            dados_receitas[mes][categoria_nome]= dados_receitas[mes].get(categoria_nome, 0) + t.valor
    
    #Transformar os dados em formato adequado para Ploty
    meses = []
    categorias = []
    valores = []
    for mes, categoria_mes in dados_receitas.items():
        for categoria, valor in categoria_mes.items():
            meses.append(mes)
            categorias.append(categoria)
            valores.append(valor)

    #criar grafico
    fig = px.bar(
        x=meses,
        y=valores,
        color=categorias,
        title="Receitas por Mes",
        labels={'x': 'Meses', 'y':'Valores','color': 'Categorias'},
        barmode='group'
    )
    return fig.to_html(full_html=False)
