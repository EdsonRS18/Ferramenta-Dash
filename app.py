# Importação de bibliotecas necessárias
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc 
from data_utils import load_data, create_graph
import networkx as nx
import layout
import malaria_layout
import callbacks

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# Carregar os dados
df = load_data('teste.csv', nrows=15000)
df['notificacoes_proprias'] = df.groupby('mun_noti')['notifications'].transform('sum')
df['notificacoes_total'] = df['notificacoes_proprias'].groupby(df['mun_noti']).transform('sum')
G = create_graph(df)
pos = nx.get_node_attributes(G, 'pos')
node_color = ['blue' if node in df['mun_noti'].values else 'green' for node in G.nodes()]

# Definição dos layouts
layout_principal = html.Div([
    layout.create_layout(df),  # Layout principal
])

pagina_malaria = html.Div([
    malaria_layout.create_malaria_layout(df),  # Página sobre malária
])

# Callback para alternar entre páginas
@app.callback(Output('page-content', 'children'), [Input('btn-navegacao', 'n_clicks')])
def alternar_paginas(n_clicks):
    if n_clicks is None:
        return layout_principal  # Define a página inicial

    if n_clicks % 2 == 0:  # Alternar entre as páginas a cada clique no botão
        return layout_principal
    else:
        return pagina_malaria

# Layout completo da aplicação com o botão de navegação
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Button("Alternar Páginas", id='btn-navegacao', color="primary", className="mr-1"),
    html.Div(id='page-content')
])

# Callback para atualização dos componentes
@app.callback(
    Output('grafo-direcional', 'figure'),
    Output('grafico-colunas', 'figure'),
    Output('cidade-dropdown', 'value'),
    Output('show-all-button', 'n_clicks'),
    [Input('cidade-dropdown', 'value')],
    [Input('grafo-direcional', 'clickData')],
    [Input('show-all-button', 'n_clicks')],
    [Input('hide-matching-municipality', 'value')],
    [Input('search-input', 'value')]
)

    
def update_graph_callback(selected_cidade, click_data, show_all_clicks, hide_matching_municipality, search_input):
    # Lógica para processar os inputs e atualizar os componentes
    # Esta função retorna os valores atualizados para os componentes especificados nos Outputs
    if search_input in (None, ''):
        search_input = None

    return callbacks.update_graph_callback(selected_cidade, click_data, show_all_clicks, df, G, pos, hide_matching_municipality, search_input)

if __name__ == '__main__':
    app.run_server(debug=True)
