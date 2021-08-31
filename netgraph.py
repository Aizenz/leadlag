import networkx as nx
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_excel('matrix.xlsx', index_col='Unnamed: 0')
df = df.to_numpy()
G = nx.DiGraph(df)
strenth = 5
elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > strenth]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= strenth]
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=0.2)
nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1, edge_color='r', arrows=False)
nx.draw_networkx_edges(G, pos, edgelist=esmall, width=0.2, alpha=0.5, edge_color='b', arrows=False)
# labels标签定义
# nx.draw_networkx_labels(G, pos, labels=None)
plt.figure(figsize=(100, 100), dpi=200)
plt.axis('off')
plt.savefig("weighted_graph.png")
plt.show()
