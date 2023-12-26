from dash import html, Input, Output, State
import dash_bootstrap_components as dbc
from dash import dcc
import plotly.graph_objects as go
from graph_utils import update_graph
from data_utils import load_data, create_graph

def update_graph_callback(selected_cidade, click_data, show_all_clicks, df, G, pos, hide_matching_municipality=None, search_input=None):
    print(f"Selected city: {selected_cidade}")
    print(f"Search input: {search_input}")  # Adicione essa linha para verificar o valor inserido no campo de busca

    # Verifique se o botão "Mostrar Todas as Cidades" foi clicado
    if show_all_clicks is not None and show_all_clicks > 0:
        selected_cidade = 'Todas'
        show_all_clicks = 0
    else:
        if click_data and 'points' in click_data:
            clicked_node_code = click_data['points'][0]['customdata']
            selected_cidade = clicked_node_code
    
    if search_input:  # Verifique se há algo no campo de busca
        # Filtre os dados com base no valor inserido no campo de busca
        df_filtered = df[df['nome_noti'].str.contains(search_input, case=False, na=False)]
    else:
        df_filtered = df
    
    if 'hide' in hide_matching_municipality:
        df_filtered = df_filtered[df_filtered['mun_noti'] != df_filtered['mun_infe']]
    
    # Atualize os gráficos com os dados filtrados
    grafo_direcional = update_graph(selected_cidade, df_filtered, G, pos)
    

    if selected_cidade == 'Todas':
        grafico_colunas = {
            'data': [],
            'layout': {
                'title': 'Notificações por Município de Infecção',
                'height': 600,
                'width': 600,
            }
        }
    else:
        dados_grafico_colunas = df_filtered[df_filtered['mun_noti'] == selected_cidade].groupby('mun_infe').agg({'notifications': 'sum', 'nome_infe': 'first', 'mun_noti': 'first'}).reset_index()

        dados_grafico_colunas = dados_grafico_colunas.sort_values(by='notifications', ascending=True).tail(10)

        dados_grafico_colunas['percentagem'] = (dados_grafico_colunas['notifications'] / df_filtered[df_filtered['mun_noti'] == selected_cidade]['notifications'].sum()) * 100

        filtered_df = df_filtered[df_filtered['mun_noti'] == selected_cidade]

        if not filtered_df.empty:
            total_notifications_mun_noti = filtered_df['notificacoes_total'].iloc[0]
            selected_city_name = filtered_df['nome_noti'].iloc[0]  # Obtaining the selected city's name
        else:
            total_notifications_mun_noti = 0
            selected_city_name = "Selected Municipality"

        # Build the trace_mun_infe
        trace_mun_infe = go.Bar(
            y=dados_grafico_colunas['nome_infe'],
            x=dados_grafico_colunas['notifications'],
            text=[f'{(notif/total_notifications_mun_noti)*100:.2f}%' for notif in dados_grafico_colunas['notifications']],
            hoverinfo='text+x',
            orientation='h',
            name='mun_infe',
        )

        # Atualize o título para incluir o nome do município selecionado
        grafico_colunas = {
            'data': [trace_mun_infe],
            'layout': {
                'title': f'TOP 10 Municípios de Infecção (Relacionado a {selected_city_name})',
                'height': 600,
                'width': 600,
                'yaxis': {
                    'tickangle': 0,
                    'tickmode': 'array',
                    'tickvals': dados_grafico_colunas['nome_infe'],
                    'ticktext': dados_grafico_colunas['nome_infe'],
                },
                'xaxis': {'title': 'Notificações'},
            }
        }

    return grafo_direcional, grafico_colunas, selected_cidade, show_all_clicks
