import numpy as np
import relationship
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from scipy import stats

if __name__ == "test":
    df = pd.read_excel('/Users/aizenz/Desktop/internHI/ideas_u20210811202801.xlsx')
    industries = df['industry'].unique()
    industries = np.sort(industries)
    i = 1
    plt.figure(figsize=(17, 30))

    for industry in industries:
        field = df[df['industry'] == industry]
        matrix = relationship.relationmatrix(field, by='industry')
        matrix = matrix.to_numpy()
        matrix = devide(matrix)
        G = nx.DiGraph(matrix)
        i += 1
        plt.subplot(10, 3, i)
        plt.title(industry)

        strenth = 1
        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] < strenth]
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] >= strenth]
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=0.7)
        nx.draw_networkx_edges(G, pos, edgelist=elarge, width=2, edge_color='r', arrows=False)
        nx.draw_networkx_edges(G, pos, edgelist=esmall, width=0.2, alpha=0.5, edge_color='b', arrows=False)
        # labels标签定义
        # nx.draw_networkx_labels(G, pos, labels=None)
    plt.tight_layout(h_pad=2, w_pad=2)
    plt.savefig("weighted_graph.png")
    plt.show()

if __name__ == "__main__":
    df = pd.read_excel('/Users/aizenz/Desktop/internHI/ideasData/lifetimeIdeas_u20210901103447.xlsx')
    matrix = relationship.relationmatrix(df, by='ticker', pair_name='idea_entity_id')
    # Pagerank
    G = nx.DiGraph(matrix.to_numpy())
    pr = nx.pagerank(G, alpha=0.9)
    pr = pd.DataFrame(pr, index=[0]).T.set_axis(matrix.index).reset_index()
    pr.columns = ['idea_entity_id', 'PR']
    pr = pr.sort_values(by='PR', ascending=False)
    pr = pd.merge(pr, df[['idea_entity_id', 'lifetimeAlpha']], on='idea_entity_id')
    pr.to_csv('pagerankIdea.csv')
    # Spearman correlation
    print(stats.spearmanr(pr['PR'], pr['lifetimeAlpha'], alternative='greater'))
    # save the pivot
    res = matrix.stack().reset_index()
    res.columns = ['follower_idea', 'leader_idea', 'PR']
    res = res[res['PR'] != 0].reset_index().drop(columns='index')
    res.to_csv('ideaPR.csv')
