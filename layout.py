from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout(df):
    header = html.H2(
        'MaláriaVis',
        className='text-center mt-1 mb-0',
        style={
            'background-color': '#4169E1',
            'color': 'white',
            'padding': '10px',
            'margin': '0px',
            'border': '0.5px solid #4169E1'
        }
    )

    cidade_options = [
        {'label': f'{mun_noti} - {df[df["mun_noti"] == mun_noti]["nome_noti"].iloc[0]}', 'value': mun_noti}
        for mun_noti in df['mun_noti'].unique()
    ]
    cidade_options.insert(0, {'label': 'Todas as cidades', 'value': 'Todas'})
    
    cidade_dropdown = html.Div([
        dbc.Row([
            dbc.Col(html.Label("Selecione a cidade:", style={'margin-top':'8px','font-family': 'Arial, sans-serif', 'margin-left': '30px', 'font-size': '16px'}), width=3.5),
            dbc.Col(
                dcc.Dropdown(
                    id='cidade-dropdown',
                    options=cidade_options,
                    value='Todas',
                    clearable=False,
                    style={'font-family': 'Arial, sans-serif', 'font-size': '16px', 'color': '#000', 'border-radius': '0px'}
                ),
                width=8,
            ),
        ], style={'margin-bottom': '10px'})
    ])

    hide_matching_checkbox = html.Div([
        html.Label([
            dcc.Checklist(
                id='hide-matching-municipality',
                options=[{'label': 'Ocultar infecções ocorridas no próprio município', 'value': 'hide'}],
                value=[],
                className='custom-checkbox-label',
                inputStyle={'margin-top':'12px','margin-right': '10px', 'font-family': 'Arial, sans-serif', 'font-size': '16px'},
            )
        ], style={'display': 'block', 'font-family': 'Arial, sans-serif', 'margin-bottom': '10px', 'font-size': '16px'}),
    ], className='mb-3')

    update_button = dbc.Button(
        'Limpar Filtros',
        id='update-button',
        n_clicks=0,
        style={
            'background-color': '#4169E1',
            'color': 'white',
            'fontWeight': 'bold',
            'border-radius': '0px',
            'font-family': 'Arial, sans-serif',
            'font-size': '16px',
            'margin-right': '30px'
        },
        className='mb-3'
    )

    anos_unicos = sorted(df['ano'].dropna().unique())
    ano_range_slider = dcc.RangeSlider(
        id='ano-range-slider',
        min=min(anos_unicos),
        max=max(anos_unicos),
        step=1,
        marks={str(ano): str(ano) for ano in anos_unicos if ano % 2 == 0},
        value=[min(anos_unicos), max(anos_unicos)],
        className='mb-3'
    )

    filter_section = html.Div([
        dbc.Row([
            dbc.Col(cidade_dropdown, width=12, lg=5),
            dbc.Col(hide_matching_checkbox, width=12, lg=4),
            dbc.Col(update_button, width=12, lg=3, className='d-flex justify-content-lg-end align-items-start'),
        ], className='mb-3 justify-content-center'),
        dbc.Row([
            dbc.Col(ano_range_slider, width=12),
        ], className='mb-5 justify-content-center')
    ], style={'background-color': '#F0F8FF', 'padding': '20px', 'border': '0.5px solid #4169E1'})

    layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([header], width=12),
            ]),
            filter_section,
            dbc.Row([
                dbc.Col(html.Div([
                    dcc.Loading(
                        id="loading-grafo-direcional",
                        type="circle",
                        children=dcc.Graph(id='grafo-direcional', className='mb-3')
                    )
                ]), width=6, style={'margin-top': '20px'}),
                dbc.Col(html.Div([
                    dcc.Loading(
                        id="loading-grafico-colunas",
                        type="circle",
                        children=dcc.Graph(id='grafico-colunas', className='mb-3')
                    )
                ]), width=6, style={'margin-top': '20px'}),
            ]),
            # dbc.Row([
            #     dbc.Col(html.Div([
            #         dcc.Loading(
            #             id="loading-grafico-linha",
            #             type="circle",
            #             children=dcc.Graph(id='line-chart', className='mb-3')
            #         )
            #     ]), width=12),
            # ]),
            dbc.Row([
                dbc.Col(html.Div([
                    dcc.Loading(
                        id="loading-endemic-corridor",
                        type="circle",
                        children=dcc.Graph(id='endemic-corridor-chart', className='mb-3')
                    )
                ]), width=12),
            ]),
        ], fluid=True),
    ], style={'padding': '20px'})

    return layout
