# Importação de bibliotecas necessárias
import plotly.graph_objects as go
import networkx as nx
from dash import dcc, html, Input, Output
from data_utils import create_graph



def create_node_text(node, node_df):
    node_type = 'mun_noti' if node in node_df['mun_noti'].values else 'mun_infe'
    node_name = node_df.loc[node_df[node_type] == node, 'nome_noti' if node_type == 'mun_noti' else 'nome_infe'].iloc[0]
    node_code = node_df.loc[node_df[node_type] == node, 'mun_noti' if node_type == 'mun_noti' else 'mun_infe'].iloc[0]

    if node_type == 'mun_noti':
        filtered_node_df = node_df[(node_df['mun_noti'] == node) & (node_df['mun_infe'] == node)]
        if not filtered_node_df.empty:
            node_notifications = filtered_node_df.iloc [0]['notifications']
        else:
            node_notifications = 0  # ou qualquer outro valor padrão

        node_total_notifications = node_df[node_df['mun_noti'] == node]['notifications'].sum()
        return f"{node_name} ({node_code})<br>Notifications: {node_notifications}<br>Total Notifications: {node_total_notifications}"
    else:
        node_notifications = node_df[node_df[node_type] == node]['notifications'].iloc[0]
        return f"{node_name} ({node_code})<br>Notifications: {node_notifications}"

def determine_node_size(node, node_df, selected_city=None):
    node_type = 'mun_noti' if node in node_df['mun_noti'].values else 'mun_infe'

    if selected_city and selected_city != 'Todas':
        # Quando uma cidade específica é selecionada
        if node_type == 'mun_noti':
            node_notifications = node_df[node_df['mun_noti'] == node]['notifications'].sum()
        else:
            node_notifications = node_df[node_df['mun_infe'] == node]['notifications'].sum()
    else:
        # Quando nenhuma cidade ou 'Todas' são selecionadas
        if node_type == 'mun_noti':
            node_total_notifications = node_df[node_df['mun_noti'] == node]['notifications'].sum()
        else:
            node_notifications = node_df[node_df['mun_infe'] == node]['notifications'].sum()

    base_size = 4

    if selected_city and selected_city != 'Todas' and node_type == 'mun_noti':
        # Redimensionamento baseado em 'notifications' quando uma cidade específica é selecionada
        if node_notifications < 100:
                size = base_size
        elif 101 <= node_notifications < 500:
            size = base_size + 10
        elif 501 <= node_notifications < 2000:
            size = base_size + 15
        else:
            size = base_size + 200
    else:
        # Redimensionamento baseado em 'total_notifications' quando nenhuma cidade ou 'Todas' são selecionadas
        if node_type == 'mun_noti':
            if node_total_notifications < 5000:
                size = base_size + 5
            elif 5000 <= node_total_notifications < 10000:
                size = base_size + 13
            elif 10000 <= node_total_notifications < 16000:
                size = base_size + 19
            else:
                size = base_size + 50
        else:
            if node_notifications < 100:
                size = base_size
            elif 101 <= node_notifications < 500:
                size = base_size + 10
            elif 501 <= node_notifications < 2000:
                size = base_size + 15
            else:
                size = base_size + 20

    return size




def determine_node_color(node, node_df):
    node_type = 'mun_noti' if node in node_df['mun_noti'].values else 'mun_infe'
    return 'blue' if node_type == 'mun_noti' else 'green'

def create_node_trace(G, node_df, selected_city=None, pos=None):
    node_text = []
    node_size = []
    node_color = []
    visible_nodes = set()

    # Defina os nós visíveis com base na seleção
    if selected_city == 'Todas':
        visible_nodes.update(node_df['mun_noti'].values)
    else:
        visible_nodes.update(G.nodes())

    # Crie os traços para os nós visíveis
    latitudes = []
    longitudes = []

    for node in visible_nodes:
        # Criação dos textos dos nós
        text = create_node_text(node, node_df)
        node_text.append(text)

        # Determinação do tamanho dos nós
        size = determine_node_size(node, node_df, selected_city)
        node_size.append(size)

        # Determinação das cores dos nós
        color = determine_node_color(node, node_df)
        node_color.append(color)

        # Manter as posições dos nós consistentes
        latitudes.append(pos[node][0])
        longitudes.append(pos[node][1])

    return go.Scattermapbox(
        lat=latitudes,
        lon=longitudes,
        mode='markers',
        marker=dict(size=node_size, color=node_color),
        text=node_text,
        hoverinfo='text',
        customdata=[node_code for node_code in visible_nodes]  # Adiciona dados personalizados para capturar o código do nó
    )

def create_edge_trace(G, edge_df, pos):
    edge_text = []

    for _, row in edge_df.iterrows():
        edge_text.append(f"Origem: {row['mun_noti']} <br> Destino: {row['mun_infe']}")

    edge_trace = go.Scattermapbox(
        lat=[],
        lon=[],
        mode='lines',
        line=dict(width=1, color='red'),
        hoverinfo='text',
        text=edge_text,
    )

    for _, row in edge_df.iterrows():
        node_noti, node_infe = row['mun_noti'], row['mun_infe']
        x0, y0 = pos[node_noti]
        x1, y1 = pos[node_infe]
        edge_trace['lat'] += (x0, x1, None)
        edge_trace['lon'] += (y0, y1, None)

    return edge_trace

def update_graph(selected_cidade, data, G, pos):
    print(f"Updating graph for selected_cidade: {selected_cidade}")

    if selected_cidade == 'Todas':
        filtered_df = data
        include_edges = False
    else:
        filtered_df = data[data['mun_noti'] == selected_cidade]
        include_edges = True
    
    G_selected = create_graph(filtered_df)
    pos_selected = nx.get_node_attributes(G_selected, 'pos')

    # Passando a variável pos_selected para a função create_node_trace
    node_trace_selected = create_node_trace(G_selected, filtered_df, selected_cidade, pos_selected)
    
    if include_edges:
        edge_trace_selected = create_edge_trace(G_selected, filtered_df, pos_selected)
        traces = [edge_trace_selected, node_trace_selected]
    else:
        traces = [node_trace_selected]

    if selected_cidade != 'Todas':
        # Ajuste para selecionar o nome correto do município
        selected_city_name = filtered_df['nome_noti'].iloc[0]
        # Adicionando o número de notificações ao título
        total_notifications = filtered_df['notifications'].sum()
        title = f'Município Selecionado: {selected_city_name}'
    else:
        selected_city_name = "Todas as cidades"
        title = f'Município Selecionado: {selected_city_name}'

    return {
        'data': traces,
        'layout': {
            'mapbox': {
                'center': dict(lat=filtered_df['latitude_noti'].mean(), lon=filtered_df['longitude_noti'].mean()),
                'zoom': 3.4,
                'style': "open-street-map",
            },
            'title': title,
            'height': 700,
            'width': 700,
        }
    }
