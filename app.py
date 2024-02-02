# Importação de bibliotecas necessárias
from dash import Dash, html, dcc, Input, Output
from dash.dependencies import Input, Output
import pandas as pd
from data_utils import load_data, create_graph
import networkx as nx
import dash_bootstrap_components as dbc 
# Importação de funções personalizadas
from malaria_layout import create_malaria_layout
from info_layout import create_info_layout
import layout
import callbacks

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# Carregar os dados
df = load_data('Definitivo.csv', nrows=15000)
df['notificacoes_proprias'] = df.groupby('mun_noti')['notifications'].transform('sum')
df['notificacoes_total'] = df.groupby('mun_noti')['notifications'].transform('sum')
G = create_graph(df)
pos = nx.get_node_attributes(G, 'pos')
node_color = ['blue' if node in df['mun_noti'].values else 'green' for node in G.nodes()]

# Layout completo da aplicação
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return layout.create_layout(df)
    elif pathname == '/pagina_malaria':
        return create_malaria_layout(df)
    elif pathname == '/outra_pagina':
        return create_info_layout(df)
    else:
        return '404 - Página não encontrada'
@app.callback(
    [
        Output('grafo-direcional', 'figure'),
        Output('grafico-colunas', 'figure'),
        Output('cidade-dropdown', 'value'),
        Output('show-all-button', 'n_clicks')
    ],
    [
        Input('cidade-dropdown', 'value'),
        Input('grafo-direcional', 'clickData'),
        Input('show-all-button', 'n_clicks'),
        Input('hide-matching-municipality', 'value'),
        Input('search-input', 'value'),
        Input('ano-dropdown', 'value')  # Adicione 'ano-dropdown' como um Input
        

    ]
)
def update_graph_callback(selected_cidade, click_data, show_all_clicks, hide_matching_municipality, search_input, selected_ano):
    # Garanta que o valor do campo de busca não seja None ou uma string vazia
    if search_input is None or search_input == '':
        search_input = None

    # Redefina o estado ou valores que você deseja reiniciar
    if show_all_clicks > 0:
        selected_cidade = 'Todas'

    # Filtrar o DataFrame pelo ano selecionado
    if selected_ano and selected_ano != 'Todos':
        df_filtered = df[df['ano'] == int(selected_ano)]
    else:
        df_filtered = df.copy()

    return callbacks.update_graph_callback(selected_cidade, click_data, show_all_clicks, df_filtered, G, pos, hide_matching_municipality, search_input)

if __name__ == '__main__':
    app.run_server(debug=True)
