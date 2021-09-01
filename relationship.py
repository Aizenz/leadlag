# What we truly want is the relationship between the ideas suplier, so the following
# tickers can be regarded as hyperlinks towards the leaders.
# We can use weight to measure the strength of those links as how many people have
# followed your strategies.
import pandas as pd
import numpy as np
import datetime
import networkx as nx
from matplotlib import pyplot as plt
# Function tendency measures the intendency of a ticker to follow another one
# it is defined as
# Y = 1/Deltatime(days)
# the closer the time is, the bigger the intendency is.
def tendency(i,j)->float:
    # para is used to determine how much tendency should be included,
    # the higher it is , the morer tendency will be included
    # i = follwer,j = leader
    if(i==j): return 0
    timedelta = (i-j)/np.timedelta64(1, 'D')
    if timedelta>0:
        if timedelta < 1:
            return 5
        elif timedelta < 2:
            return 4
        elif timedelta < 3:
            return 3
        elif timedelta < 4:
            return 2
        elif timedelta < 5:
            return 1
        else:
            return 0.1
    elif timedelta<0:
        if -1 < timedelta:
            return -5
        elif -2 < timedelta:
            return -4
        elif -3 < timedelta:
            return -3
        elif -4 < timedelta:
            return -2
        elif -5 < timedelta:
            return -1
        else:
            return -0.1



def relationmatrix(df:pd.DataFrame,by='ticker',pair_name = 'creator')->pd.DataFrame:
    # This function return a relationship matrix between creator in the form of directed graphs
    # This matrix measures the tendency from creator j to i, which means i is leader and j is lag
    # by can be 'ticker' |  'industry'
    # pair_name can be 'creator' or 'idea_entity_id'
    # ----------
    # Notice that 'by' mustn't be equavalent with pair_name
    areas = df[by].unique()
    pairs = df[pair_name].unique()
    matrix = pd.DataFrame(np.zeros((len(pairs), len(pairs))), index=pairs, columns=pairs)

    for area in areas:
        tickersgroup = df[df[by] == area]
        # You should notice that i&j are not continuous numbers because the index is not continuous
        for i, row_i in tickersgroup.iterrows():
            for j, column_j in tickersgroup.iterrows():
                if (j <= i):
                    continue
                # make sure that the followers have the same direction
                elif (row_i['direction'] == column_j['direction'] and row_i[pair_name] != column_j[pair_name]):
                    # if temp>0,then i is the leader and j is the lag
                    # the rows indicate where they pointed to, and the columns indicate who is pointing them
                    # so the rows are the leader index.
                    temp = tendency(row_i['create_time'], column_j['create_time'])
                    if (temp < 0):
                        matrix.loc[column_j[pair_name], row_i[pair_name]] -= temp
                    elif (temp > 0):
                        matrix.loc[row_i[pair_name], column_j[pair_name]] += temp
                    else:continue
    return matrix

if __name__ == "__main__":
    df = pd.read_excel('/Users/aizenz/Desktop/internHI/ideas_u20210811202801.xlsx')
    matrix = relationmatrix()
    result = pd.DataFrame(matrix.sum())
    #pr = nx.pagerank(nx.DiGraph(matrix.to_numpy()))
    #pr = pd.DataFrame(pr,index=['pagerank']).T
    #pr = pr.append(result)
    #result = result.sort_values(ascending= False)
    result.to_excel('/Users/aizenz/Desktop/internHI/result.xlsx')
    matrix.to_csv('/Users/aizenz/Desktop/internHI/matrix.csv')
    #pr.to_excel('/Users/aizenz/Desktop/internHI/pagerank.xlsx')


    df = pd.read_csv('/Users/aizenz/Desktop/internHI/matrix.csv', index_col='Unnamed: 0')
    df = df.to_numpy()
    G = nx.DiGraph(df)
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 10]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 10]
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=0.2)
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1, edge_color='b', arrows=False)
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=0.2, alpha=0.5, edge_color='b', arrows=False)
    # labels标签定义
    # nx.draw_networkx_labels(G, pos, labels=None)
    plt.figure(figsize=(600, 600), dpi=200)
    plt.axis('off')
    plt.savefig("weighted_graph.png")
    plt.show()




