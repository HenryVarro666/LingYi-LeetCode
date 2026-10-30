---
title: "753. 破解保险箱"
aliases: ["yiduobo的每日leetcode 753.破解保险箱"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/338167746"
zhihu_id: "338167746"
zhihu_title: "yiduobo的每日leetcode 753.破解保险箱"
question_id: "753"
question: "破解保险箱"
problem_url: "https://leetcode.cn/problems/cracking-the-safe/"
created: "2020-12-19T23:40:39+08:00"
updated: "2020-12-19T23:40:39+08:00"
upvotes: 0
comments: 0
---

# 753. 破解保险箱

> **[yiduobo的每日leetcode 753.破解保险箱](https://zhuanlan.zhihu.com/p/338167746) · 知乎 · 2020-12-19 · 赞同 0**
> 力扣：[753. 破解保险箱](https://leetcode.cn/problems/cracking-the-safe/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

753.破解保险箱

[力扣](https://leetcode-cn.com/problems/cracking-the-safe/)

很有意思的题目。拿到题目的第一想法是将各个密码都看作一个状态，然后每次输入新的一位密码状态就会发生转移。如果将状态视为点，输入的一位密码视为边，那么题目就被转化为了有向图上的汉密尔顿路径问题，即给出一张有向图，找出其中最短的一条路径，要求经过图中每个点一次且每条边最多只能经过一次。

很遗憾，汉密尔顿路径问题本身是np难的，而这里构造的图也并不是很规范，因此不太容易使用构造法来获得答案。

不过注意到这个图虽然不规范，但是也有特别的性质，即每个点的入度和出度都一定是k，且每条入编的起点的后缀一致，每条出边的终点前缀一致。

例如在n和k都等于3的情况下，对于状态012，其入边的起始点分别为001、101以及201，这三个具有相同后缀01的点加上值为2的边得到了012；另一方面，从012出发往后可以走到120、121以及122这三个前缀为12的点。

有了这个性质，我们可以用一种新的视角来看之前构造的图。我们不再将每个状态单独列为节点，而是根据其除去首位的后缀来构图。

例如在n和k都等于3的情况下，原始图中有

000、001、002、

010、011、012、

020、021、022、

100、101、102

110、111、112

120、121、122、

200、201、202、

210、211、212、

220、221、222

这总共27个节点

对于新的构图方式，图中只有

00、01、02、

10、11、12

20、21、22

这9个点，而原始图中所有的边，则都根据后缀合并到一个节点上。

例如原来从010、110、210到100的边，在新图上就是从10到00的边，边上的权值依然为0。

那么到了这里，原图中的汉密尔顿路径问题，就转化为了新图中的欧拉路径问题，即对于一张有向图，如果才能不重复地将每条边都走一遍，这个问题是有多项式算法的，印象中之前好像也有一题也是欧拉路径问题。

那么对于欧拉路径问题，一般做法需要先计算图中节点的度，然后若所有点的入度都等于出度，或者有两个点满足其中一个入度比出度多1，而另一个入度比出度少1，那么就是有解的。对于本体，所有节点的入度和出度都是一样的，因此我们可以从任意点开始执行dfs。对于当前点，枚举其所有的出边edge以及对应的节点next，依次删去这些边然后对next进行dfs。执行完所有next的dfs之后，将now加入到答案中即可。对于本题，则是执行完之后将当前节点的最后一位数字加入到答案中。

dfs完成之后，还需要将起点的前缀也加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def crackSafe(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """

        if n == 1:
            return ''.join([str(x) for x in range(k)])

        G = {}
        if n == 2:
            node_list = range(k)
        elif n == 3:
            node_list = [x * 10 + y for x in range(k) for y in range(k)]
        else:
            node_list = [x * 100 + y * 10 + z for x in range(k) for y in range(k) for z in range(k)]
        
        for now in node_list:
            G[now] = {}
            for edge_num in range(k):
                next = (now * 10 + edge_num) % (10 ** (n - 1))
                G[now][edge_num] = next
        
        res = []
        self.dfs(0, G, k, res)
        return ''.join(str(x) for x in res) + '0' * (n - 2)

    def dfs(self, now, G, k, res):
        for edge_num in range(k):
            if edge_num in G[now]:
                next = G[now][edge_num]
                G[now].pop(edge_num)
                self.dfs(next, G, k, res)

        res.append(now % 10)
```
