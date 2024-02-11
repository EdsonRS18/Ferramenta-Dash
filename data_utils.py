# Importação de bibliotecas necessárias
import pandas as pd
import networkx as nx

def load_data(file_path, nrows=1500):
    return pd.read_csv(file_path, nrows=nrows)

def create_graph(data):
    G = nx.DiGraph()

    for _, row in data.iterrows():
        for node, pos_prefix in [(row['mun_noti'], 'noti'), (row['mun_infe'], 'infe')]:
            G.add_node(node, pos=(row[f'latitude_{pos_prefix}'], row[f'longitude_{pos_prefix}']))
        
        G.add_edge(row['mun_noti'], row['mun_infe'])

    return G

