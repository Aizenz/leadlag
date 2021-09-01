import datetime
import numpy as np
import relationship
import pandas as pd
import networkx as nx
from scipy import stats

# By idea level
if __name__ == "1":
    df = pd.read_excel('/Users/aizenz/Desktop/internHI/ideasData/lifetimeIdeas_u20210901103447.xlsx')
    matrix = relationship.relationmatrix(df, by='ticker', pair_name='idea_entity_id')
    df.lifetimeAlpha = df['lifetimeAlpha']/df['size']
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

# By contributor level

if __name__ =='2':
    df = pd.read_excel('/Users/aizenz/Desktop/internHI/ideasData/lifetimeIdeas_u20210901103447.xlsx')
    matrix = relationship.relationmatrix(df, by='ticker', pair_name='creator')
    df.lifetimeAlpha = df['lifetimeAlpha'] / df['size']
    # lifetimeAlpha by creator
    creatorAlpha = df[['creator', 'lifetimeAlpha']].groupby(['creator']).mean()
    # Pagerank by leader
    G = nx.DiGraph(matrix.to_numpy())
    pr = nx.pagerank(G, alpha=0.9)
    pr = pd.DataFrame(pr, index=[0]).T.set_axis(matrix.index).reset_index()
    pr.columns = ['creator', 'PR']
    pr = pr.sort_values(by='PR', ascending=False)
    pr = pd.merge(pr, creatorAlpha, on='creator')
    pr.to_csv('PRleader.csv')
    # Spearman correlation
    print('leader:', stats.spearmanr(pr['PR'], pr['lifetimeAlpha'], alternative='greater'))

    # Pagerank by follower, using the reverse matrix
    G = nx.DiGraph(matrix.to_numpy().T)
    pr = nx.pagerank(G, alpha=0.9)
    pr = pd.DataFrame(pr, index=[0]).T.set_axis(matrix.index).reset_index()
    pr.columns = ['creator', 'PR']
    pr = pr.sort_values(by='PR', ascending=False)
    pr = pd.merge(pr, creatorAlpha, on='creator')
    pr.to_csv('PRfollower.csv')
    # Spearman correlation
    print('follower:', stats.spearmanr(pr['PR'], pr['lifetimeAlpha'], alternative='greater'))

    # save the pivot
    res = matrix.stack().reset_index()
    res.columns = ['follower_idea', 'leader_idea', 'PR']
    res = res[res['PR'] != 0].reset_index().drop(columns='index')
    res.to_csv('ideaPR.csv')

# The resignation
if __name__ =='__main__':
    df = pd.read_excel('/Users/aizenz/Desktop/internHI/ideasData/lifetimeIdeas_u20210901103447.xlsx')
    dfBefore = df[df['create_time'] < np.datetime64('2021-08-01')]
    dfAfter = df[df['create_time'] >= np.datetime64('2021-08-01')]
    matrixBefore = relationship.relationmatrix(dfBefore, by='ticker', pair_name='creator')
    matrixAfter = relationship.relationmatrix(dfAfter, by='ticker', pair_name='creator')

    prBefore = pd.DataFrame(nx.pagerank(nx.DiGraph(matrixBefore.to_numpy()), alpha=0.9), index=[0]).T.set_axis(matrixBefore.index).reset_index()
    prBefore.columns = ['creator', 'PRBeforeAug']
    prBefore = prBefore.sort_values(by='PRBeforeAug', ascending=False)

    prAfter = pd.DataFrame(nx.pagerank(nx.DiGraph(matrixAfter.to_numpy()), alpha=0.9), index=[0]).T.set_axis(matrixAfter.index).reset_index()
    prAfter.columns = ['creator', 'PRAfterAug']
    prAfter = prAfter.sort_values(by='PRAfterAug', ascending=False)
    # Spearman correlation
    pr = pd.merge(prBefore, prAfter, on=['creator'], how='inner')
    pr.to_excel('robustness.xlsx')
    print(stats.spearmanr(pr['PRBeforeAug'], pr['PRAfterAug']))

