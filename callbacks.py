import plotly.graph_objects as go
from graph_utils import update_graph

def update_graph_callback(selected_city, click_data, show_all_clicks, df, G, pos, hide_matching_municipality=None, search_input=None):
    print(f"Selected city: {selected_city}")
    print(f"Search input: {search_input}")

    if show_all_clicks and show_all_clicks > 0:
        selected_city = 'Todas'
        show_all_clicks = 0
    elif click_data and 'points' in click_data:
        clicked_node_code = click_data['points'][0]['customdata']
        selected_city = clicked_node_code

    df_filtered = df[df['nome_noti'].str.contains(search_input, case=False, na=False)] if search_input else df

    if hide_matching_municipality and 'hide' in hide_matching_municipality:
        df_filtered = df_filtered[df_filtered['mun_noti'] != df_filtered['mun_infe']]

    grafo_direcional = update_graph(selected_city, df_filtered, G, pos)

    if selected_city == 'Todas':
        grafico_colunas = {
            'data': [],
            'layout': {
                'title': 'Notificações por Município de Infecção',
                'height': 700,
                'width': 700,
            }
        }
    else:
        dados_grafico_colunas = df_filtered[df_filtered['mun_noti'] == selected_city].groupby('mun_infe').agg(
            {'notifications': 'sum', 'nome_infe': 'first', 'mun_noti': 'first'}
        ).reset_index().sort_values(by='notifications', ascending=True).tail(10)

        dados_grafico_colunas['percentagem'] = (dados_grafico_colunas['notifications'] / df_filtered[df_filtered['mun_noti'] == selected_city]['notifications'].sum()) * 100

        filtered_df = df_filtered[df_filtered['mun_noti'] == selected_city]
        total_notifications_mun_noti = filtered_df['notificacoes_total'].iloc[0] if not filtered_df.empty else 0
        selected_city_name = filtered_df['nome_noti'].iloc[0] if not filtered_df.empty else "Selected Municipality"

        trace_mun_infe = go.Bar(
            y=dados_grafico_colunas['nome_infe'],
            x=dados_grafico_colunas['notifications'],
            text=[f'{(notif/total_notifications_mun_noti)*100:.2f}%' for notif in dados_grafico_colunas['notifications']],
            hoverinfo='text+x',
            orientation='h',
            name='mun_infe',
        )

        grafico_colunas = {
            'data': [trace_mun_infe],
            'layout': {
                'title': f'TOP 10 Municípios de Infecção (Relacionado a {selected_city_name})',
                'height': 700,
                'width': 700,
                'yaxis': {
                    'tickmode': 'linear',
                    'tickvals': dados_grafico_colunas['nome_infe'],
                    'ticktext': dados_grafico_colunas['nome_infe'],
                    'dtick': 1,
                    'automargin': True,
                },
                'xaxis': {'title': 'Notificações'},
                'margin': {'l': 150},
            }
        }

    return grafo_direcional, grafico_colunas, selected_city, show_all_clicks
