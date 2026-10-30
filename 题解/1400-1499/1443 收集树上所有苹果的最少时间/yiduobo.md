---
title: "1443. 收集树上所有苹果的最少时间"
aliases: ["yiduobo的每日leetcode 1443.收集树上所有苹果的最少时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/410406086"
zhihu_id: "410406086"
zhihu_title: "yiduobo的每日leetcode 1443.收集树上所有苹果的最少时间"
question_id: "1443"
question: "收集树上所有苹果的最少时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-collect-all-apples-in-a-tree/"
created: "2021-09-14T21:13:30+08:00"
updated: "2021-09-14T21:13:30+08:00"
upvotes: 0
comments: 0
---

# 1443. 收集树上所有苹果的最少时间

> **[yiduobo的每日leetcode 1443.收集树上所有苹果的最少时间](https://zhuanlan.zhihu.com/p/410406086) · 知乎 · 2021-09-14 · 赞同 0**
> 力扣：[1443. 收集树上所有苹果的最少时间](https://leetcode.cn/problems/minimum-time-to-collect-all-apples-in-a-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1443.收集树上所有苹果的最少时间

[力扣](https://leetcode-cn.com/problems/minimum-time-to-collect-all-apples-in-a-tree/)

对于树中的一个节点而言，只有当这个节点上有苹果，或者其子树中有苹果时才有必要走到这个节点上。如果有必要走到这个节点，那么需要一来一去两点代价。

那么可以从根节点开始进行dfs，对于当前节点now：

1、首先遍历now的所有孩子节点next，考察其所有子树是否有苹果，以及拿到苹果所需的代价值之和cost。

2、若当前节点上有苹果，或者cost大于0，那么说明有必要走到当前节点，因此此时应该返回cost + 2，否则返回0，说明不需要走到这个节点来。

dfs完成后，最终答案还需要减去2，因为根节点是不需要两点代价的。另外需要注意特别判断树中只有一个节点的情况，此时答案必然为0。

最后附上python代码：

```python
class Solution(object):
    def minTime(self, n, edges, hasApple):
        """
        :type n: int
        :type edges: List[List[int]]
        :type hasApple: List[bool]
        :rtype: int
        """

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        used = [False] * n
        res = max(self.dfs(0, g, hasApple, used) - 2, 0)
        return res
        

    def dfs(self, now, g, hasApple, used):
        used[now] = True
        cost = 0
        for next in g.get(now, set()):
            if not used[next]:
                cost += self.dfs(next, g, hasApple, used)

        if cost > 0 or hasApple[now]:
            return cost + 2
        else:
            return 0
```
