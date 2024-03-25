import plotly.graph_objects as go
from update_graph import update_graph

def update_graph_callback(selected_city, click_data, df, G, pos, hide_matching_municipality=None, selected_years=None):
    print(f"Selected city: {selected_city}, Selected years: {selected_years}")

    if click_data and 'points' in click_data:
        clicked_node_code = click_data['points'][0]['customdata']
        selected_city = clicked_node_code

    df_filtered = df

    if hide_matching_municipality and 'hide' in hide_matching_municipality:
        df_filtered = df_filtered[df_filtered['mun_noti'] != df_filtered['mun_infe']]

    grafo_direcional = update_graph(selected_city, df_filtered, G, pos, hide_matching_municipality)

    if selected_city == 'Todas':
        # Mostrar os top 10 municípios de infecção
        dados_grafico_colunas = df_filtered.groupby('mun_infe').agg(
    {'notifications': 'sum', 'nome_infe': 'first'}
    ).reset_index().sort_values(by='notifications', ascending=True).tail(10)

        trace_mun_infe = go.Bar(
            y=dados_grafico_colunas['nome_infe'],
            x=dados_grafico_colunas['notifications'],
            hoverinfo='x',
            orientation='h',
            name='mun_infe',
        )

        grafico_colunas = {
            'data': [trace_mun_infe],
            'layout': {
                'title': f'TOP 10 Municípios de Infecção{selected_years}',
                'height': 700,
                'width': 600,
                'yaxis': {
                    'tickmode': 'linear',
                    'tickvals': list(range(10)),
                    'ticktext': dados_grafico_colunas['nome_infe'],
                    'dtick': 1,
                    'automargin': True,
                },
                'xaxis': {'title': 'Número de Notificações'},
                'margin': {'l': 150},
            }
        }
    else:
        dados_grafico_colunas = df_filtered[df_filtered['mun_noti'] == selected_city].groupby('mun_infe').agg(
            {'notifications': 'sum', 'nome_infe': 'first', 'mun_noti': 'first'}
        ).reset_index().sort_values(by='notifications', ascending=True).tail(10)

        total_notifications_selected_city = df_filtered[df_filtered['mun_noti'] == selected_city]['notifications'].sum()

        dados_grafico_colunas['percentagem'] = (dados_grafico_colunas['notifications'] / total_notifications_selected_city) * 100

        filtered_df = df_filtered[df_filtered['mun_noti'] == selected_city]
        total_notifications_mun_noti = filtered_df['notificacoes_total'].iloc[0] if not filtered_df.empty else 0
        selected_city_name = filtered_df['nome_noti'].iloc[0] if not filtered_df.empty else "Selected Municipality"


        trace_mun_infe = go.Bar(
            y=dados_grafico_colunas['nome_infe'],
            x=dados_grafico_colunas['notifications'],
            text=[f'{percent:.2f}%' for percent in dados_grafico_colunas['percentagem']],
            hoverinfo='text+x',
            orientation='h',
            name='mun_infe',
        )

        grafico_colunas = {
        'data': [trace_mun_infe],
        'layout': {
            'title': f'TOP 10 Municípios de Infecção (Relacionado a {selected_city_name}){selected_years}',
            'height': 700,
            'width': 600,
            'yaxis': {
                'tickmode': 'linear',
                'tickvals': dados_grafico_colunas['nome_infe'],
                'ticktext': dados_grafico_colunas['nome_infe'],
                'dtick': 1,
                'automargin': True,
            },
            'xaxis': {'title': 'Número de Notificações'},
            'margin': {'l': 150},
        }
    }

    return grafo_direcional, grafico_colunas, selected_city



import plotly.express as px

from dash import dcc

def create_line_chart(df, selected_year=None):
    df_aggregated = df.groupby('ano')['notifications'].sum().reset_index()

    if selected_year:
        total_notifications_selected_year = df[df['ano'] == selected_year]['notifications'].sum()
        df_aggregated['percentagem'] = (df_aggregated['notifications'] / total_notifications_selected_year) * 100
    else:
        df_aggregated['percentagem'] = (df_aggregated['notifications'] / df_aggregated['notifications'].sum()) * 100

    line_chart = px.line(df_aggregated, x='ano', y='percentagem', markers=True, title='Evolução de Notificações de Malária ao Longo dos Anos')

    line_chart.update_layout(
        xaxis_title='Ano',
        yaxis_title='Porcentagem de Notificações de Malária',
        height=400,
    )

    return dcc.Graph(id='line-chart', figure=line_chart)

