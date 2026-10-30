---
title: "1627. 带阈值的图连通性"
aliases: ["yiduobo的每日leetcode 1627.带阈值的图连通性"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/437400176"
zhihu_id: "437400176"
zhihu_title: "yiduobo的每日leetcode 1627.带阈值的图连通性"
question_id: "1627"
question: "带阈值的图连通性"
problem_url: "https://leetcode.cn/problems/graph-connectivity-with-threshold/"
created: "2021-11-24T23:42:03+08:00"
updated: "2021-11-24T23:42:03+08:00"
upvotes: 0
comments: 0
---

# 1627. 带阈值的图连通性

> **[yiduobo的每日leetcode 1627.带阈值的图连通性](https://zhuanlan.zhihu.com/p/437400176) · 知乎 · 2021-11-24 · 赞同 0**
> 力扣：[1627. 带阈值的图连通性](https://leetcode.cn/problems/graph-connectivity-with-threshold/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1627.带阈值的图连通性

[力扣](https://leetcode-cn.com/problems/graph-connectivity-with-threshold/)

图中两点x与y相连的条件是存在一个z满足x和y都是z的倍数，且z大于threshold，那么对于任意大于threshold的数k而言，点k、2k、...、mk之间都是相连的。由于题目只关心连通性而不管关心具体图的构成，因此在这里可以使用并查集来维护这个连通性。

于是现在就有了一种做法，从threshold + 1开始枚举k，然后通过并查集将k与2k、k与3k、...、k与mk的连通起来。这个做法需要从threshold + 1开始枚举到n，而对于枚举到的k，则需要执行n / k次并查集的查找与合并操作，因此实际上一共执行了n / (threshold + 1) + n / (threshold + 2) + ... + n / n，这个式子的渐进复杂度为O(nlogn)，因此总的时间复杂度就是O(nlogn \* α(n))，完全是够用的了。

当然，在这里也可以利用数论知识改进k的枚举过程。实际上现在的枚举方式与筛法很类似，而筛法本身也是多种多样的，有兴趣的话可以去了解一下，这里就不再展开了。

最后附上python代码：

```python
class Solution(object):
    def areConnected(self, n, threshold, queries):
        """
        :type n: int
        :type threshold: int
        :type queries: List[List[int]]
        :rtype: List[bool]
        """

        fa = range(n + 1)
        for z in range(threshold + 1, n):
            fa_z = self.find(fa, z)
            tmp = z + z
            while tmp <= n:
                fa_tmp = self.find(fa, tmp)
                if fa_z != fa_tmp:
                    fa[fa_tmp] = fa_z
                
                tmp += z
        
        res = []
        for x, y in queries:
            res.append(self.find(fa, x) == self.find(fa, y))
        
        return res

    def find(self, fa, now):
        if fa[now] != now:
            fa[now] = self.find(fa, fa[now])
        return fa[now]
```
