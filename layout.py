from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout(df):
    # Título e Subtítulo
    header = html.H2('Painel de Infecções e Notificações de Malária', className='text-center mt-3 mb-4')
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

    hide_matching_checkbox = html.Div([
    html.Label([
        dcc.Checklist(
            id='hide-matching-municipality',
            options=[{'label': '   Ocultar infecções ocorridas no próprio município', 'value': 'hide'}],
            value=[],
            # Removido o style inline para ajuste via CSS
            className='custom-checkbox-label',  # Classe customizada para estilizar especificamente este label
        )
    ], style={'display': 'block', 'margin-left': '20px'}),  # Adiciona um espaço à esquerda do checkbox
], className='mb-3')

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

    # Gráficos com Spinners
    grafo_direcional = html.Div([
        dcc.Loading(
            id="loading-grafo-direcional",
            type="circle",
            children=dcc.Graph(id='grafo-direcional', className='mb-3')
        )
    ])
    grafico_colunas = html.Div([
        dcc.Loading(
            id="loading-grafico-colunas",
            type="circle",
            children=dcc.Graph(id='grafico-colunas', className='mb-3')
        )
    ])
    grafico_linha = html.Div([
        dcc.Loading(
            id="loading-grafico-linha",
            type="circle",
            children=dcc.Graph(id='line-chart', className='mb-3')
        )
    ])

    # Inserindo as imagens JPG e PNG

    img_upe_url = "https://upload.wikimedia.org/wikipedia/commons/9/9b/Logo-upe-site.png"
    img_dotlab_url = "https://avatars.githubusercontent.com/u/72280399?s=280&v=4"




        # Cria as tags de imagem
    img_jpg = html.Img(src=img_upe_url, className='img-fluid', style={'max-height': '100px', 'max-width': '100px'})
    img_png = html.Img(src=img_dotlab_url, className='img-fluid', style={'max-height': '100px', 'max-width': '100px'})

    # Coluna para as imagens com ajuste para centralização horizontal e vertical
    images_column = dbc.Col(
        html.Div(
            [img_jpg, img_png],
            className='d-flex justify-content-center align-items-center',  # Centraliza as imagens na coluna
            style={'height': '100%'}  # Assegura que o div interno ocupe toda a altura da coluna, para o alinhamento vertical funcionar
        ),
        width=4,
        className='d-flex justify-content-end align-items-start',  # Estes estilos podem ser ajustados ou removidos conforme o desejado
    )
    # Cria o layout da aplicação
    # Atualiza a estrutura do layout para incluir a coluna de imagens atualizada
    layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([header], width=8),  # Coluna para o título com 8 espaços
                images_column,  # Coluna atualizada para as imagens
        ], className='mb-5 align-items-center'),  # Alinhar verticalmente o conteúdo da linha ao centro # Alinhar verticalmente o conteúdo da linha ao centro
            dbc.Row([
                dbc.Col([], width=12),  # Coluna vazia para criar espaço
            ], className='mb-2'),  # Definindo a margem apenas abaixo do título
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
