import plotly.graph_objects as go


def create_node_text(node, node_df):
    node_type = 'mun_noti' if node in node_df['mun_noti'].values else 'mun_infe'
    node_name = node_df.loc[node_df[node_type] == node, 'nome_noti' if node_type == 'mun_noti' else 'nome_infe'].iloc[0]
    node_code = node_df.loc[node_df[node_type] == node, 'mun_noti' if node_type == 'mun_noti' else 'mun_infe'].iloc[0]

    if node_type == 'mun_noti':
        # Filtra linhas onde mun_noti é igual a mun_infe e calcula a soma das notificações
        node_notifications = node_df[(node_df['mun_noti'] == node) & (node_df['mun_infe'] == node)]['notifications'].sum()

        # Soma total de notificações apenas para o nó específico
        total_notifications = node_df[node_df[node_type] == node]['notifications'].sum()

        return f"{node_name} ({node_code})<br>Notifications: {node_notifications}<br>Total Notifications: {total_notifications}"
    else:
        # Quando o nó é do tipo 'mun_infe', mostra apenas as notificações desse nó
        node_notifications = node_df[node_df[node_type] == node]['notifications'].iloc[0]
        return f"{node_name} ({node_code})<br>Notifications: {node_notifications}"



def determine_node_size(node, node_df, selected_city=None):
    node_type = 'mun_noti' if node in node_df['mun_noti'].values else 'mun_infe'

    if selected_city and selected_city != 'Todas' and node_type == 'mun_noti':
        # Quando um mun_noti está selecionado, redimensiona com base em 'notifications'
        node_notifications = node_df[node_df['mun_noti'] == node]['notifications'].sum()
        if node_notifications < 100:
            size = 10
        elif 101 <= node_notifications < 500:
            size = 20
        elif 501 <= node_notifications < 2000:
            size = 30
        else:
            size = 40
    else:
        # Quando nenhum mun_noti está selecionado ou é tela inicial, redimensiona com base em 'total_notifications'
        total_notifications = node_df[node_df['mun_noti'] == node]['notifications'].sum()
        if total_notifications < 5000:
            size = 10
        elif 5000 <= total_notifications < 10000:
            size = 20
        elif 10000 <= total_notifications < 16000:
            size = 30
        else:
            size = 40

    return size

def determine_node_color(node, node_df):
    node_type = 'mun_noti' if node in node_df['mun_noti'].values else 'mun_infe'
    return 'blue' if node_type == 'mun_noti' else 'green'

def create_node_trace(G, node_df, selected_city=None, pos=None, hide_matching_municipality=False):
    node_text = []
    node_size = []
    node_color = []
    visible_nodes = set()

    # Defina os nós visíveis com base na seleção
    if selected_city == 'Todas':
        visible_nodes.update(node_df['mun_noti'].values)
    else:
        visible_nodes.update(G.nodes())

    if hide_matching_municipality:
        # Se a opção hide_matching_municipality estiver ativada, remova o nó correspondente
        visible_nodes.discard(node_df['mun_noti'].iloc[0])

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
        customdata=[node_code for node_code in visible_nodes]
    )