import plotly.graph_objects as go


def create_edge_trace(G, edge_df, pos):
    edge_text = []

    #for _, row in edge_df.iterrows():
        #edge_text.append(f"Origem: {row['mun_noti']} <br> Destino: {row['mun_infe']}")

    edge_trace = go.Scattermapbox(
        lat=[],
        lon=[],
        mode='lines',
        line=dict(width=1, color='LightPink'),
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