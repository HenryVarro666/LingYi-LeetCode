---
title: "684. 冗余连接"
aliases: ["yiduobo的每日leetcode 684.冗余连接"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/303313792"
zhihu_id: "303313792"
zhihu_title: "yiduobo的每日leetcode 684.冗余连接"
question_id: "684"
question: "冗余连接"
problem_url: "https://leetcode.cn/problems/redundant-connection/"
created: "2020-11-20T23:57:27+08:00"
updated: "2020-11-20T23:57:27+08:00"
upvotes: 0
comments: 0
---

# 684. 冗余连接

> **[yiduobo的每日leetcode 684.冗余连接](https://zhuanlan.zhihu.com/p/303313792) · 知乎 · 2020-11-20 · 赞同 0**
> 力扣：[684. 冗余连接](https://leetcode.cn/problems/redundant-connection/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

684.冗余连接

[力扣](https://leetcode-cn.com/problems/redundant-connection/)

题目给出一个图，其中存在一个环，需要找到构成环的那一条边是什么。由于题目只存在一个环，因此可以使用并查集来做，具体来说就是通过并查集维护一个祖先数组fa，其中fa[x]表示x的祖先节点的编号。接下来按顺序枚举每条边，设这条边上的两点为x与y，那么祖先节点分别为fa[x]以及fa[y]。若此时fa[x]不等于fa[y]，那么我们将较大的点的祖先指向较小的点；若此时fa[x]等于fa[y]，说明二者已经通过别的边连接在一起了，因此当前边就是最终的答案。

最后附上python代码：

```python
class Solution(object):
    def findRedundantConnection(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: List[int]
        """
        
        n = len(edges)
        fa = [index for index in range(n)]

        for edge in edges:
            x, y = edge
            x -= 1
            y -= 1
            if self.find(x, fa) == self.find(y, fa):
                return edge
            
            if fa[x] < fa[y]:
                fa[fa[y]] = fa[x]
            else:
                fa[fa[x]] = fa[y]

    def find(self, x, fa):
        if fa[x] == x:
            return x
        
        tmp = self.find(fa[x], fa)
        fa[x] = tmp
        return tmp
```
