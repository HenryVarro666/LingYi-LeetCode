---
title: "1376. 通知所有员工所需的时间"
aliases: ["yiduobo的每日leetcode 1376.通知所有员工所需的时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/401596768"
zhihu_id: "401596768"
zhihu_title: "yiduobo的每日leetcode 1376.通知所有员工所需的时间"
question_id: "1376"
question: "通知所有员工所需的时间"
problem_url: "https://leetcode.cn/problems/time-needed-to-inform-all-employees/"
difficulty: "Medium"
rating: 1561
created: "2021-08-19T22:24:55+08:00"
updated: "2021-08-19T22:24:55+08:00"
upvotes: 2
comments: 0
---

# 1376. 通知所有员工所需的时间

> **[yiduobo的每日leetcode 1376.通知所有员工所需的时间](https://zhuanlan.zhihu.com/p/401596768) · 知乎 · 2021-08-19 · 赞同 2**
> 力扣：[1376. 通知所有员工所需的时间](https://leetcode.cn/problems/time-needed-to-inform-all-employees/) · Medium · 灵茶山艾府：[深入理解递归：自顶向下/自底向上/记忆化搜索（附 O(1) 空间迭代写法！）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1376.通知所有员工所需的时间

[力扣](https://leetcode-cn.com/problems/time-needed-to-inform-all-employees/)

题目保证从属关系可以用一棵树来表示，那么我们也可以将其视为一个有向连通图，那么对于点i出发的边，其边长就是informTime[i]。

接下来我们从根开始进行一趟bfs，计算从根节点开始到每个节点的距离，然后取其中的最大值作为答案即可。

具体来说，对于点x，我们设根节点到x的距离为f[x]，那么x只能从fa[x]走过来，于是就有

f\[x\] \= f\[fa\[x\]\] + informTime\[fa\[x\]\]

最后附上python代码：

```python
class Solution(object):
    def numOfMinutes(self, n, headID, manager, informTime):
        """
        :type n: int
        :type headID: int
        :type manager: List[int]
        :type informTime: List[int]
        :rtype: int
        """

        g = {x : set() for x in range(n)}
        q = []
        f = [0] * n
        for index, x in enumerate(manager):
            if x == -1:
                q.append(index)
            else:
                g[x].add(index)
        
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                f[next] = f[now] + informTime[now]
                q.append(next)
                r += 1
        
        return max(f)
```
