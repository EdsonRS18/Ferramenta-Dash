from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

def create_layout(df):

    # Adicionando botões de navegação acima do dropdown
    buttons_navigation = dbc.Row([
        dbc.Col(dcc.Link(dbc.Button("Ir para Malária", color="primary", className='nav-button'), href="/pagina_malaria"), width=6),
        dbc.Col(dcc.Link(dbc.Button("Ir para Outra Página", color="primary", className='nav-button'), href="/outra_pagina"), width=6),
    ], style={'margin-top': '20px'})

    # Dropdown para seleção de cidade
    options_cidade_dropdown = [{'label': f'{mun_noti} - {df[df["mun_noti"] == mun_noti]["nome_noti"].iloc[0]}', 'value': mun_noti} for mun_noti in df['mun_noti'].unique()]
    options_cidade_dropdown.insert(0, {'label': 'Todas as cidades', 'value': 'Todas'})

    # Layout do filtro e seleção de cidade
    cidade_dropdown = dcc.Dropdown(
        id='cidade-dropdown',
        options=options_cidade_dropdown,
        value='Todas',
        style={'width': '100%'}  # Aumentando a largura do dropdown
    )
    update_button = dbc.Button(
    'Mostrar todas as cidades',
    id='update-button',
    n_clicks=0,
    color='primary',
    style={'margin-top': '10px'}
)

    search_input = dcc.Input(
        id='search-input',
        type='text',
        placeholder='Digite o nome do município...',
        style={'width': '100%'}  # Aumentando a largura da caixa de texto
    )

    hide_matching_checkbox = dcc.Checklist(
        id='hide-matching-municipality',
        options=[{'label': 'Ocultar notificações do município nele mesmo', 'value': 'hide'}],
        value=[]
    )

    # Layout dos gráficos
    grafo_direcional = dcc.Graph(
        id='grafo-direcional',
        config={'scrollZoom': False, 'displayModeBar': True},
        #style={'height': '400px'}
    )

    grafico_colunas = dcc.Graph(
        id='grafico-colunas',
       # style={'height': '400px'}
    )

    # Criando o Dropdown de Ano
    anos_unicos = sorted(df['ano'].dropna().unique())
    options_ano_dropdown = [
        {'label': 'Todos os anos', 'value': 'Todos'},
        * [{'label': str(ano), 'value': str(ano)} for ano in anos_unicos]
    ]

    ano_dropdown = dcc.Dropdown(
        id='ano-dropdown',
        options=options_ano_dropdown,
        value='Todos',  # Inicia com a opção "Todos os anos" selecionada
        clearable=False,
        style={'width': '100%'}  # Aumentando a largura do dropdown
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
        buttons_navigation,

        dbc.Row([
            dbc.Col([
                html.Label('Selecione a cidade:'),
                cidade_dropdown,
            ], width=4),

            dbc.Col([
                html.Label('Filtro por nome de município:'),
                search_input,
                hide_matching_checkbox,
            ], width=4),

            dbc.Col([
                html.Label('Selecione o ano:'),
                ano_dropdown,
            ], width=4),
            dbc.Col([
            update_button,  # Adicione o novo botão de atualização
        ], width=4),
        ], className='filter-section'),

        graficos_lado_a_lado
        
    ], style={'height': '800px'})

    return layout
