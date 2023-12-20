# Importação de bibliotecas necessárias
from dash import Input, Output, State

import dash
import networkx as nx
import plotly.graph_objects as go
import dash_bootstrap_components as dbc 
# Importação de funções personalizadas
from graph_utils import  update_graph
from data_utils import load_data, create_graph
import layout
import callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = load_data('teste.csv', nrows=5000)
df['notificacoes_proprias'] = df.groupby('mun_noti')['notifications'].transform('sum')
df['notificacoes_total'] = df.groupby('mun_noti')['notifications'].transform('sum')

G = create_graph(df)
pos = nx.get_node_attributes(G, 'pos')
node_color = ['blue' if node in df['mun_noti'].values else 'green' for node in G.nodes()]

app.layout = layout.create_layout(df)

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
        Input('search-input', 'value')  # Novo input para o campo de busca
    ]
)
def update_graph_callback(selected_cidade, click_data, show_all_clicks, hide_matching_municipality, search_input):
    # Garanta que o valor do campo de busca não seja None ou uma string vazia
    if search_input is None or search_input == '':
        search_input = None

    return callbacks.update_graph_callback(selected_cidade, click_data, show_all_clicks, df, G, pos, hide_matching_municipality, search_input)
if __name__ == '__main__':
    app.run_server(debug=True)

