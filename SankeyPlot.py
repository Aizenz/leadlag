import plotly.graph_objects as go
import plotly.offline as py
import pandas as pd
import relationship

df = pd.read_excel('/Users/aizenz/Desktop/internHI/ideas_u20210811202801.xlsx')
matrix = relationship.relationmatrix(df, by='level3')
matrix.to_excel('matrix.xlsx')
creators = df['creator'].unique()

links = []
res = pd.DataFrame(columns=('leader', 'follower', 'strength'))
for i in range(len(creators)):
    for j in range(len(creators)):
        # ------------------- here comes the filter
        if i != 0 and j != 0 and 1 < matrix.iloc[i, j]:
            links.append([i, j, matrix.iloc[i, j]])
            temp = pd.DataFrame([[matrix.index[i], matrix.columns[j], matrix.iloc[i, j]]],
                                columns=('leader', 'follower', 'strength'))
            res = res.append(temp)
res = res.sort_values(by='strength', ascending=False).reset_index()
res.to_excel('relationstrength.xlsx')

data = [go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=creators,
        color="blue"
    ),
    link=dict(
        source=[i[1] for i in links],
        target=[i[0] for i in links],
        value=[i[2] for i in links]
    ))]
fig = go.Figure(data)

fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
py.plot(fig, filename='SankeyPlot.html')
