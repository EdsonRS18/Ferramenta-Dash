from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout(df):
    # Título e Subtítulo
    header = html.H2('Dashboard de Malária', className='text-center mt-3 mb-4')
    subheader = html.H4('', className='text-center mb-5')

    # Dropdown de Seleção de Cidade
    cidade_options = [
        {'label': f'{mun_noti} - {df[df["mun_noti"] == mun_noti]["nome_noti"].iloc[0]}', 'value': mun_noti}
        for mun_noti in df['mun_noti'].unique()
    ]
    cidade_options.insert(0, {'label': 'Todas as cidades', 'value': 'Todas'})
    cidade_dropdown = dcc.Dropdown(
        id='cidade-dropdown',
        options=cidade_options,
        value='Todas',
        clearable=False,
        style={'color': '#000'}  # Melhora a legibilidade do texto
    )

    # Checklists e Botões
    hide_matching_checkbox = dcc.Checklist(
        id='hide-matching-municipality',
        options=[{'label': 'Ocultar infecções ocorridas no próprio município', 'value': 'hide'}],
        value=[],
        className='mb-3'
    )
    update_button = dbc.Button(
        'Mostrar Todas as Cidades',
        id='update-button',
        n_clicks=0,
        color='info',
        className='mb-3'
    )

    # Range Slider de Ano
    anos_unicos = sorted(df['ano'].dropna().unique())
    ano_range_slider = dcc.RangeSlider(
        id='ano-range-slider',
        min=min(anos_unicos),
        max=max(anos_unicos),
        step=1,
        marks={str(ano): str(ano) for ano in anos_unicos if ano % 2 == 0},  # Marcadores para anos pares
        value=[min(anos_unicos), max(anos_unicos)],
        className='mb-3'
    )

    # Gráficos
    grafo_direcional = dcc.Graph(id='grafo-direcional', className='mb-3')
    grafico_colunas = dcc.Graph(id='grafico-colunas', className='mb-3')
    grafico_linha = dcc.Graph(id='line-chart', className='mb-3')

    # Organização do Layout com uma estética aprimorada
    layout = html.Div([
        dbc.Container([
            header,
            #subheader,
            dbc.Row([
                dbc.Col(cidade_dropdown, width=12, lg=4),
                dbc.Col(hide_matching_checkbox, width=12, lg=4),
                dbc.Col(update_button, width=12, lg=4, className='d-flex justify-content-lg-end align-items-start'),
            ], className='mb-5'),
            dbc.Row([
                dbc.Col(ano_range_slider, width=12),
            ], className='mb-5'),
            dbc.Row([
                dbc.Col(grafo_direcional, md=6),
                dbc.Col(grafico_colunas, md=6),
            ], className='mb-4'),
            dbc.Row([
                dbc.Col(grafico_linha, width=12),
            ]),
        ], fluid=True),
    ], style={'padding': '20px'})

    return layout
