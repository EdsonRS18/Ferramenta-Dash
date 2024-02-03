# Importação de bibliotecas necessárias
from dash import Dash, html, dcc, Input, Output, exceptions
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
from data_utils import load_data, create_graph
import networkx as nx
import dash_bootstrap_components as dbc 
# Importação de funções personalizadas
from malaria_layout import create_malaria_layout
from info_layout import create_info_layout
import layout
from dash.exceptions import PreventUpdate

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

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
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
    ],
    [
        Input('cidade-dropdown', 'value'),
        Input('grafo-direcional', 'clickData'),
        # Remova a entrada correspondente ao 'show-all-button'
        Input('hide-matching-municipality', 'value'),
        Input('search-input', 'value'),
        Input('ano-dropdown', 'value'),
        Input('update-button', 'n_clicks'),  
    ]
)
def update_graph_callback(selected_cidade, click_data, hide_matching_municipality, search_input, selected_ano, update_clicks):
    if update_clicks is not None and update_clicks > 0:
        # Lógica de atualização aqui
        callbacks.update_graph_callback('Todas', None, df, G, pos, hide_matching_municipality, search_input)
    else:
        if search_input is None or search_input == '':
            search_input = None

        if selected_ano and selected_ano != 'Todos':
            df_filtered = df[df['ano'] == int(selected_ano)]
        else:
            df_filtered = df.copy()

        return callbacks.update_graph_callback(selected_cidade, click_data, df_filtered, G, pos, hide_matching_municipality, search_input)


if __name__ == '__main__':
    app.run_server(debug=True)
