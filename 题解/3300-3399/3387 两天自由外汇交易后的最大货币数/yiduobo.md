---
title: "3387. 两天自由外汇交易后的最大货币数"
aliases: ["yiduobo的每日leetcode 3387.两天自由外汇交易后的最大货币数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "leetcode/hash-table", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/29830006159"
zhihu_id: "29830006159"
zhihu_title: "yiduobo的每日leetcode 3387.两天自由外汇交易后的最大货币数"
question_id: "3387"
question: "两天自由外汇交易后的最大货币数"
problem_url: "https://leetcode.cn/problems/maximize-amount-after-two-days-of-conversions/"
difficulty: "Medium"
rating: 1788
created: "2025-03-12T22:37:52+08:00"
updated: "2025-03-12T22:37:52+08:00"
upvotes: 1
comments: 0
---

# 3387. 两天自由外汇交易后的最大货币数

> **[yiduobo的每日leetcode 3387.两天自由外汇交易后的最大货币数](https://zhuanlan.zhihu.com/p/29830006159) · 知乎 · 2025-03-12 · 赞同 1**
> 力扣：[3387. 两天自由外汇交易后的最大货币数](https://leetcode.cn/problems/maximize-amount-after-two-days-of-conversions/) · Medium · 灵茶山艾府：[两次 DFS，简洁写法，附思考题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3387.两天自由外汇交易后的最大货币数

[3387. 两天自由外汇交易后的最大货币数 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-amount-after-two-days-of-conversions/description/)

题目给出一个字符串initialCurrency，表示初始的货币类型。一开始拥有1.0单位的initialCurrency。

另外给出四个数组pairs1、rates1、pairs2、rates2，分别表示两天内货币对的汇率。其中：

对于pairs1\[i\] \= \[startCurrency\[i\], targetCurrency\[i\]\]以及rates1\[i\]，表示在第一天可以按照汇率rates1\[i\]将startCurrency\[i\]转换为targetCurrency\[i\]。

对于pairs2\[i\] \= \[startCurrency\[i\], targetCurrency\[i\]\]以及rates2\[i\]，表示在第二天可以按照汇率rates2\[i\]将startCurrency\[i\]转换为targetCurrency\[i\]。

另外，每种targetCurrency都可以按照汇率1 / rate转换会对应的startCurrency。

在两天内都可以进行任意次数的兑换，问两天的兑换后可能拥有的最大initialCurrency的数量。题目保证转换图中没有循环。

将题目中的货币视为有向图中的点，将兑换关系视为带权的有向边，那么对于一组从startCurrency到targetCurrency，汇率为rate的兑换关系，在图中就是从startCurrency到targetCurrency的权重为rate的边，另外同时也需要建立一条从targetCurrency到startCurrency的权重为1 / rate的边。

根据pairs1、rates1以及pairs2、rates2分别建立两天的兑换关系图，由于题目保证图中不存在循环，那么就可以从initialCurrency开始进行bfs，分别计算出两天内1单位的initialCurrency可以兑换的各种货币的数量，分别记为r1和r2。

接下来枚举每种同时出现在r1和r2中的货币tmp，如果在第一天将initialCurrency转换为tmp，那么就可以获得tmp的数量为r1[tmp]，然后在第二天将tmp转换回initialCurrency，可以的得到的initialCurrency就是r1[tmp] / r2[tmp]，取所有r1[tmp] / r2[tmp]中的最大值作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxAmount(self, initialCurrency, pairs1, rates1, pairs2, rates2):
        """
        :type initialCurrency: str
        :type pairs1: List[List[str]]
        :type rates1: List[float]
        :type pairs2: List[List[str]]
        :type rates2: List[float]
        :rtype: float
        """
        
        def build_graph(pairs, rates):
            g = {}
            for p, r in zip(pairs, rates):
                x, y = p
                if x not in g:
                    g[x] = {}
                if y not in g:
                    g[y] = {}
                g[x][y] = r
                g[y][x] = 1 / r
            
            return g
        
        def calc(g):
            q = [initialCurrency]
            r = {initialCurrency : 1.0}
            head, tail = 0, 1
            while head < tail:
                for x in q[head : tail]:
                    for y in g.get(x, {}):
                        if y not in r:
                            r[y] = r[x] * g[x][y]
                            q.append(y)
                
                head, tail = tail, len(q)
            
            return r
        
        g1 = build_graph(pairs1, rates1)
        g2 = build_graph(pairs2, rates2)
        r1 = calc(g1)
        r2 = calc(g2)
        res = 0
        for tmp in r1:
            if tmp in r2:
                r = r1[tmp] / r2[tmp]
                res = max(res, r)
        return res
```
