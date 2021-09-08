# How can we forecast the importance of a coming idea?
import pandas as pd
import networkx as nx
import numpy as np
import relationship

if __name__ == "__main__":
    df = pd.read_excel('/Users/aizenz/Desktop/internHI/ideasData/lifetimeIdeas_u20210901103447.xlsx')
    PR_list = pd.DataFrame()
    PR_list['creator'] = df['creator'].unique()
    # 1.The dynamic pagerank
    # 1.1 start point
    data = df[df['create_time'] <= np.datetime64('2021-06-30')]
    creators = data['creator'].unique
    matrix = relationship.relationmatrix(data)
    pr = pd.DataFrame(nx.pagerank(nx.DiGraph(matrix.to_numpy()), alpha=0.9), index=[0]).T.set_axis(
        matrix.index).reset_index()
    pr.columns = ['creator', '2021-06-30']
    PR_list = pd.merge(PR_list, pr, how='outer', on='creator')
    timestamp = np.datetime64('2021-06-30')
    while timestamp <= np.datetime64('2021-08-31'):
        timestamp = timestamp + np.timedelta64(1, 'D')
        data = df[df['create_time'] < timestamp]
        creators = data['creator'].unique
        matrix = relationship.relationmatrix(data)
        pr = pd.DataFrame(nx.pagerank(nx.DiGraph(matrix.to_numpy()), alpha=0.9), index=[0]).T.set_axis(
            matrix.index).reset_index()
        pr.columns = ['creator', np.datetime_as_string(timestamp, unit='D')]
        PR_list = pd.merge(PR_list, pr, how='outer', on='creator')
        PR_list.to_csv('test.csv')

    # 2.The independence of an idea
