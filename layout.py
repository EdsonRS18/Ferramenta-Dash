from dash import html, dcc
import dash_bootstrap_components as dbc

from dash import html, dcc

def create_layout(df):
    # Dropdown para seleção de cidade
    options_cidade_dropdown = [{'label': f'{mun_noti} - {df[df["mun_noti"] == mun_noti]["nome_noti"].iloc[0]}', 'value': mun_noti} for mun_noti in df['mun_noti'].unique()]
    options_cidade_dropdown.insert(0, {'label': 'Todas as cidades', 'value': 'Todas'})

    # Layout do filtro e seleção de cidade
    cidade_dropdown = dcc.Dropdown(
        id='cidade-dropdown',
        options=options_cidade_dropdown,
        value='Todas'
    )

    search_input = dcc.Input(
        id='search-input',
        type='text',
        placeholder='Digite o nome do município...'
    )

    show_all_button = dbc.Button(
        'Mostrar Todas as Cidades',
        id='show-all-button',
        n_clicks=0,
        color='success'
    )

    hide_matching_checkbox = dcc.Checklist(
        id='hide-matching-municipality',
        options=[{'label': 'Ocultar notificações do município nele mesmo', 'value': 'hide'}],
        value=[]
    )

    # Layout dos gráficos
    grafo_direcional = dcc.Graph(
        id='grafo-direcional',
        config={'scrollZoom': False, 'displayModeBar': True}
    )

    grafico_colunas = dcc.Graph(
        id='grafico-colunas'
    )

    # Layout dos gráficos lado a lado
    graficos_lado_a_lado = html.Div([
        html.Div([
            grafo_direcional
        ], style={'width': '50%', 'display': 'inline-block'}),  # Simulando 15 colunas

        html.Div([
            grafico_colunas
        ], style={'width': '50%', 'display': 'inline-block'}),  # Simulando mais 15 colunas
    ])
    # Montagem do layout final
    layout = html.Div(
        html.Div([
            html.Div([
                cidade_dropdown,
                show_all_button
            ]),

            html.Div([
                search_input,
                hide_matching_checkbox
            ]),

            graficos_lado_a_lado  # Adicionando os gráficos na disposição lado a lado
        ]),
        style={'height': '800px'}
    )

    return layout
