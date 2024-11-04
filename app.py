# Importação de bibliotecas necessárias
from dash import Dash, html, dcc, Input, Output, exceptions
from data_utils import load_data, create_graph
import networkx as nx
import plotly.express as px
import pandas as pd


import layout
import callbacks

# Definição do aplicativo Dash
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server

# Carregar os dados
df = pd.read_csv('Definitivo.csv', sep=',')
df1 = pd.read_csv('corredor.csv', sep=',')

df['notificacoes_proprias'] = df.groupby('mun_noti')['notifications'].transform('sum')
df['notificacoes_total'] = df.groupby('mun_noti')['notifications'].transform('sum')
G = create_graph(df)
pos = nx.get_node_attributes(G, 'pos')
node_color = ['blue' if node in df['mun_noti'].values else 'green' for node in G.nodes()]

# Definição do layout do aplicativo Dash
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

# Callback para renderizar os diferentes layouts com base na URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return layout.create_layout(df)
    else:
        return '404 - Página não encontrada'
    
# Callback para atualizar o conteúdo quando o botão de atualização é clicado
@app.callback(Output('url', 'pathname'), [Input('update-button', 'n_clicks')])
def refresh_page(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        return '/'
    raise exceptions.PreventUpdate

@app.callback(
    [
        Output('grafo-direcional', 'figure'),
        Output('grafico-colunas', 'figure'),
        Output('cidade-dropdown', 'value'),
        Output('endemic-corridor-chart', 'figure')
    ],
    [
        Input('cidade-dropdown', 'value'),
        Input('grafo-direcional', 'clickData'),
        Input('hide-matching-municipality', 'value'),
        Input('ano-range-slider', 'value'),
        Input('update-button', 'n_clicks'),  
    ]
)
def update_graph_callback(selected_cidade, click_data, hide_matching_municipality, selected_ano, update_clicks):
    if update_clicks is not None and update_clicks > 0:
        # Lógica de atualização aqui
        grafo_direcional, grafico_colunas, selected_city = callbacks.update_graph_callback('Todas', None, df, G, pos, hide_matching_municipality, selected_ano)
    else:
        if selected_ano and 'Todos' not in selected_ano:
            df_filtered = df[df['ano'].between(int(selected_ano[0]), int(selected_ano[1]))]
        else:
            df_filtered = df.copy()

        grafo_direcional, grafico_colunas, selected_city = callbacks.update_graph_callback(selected_cidade, click_data, df_filtered, G, pos, hide_matching_municipality, selected_ano)

    endemic_corridor_chart = callbacks.create_endemic_corridor(df1, selected_city, selected_ano)

    return grafo_direcional, grafico_colunas, selected_city, endemic_corridor_chart

@app.callback(
    Output('line-chart', 'figure'),
    [Input('cidade-dropdown', 'value'),
     Input('ano-range-slider', 'value')]
)
def update_line_chart(selected_cidade, selected_ano):
    df_filtered = df

    if selected_ano and len(selected_ano) == 2:
        df_filtered = df_filtered[df_filtered['ano'].between(int(selected_ano[0]), int(selected_ano[1]))]

    filtered_df = df_filtered[df_filtered['mun_noti'] == selected_cidade]

    selected_city_name = filtered_df['nome_noti'].iloc[0] if not filtered_df.empty else "Todos os municípios"

    if selected_cidade == 'Todas':
        df_aggregated = df_filtered.groupby('ano')['notifications'].sum().reset_index()
    else:
        df_aggregated = df_filtered[df_filtered['mun_noti'] == selected_cidade].groupby('ano')['notifications'].sum().reset_index()

    line_chart = px.line(df_aggregated, x='ano', y='notifications', markers=True, title=f'Evolução da Malária de {selected_ano[0]} a {selected_ano[1]} em {selected_city_name}')

    line_chart.update_layout(
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ),
        xaxis_title='Ano',
        yaxis_title='Número de Notificações',
        height=400,
        title={
            'text': f'<b>Série histórica (notificações) em {selected_city_name} de {selected_ano[0]} - {selected_ano[1]}</b>'
        }
    )

    return line_chart

@app.callback(
    Output('intervalo-selecionado', 'children'),
    [Input('ano-range-slider', 'value')]
)
def update_intervalo_selecionado(intervalo):
    if intervalo is None or len(intervalo) != 2:
        return 'Intervalo não selecionado'

    inicio, fim = intervalo
    return f'Intervalo Selecionado: {inicio} a {fim}'

# Defina o valor padrão para os últimos 3 anos
@app.callback(
    Output('ano-range-slider', 'value'),
    [Input('ano-range-slider', 'min'),
     Input('ano-range-slider', 'max')]
)
def set_default_intervalo(min_value, max_value):
    # Defina os últimos 3 anos como valor padrão
    default_inicio = max_value - 2
    default_fim = max_value

    return [default_inicio, default_fim]

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)

