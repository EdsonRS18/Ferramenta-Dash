from dash import html, dcc
import dash_bootstrap_components as dbc


from callbacks import create_line_chart
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
    

    hide_matching_checkbox = dcc.Checklist(
        id='hide-matching-municipality',
        options=[{'label': 'Ocultar infecções ocorridas no próprio município', 'value': 'hide'}],
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

     # Gere uma lista de anos pares
    anos_pares = [ano for ano in anos_unicos if ano % 2 == 0]

    # Configure o RangeSlider para exibir todos os anos, mas visualmente de dois em dois
    ano_range_slider = dcc.RangeSlider(
        id='ano-range-slider',
        min=min(anos_unicos),
        max=max(anos_unicos),
        step=1,  # Mantenha o passo como 1 para incluir todos os anos
        marks={str(ano): str(ano) if ano % 2 == 0 else '' for ano in anos_unicos},
        value=[min(anos_unicos), max(anos_unicos)],  # Defina o intervalo inicial
    )


    # Layout dos gráficos lado a lado
    graficos_lado_a_lado = html.Div([
        html.Div([
            dcc.Loading(
                id="loading-graficos",
                type="circle",
                children=[
                    html.Div([
                        grafo_direcional,
                        grafico_colunas,
                    ], style={'width': '100%', 'display': 'flex'}),
                ],
            ),
        ], key='graficos_lado_a_lado_key'),
    ], key='graficos_lado_a_lado_loading_key')

    # Bloco separado para o gráfico de linha
    grafico_linha = dbc.Row([
    dbc.Col([
        dcc.Graph(id='line-chart')  # Certifique-se de usar o mesmo ID definido no callback
    ], width=12),
])
    # Montagem do layout final
    layout = html.Div([
     #   buttons_navigation,

        dbc.Row([
            dbc.Col([
                html.Label('Selecione a cidade:'),
                cidade_dropdown,
            ], width=4),

            dbc.Col([
                html.Label(''),
                hide_matching_checkbox,
            ], width=4),

            # Substitua a seção do layout onde o dropdown de ano é adicionado pelo RangeSlider
            dbc.Col([
            html.Label('Selecione o intervalo de anos:'),
            ano_range_slider,
            # Adicione a linha informativa para exibir o intervalo selecionado por extenso
            html.Div(id='intervalo-selecionado', style={'margin-top': '10px'}),
    ], width=4),
            dbc.Col([
            update_button,  # Adicione o novo botão de atualização
        ], width=4),
        ], className='filter-section'),

        # Adicione os blocos de gráfico ao layout
     # Adicione o indicador de carregamento e os blocos de gráfico ao layout
    html.Div([
        graficos_lado_a_lado,
        grafico_linha,
    ], style={'width': '100%'}),

        
    ], style={'height': '800px'})

    return layout
