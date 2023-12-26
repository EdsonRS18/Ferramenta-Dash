from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout(df):
    # Dropdown para seleção de cidade
    options_cidade_dropdown = [{'label': f'{mun_noti} - {df[df["mun_noti"] == mun_noti]["nome_noti"].iloc[0]}', 'value': mun_noti} for mun_noti in df['mun_noti'].unique()]
    options_cidade_dropdown.insert(0, {'label': 'Todas as cidades', 'value': 'Todas'})

    # Layout do filtro e seleção de cidade
    cidade_dropdown = dcc.Dropdown(
        id='cidade-dropdown',
        options=options_cidade_dropdown,
        value='Todas',
        style={'width': '100%'}
    )

    search_input = dcc.Input(
        id='search-input',
        type='text',
        placeholder='Digite o nome do município...',
        style={'width': '100%', 'margin-top': '10px'}
    )

    show_all_button = dbc.Button(
        'Mostrar Todas as Cidades',
        id='show-all-button',
        n_clicks=0,
        color='success',
        className='mr-1',
        style={'width': '100%'}
    )

    hide_matching_checkbox = dcc.Checklist(
        id='hide-matching-municipality',
        options=[{'label': 'Ocultar notificações do municipio nele mesmo', 'value': 'hide'}],
        value=[],
        style={'margin-top': '10px'}
    )

    # Layout dos gráficos
    grafo_direcional = dcc.Graph(
        id='grafo-direcional',
        config={'scrollZoom': False, 'displayModeBar': True},
        style={'height': '450px'}
    )

    grafico_colunas = dcc.Graph(
        id='grafico-colunas',
        style={'height': '450px'}
    )

    # Montagem do layout final
    layout = html.Div(
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    dbc.Row([
                        dbc.Col(cidade_dropdown, width=9),
                        dbc.Col(show_all_button, width=3),
                    ], justify='between', style={'margin-bottom': '10px'}),
                    
                    dbc.Row([
                        dbc.Col(search_input, width=9),
                        dbc.Col(hide_matching_checkbox, width=3),
                    ]),
                ], style={'margin-bottom': '20px'}),

                html.Div([
                    dbc.Row([
                        dbc.Col(grafo_direcional, width=6, style={'margin-bottom': '20px'}),
                        dbc.Col(grafico_colunas, width=6, style={'margin-bottom': '20px'}),
                    ]),
                ], style={'margin-bottom': '20px', 'margin-left': '-15px', 'margin-right': '-15px'}),
                
                # Adicione outras seções conforme necessário...
            ]),
            style={
                'font-family': 'Arial, sans-serif',
                'padding': '20px',
                'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
                'border-radius': '10px'
            }
        )
    )

    return layout
