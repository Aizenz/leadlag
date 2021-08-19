
# Industry-ticker-delay
# How to recognize the leading signal?
# The leading signal should be

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
df = pd.read_excel('/Users/aizenz/Desktop/internHI/ideas_u20210811202801.xlsx')
df = df.drop_duplicates(subset = 'create_time')
Industries = df.drop_duplicates(subset='industry')['industry']

plt.figure(figsize=(10,8))
i = 0
for industry in Industries:
    i += 1
    plt.subplot(6, 5, i)
    plt.title(industry)
    plt.yticks([])
    plt.xticks([])
    plt.scatter(df[df['industry'] == industry]['create_time'],df[df['industry'] == industry]['ticker'])

# 显示画布
plt.show()