---
title: "851. 喧闹和富有"
aliases: ["yiduobo的每日leetcode 851.喧闹和富有"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348414419"
zhihu_id: "348414419"
zhihu_title: "yiduobo的每日leetcode 851.喧闹和富有"
question_id: "851"
question: "喧闹和富有"
problem_url: "https://leetcode.cn/problems/loud-and-rich/"
created: "2021-02-01T22:25:56+08:00"
updated: "2021-02-01T22:25:56+08:00"
upvotes: 0
comments: 0
---

# 851. 喧闹和富有

> **[yiduobo的每日leetcode 851.喧闹和富有](https://zhuanlan.zhihu.com/p/348414419) · 知乎 · 2021-02-01 · 赞同 0**
> 力扣：[851. 喧闹和富有](https://leetcode.cn/problems/loud-and-rich/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

851.喧闹和富有

[力扣](https://leetcode-cn.com/problems/loud-and-rich/)

对于每个人而言，其最终的answer只会受到其自身以及明确比此人更富有的人的影响，因此可以使用动态规划来解决。对于y而言，就有f[y] \= min(f[x], f[y])，其中x为所有的明确比y更富有的人。

接下来，则是动态规划计算顺序的问题。对于每个人，我们都需要优先计算比此人更富有的人的answer，那么如果我们针对每一组richer关系建立有向边，那么这个计算顺序就可以通过拓扑排序来得到，当然动态规划也可以同步进行。

于是现在的做法为：

1、先按照richer关系建立有向图，其中对于richer[x, y]，我们建立一条从x指向y的有向边。

2、对构建好的图执行拓扑排序，对于当前处理的节点x，遍历其每条出边，设其出边的另一头为y，那么就有f[y] \= min(f[x], f[y])。同时，将y的入度减一。当y的入度为0时，将y加入到拓扑排序的队列当中。

初始在队列中的点为没有明确更富有的人，在拓扑排序完成后，f就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def loudAndRich(self, richer, quiet):
        """
        :type richer: List[List[int]]
        :type quiet: List[int]
        :rtype: List[int]
        """

        n = len(quiet)
        f = range(n)
        ind = [0] * n
        g = {x : set() for x in range(n)}
        for x, y in richer:
            g[x].add(y)
            ind[y] += 1
        
        q = []
        for index in range(n):
            if ind[index] == 0:
                q.append(index)
        
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                if quiet[f[next]] > quiet[f[now]]:
                    f[next] = f[now]
                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    r += 1
        
        return f
```
