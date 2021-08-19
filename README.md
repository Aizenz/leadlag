# 使用说明
### 作用：探究谁是交易员中的领袖，谁是交易员中的mockingbird
### 方法：通过交易之间的时间差来寻找不同交易员的交易相似性
> 假设：两笔同类同向交易之间的时间差越少，则该"trade pair"的相似性越高，后者越有可能是前者的模仿者。

类别一：By='ticker'。对每一只股票来说，前人的交易总是可能给后人一些启示。
我们假设每一笔交易都被后面所有的交易所模仿，且时间越近的交易模仿可能性越高，
对任意两笔同ticker的trade pair i&j，定义模仿趋势如下。

类别二：By='industry'。模仿者可能不会直接购买领导者所买的股票，而是购买了同行业的股票，
我们把这种扩大类别的跟随交易也视作相似策略。同样的，定义任意两笔同industry的trade pair i&j，
定义模仿趋势如下。

> 1⃣️idea pair模仿趋势定义：$$ tendency_{ij} = \frac{1}{time_j-time_i}$$

则对于交易i&j而言，tendency越小，则说明j跟随i的可能性越小，tendency越大，
则说明j跟随i的可能性越大。tendency大于1，意味着这两者之间的交易时间差小于24小时。
需要注意的是，这里的time已经换算成了天的整数倍。

现在我们已经拥有了一个可以求得所有指定trade pair模仿趋势的方法了，则对于任意creator pair m&n，
我们可以把他们n到m的所有模仿趋势加总，得到by creator 的关系亲密程度指数：
> 2⃣️creator pair关系亲密程度定义：$Relationship_{nm} = \Sigma_{n,m\in C}Tendency_{ij}(i\in n,j \in m)$$$ 

需要注意的是，这是一个有方向的关系，这意味着两个交易员可能存在互相模仿的问题。

此时我们得到了一张creators * creators 的正方形矩阵，这是一张有向图，他的每一行指示了该行的creator指向其他人的程度，
他的每一列指示了该creator被多少人指向，即他被多少人模仿的程度。


### 使用说明：
relationship.relationshipmetrix(df,by):

df是你需要传入的ideas列表，他至少应该包含creat_time,creator,ticker,industry。

by是你需要指明的类别，如果by = 'ticker'则在所有同ticker 的交易中寻找idea pairs。如果by = 'industry'，则在所有同industry的交易中寻找idea pairs.

该函数会返回一个pandas.Dataframe 他的横纵坐标都是creator， 他的参数表明了横坐标指向纵坐标的关系亲密程度，即定义2⃣️。
### 可能存在的问题
1. 该算法的idea pair的关系并不稳固，因为使用了时间差来定义概率，然而时间差的影响因素很多，并不一定时间差小的idea pairs 模仿概率就大
2. 同一个人可能对同一个ticker前后做了多次交易，我在计算tendency的时候，排除了同一个人进行的同类别交易之间的影响，即自己不可能是自己的模仿者。
3. 研究中
