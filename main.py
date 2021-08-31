import numpy as np
import relationship
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def devide(matrix):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] != 0:
                matrix[i][j] = 1.0 / matrix[i][j]
    return matrix


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
    df = pd.read_excel('/Users/aizenz/Desktop/internHI/ideas_u20210811202801.xlsx')
    matrix = relationship.relationmatrix(df)
    G = nx.DiGraph(matrix.to_numpy().T)
    pr = nx.pagerank(G, alpha=0.9)
    pd.DataFrame(list(pr.items()), index=matrix.index).to_excel('Rpagerank.xlsx')

    creators = df['creator'].unique()
    res = pd.DataFrame(columns=('follower', 'leader', 'strength'))
    for i in range(len(creators)):
        for j in range(len(creators)):
            # ------------------- here comes the filter
            if i != 0 and j != 0:
                temp = pd.DataFrame([[matrix.index[i], matrix.columns[j], matrix.iloc[i, j]]],
                                    columns=('follower', 'leader', 'strength'))
                res = res.append(temp)
    res = res.sort_values(by='strength', ascending=False).reset_index()
    res.to_excel('relationstrengthWithPagerank.xlsx')
