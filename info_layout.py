# info_layout.py
from dash import html
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_info_layout(df):
    # Aqui você pode adicionar os componentes para exibir informações sobre o projeto
    info_content = html.Div([
        html.H2('Informações'),
        html.P('Aqui você pode adicionar informações sobre o projeto.'),
        # Adicione mais componentes conforme necessário para exibir os dados ou gráficos
    ])

    # Montagem do layout final para a seção de informações
    info_layout = html.Div(
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.Div([
                        info_content,
                        # Adicione mais conteúdo relacionado às informações conforme necessário...
                    ])
                ], style={'margin-bottom': '20px'}),
            ]),
            style={
                'font-family': 'Arial, sans-serif',
                'padding': '20px',
                'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
                'border-radius': '10px'
            }
        )
    )

    return html.Div([
        info_layout,
        html.Div([
            dcc.Link(dbc.Button("Ir para Painel", color="primary"), href="/"),
            dcc.Link(dbc.Button("Ir para Malária", color="primary"), href="/pagina_malaria")
        ], style={'margin-top': '20px'})
    ])
