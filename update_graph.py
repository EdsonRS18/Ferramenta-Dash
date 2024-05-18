# Importação de bibliotecas necessárias
import plotly.graph_objects as go
import networkx as nx
from data_utils import create_graph
from nodes import create_node_trace
from aresta import create_edge_trace

def update_graph(selected_city, data, G, pos, hide_matching_municipality=False):
    print(f"Updating graph for selected_city: {selected_city}")

    if selected_city == 'Todas':
        filtered_df = data
        include_edges = False
    else:
        filtered_df = data[data['mun_noti'] == selected_city]
        include_edges = True

    G_selected = create_graph(filtered_df)
    pos_selected = nx.get_node_attributes(G_selected, 'pos')

    # Passando a variável pos_selected e hide_matching_municipality para a função create_node_trace
    node_trace_selected = create_node_trace(G_selected, filtered_df, selected_city, pos_selected, hide_matching_municipality)

    if include_edges:
        edge_trace_selected = create_edge_trace(G_selected, filtered_df, pos_selected)
        traces = [edge_trace_selected, node_trace_selected]
    else:
        traces = [node_trace_selected]

    if selected_city != 'Todas':
        selected_city_name = filtered_df['nome_noti'].iloc[0]
        total_notifications = filtered_df['notifications'].sum()
        title = f'<b>Número de notificações por município</b><br><b>(Município selecionado {selected_city_name})<b>'
    else:
        selected_city_name = "Todos"
        title = f'<b>Número de notificações por município</b><br><b>(Município selecionado: {selected_city_name})<b>'

    return {
        'data': traces,
        'layout': {
            'mapbox': {
                'center': dict(lat=filtered_df['latitude_noti'].mean(), lon=filtered_df['longitude_noti'].mean()),
                'zoom': 3.4,
                'style': "open-street-map",
            },
            'title': title,
            'height': 700
        }
    }



