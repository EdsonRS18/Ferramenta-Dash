from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

def create_layout(df):

    # Adicionando botões de navegação acima do dropdown
    
    buttons_navigation = dbc.Row([
        dbc.Col(dcc.Link(dbc.Button("Ir para Malária", color="primary"), href="/pagina_malaria"), width=6),
        dbc.Col(dcc.Link(dbc.Button("Ir para Outra Página", color="primary"), href="/outra_pagina"), width=6),
    ], style={'margin-top': '20px'})

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

    # Adicionando botão "Mostrar Todas as Cidades"
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

   # Criando o Dropdown de Ano
    ano_dropdown = dcc.Dropdown(
        id='ano-dropdown',
        options=[
            {'label': 'Todos os anos', 'value': 'Todos'},
            * [{'label': str(ano), 'value': str(ano)} for ano in df['ano'].unique() if not pd.isna(ano)]
        ],
        value=None,  # Inicia sem nenhum valor selecionado
        clearable=False,
        style={'width': '50%'}
    )



    # Layout dos gráficos lado a lado
    graficos_lado_a_lado = html.Div([
        html.Div([
            grafo_direcional
        ], style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            grafico_colunas
        ], style={'width': '50%', 'display': 'inline-block'}),
    ], key='graficos_lado_a_lado_key')

    # Montagem do layout final
    layout = html.Div([
        html.Div([
            cidade_dropdown,
            show_all_button
        ]),

        html.Div([
            search_input,
            hide_matching_checkbox,
            ano_dropdown,  # Adicione o Dropdown de Ano ao layout

        ]),

        graficos_lado_a_lado
    ], style={'height': '800px'})

    return layout
