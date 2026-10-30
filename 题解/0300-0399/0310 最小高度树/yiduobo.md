---
title: "310. 最小高度树"
aliases: ["yiduobo的每日leetcode 310.最小高度树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/158640075"
zhihu_id: "158640075"
zhihu_title: "yiduobo的每日leetcode 310.最小高度树"
question_id: "310"
question: "最小高度树"
problem_url: "https://leetcode.cn/problems/minimum-height-trees/"
created: "2020-07-11T00:19:04+08:00"
updated: "2020-07-11T00:19:04+08:00"
upvotes: 0
comments: 0
---

# 310. 最小高度树

> **[yiduobo的每日leetcode 310.最小高度树](https://zhuanlan.zhihu.com/p/158640075) · 知乎 · 2020-07-11 · 赞同 0**
> 力扣：[310. 最小高度树](https://leetcode.cn/problems/minimum-height-trees/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

310.最小高度树<https://leetcode-cn.com/problems/minimum-height-trees/>

题目要求我们为树选择一个根节点，使得树的高度最小。直观的想法就是先找到树中距离最远的两个点，然后选择这两个点的中点作为根节点。

实际上，树中距离最远的两个点一般称之为树的直径，可以通过两次dfs获得，即从树中任意一点M开始进行dfs，走到离M最远的点N，然后从N开始dfs，走到离N最远的点O，那么N到O之间就是树的直径。具体证明也比较简单：

1、若M本身就在直径上，那么N显然为直径的某一端，而O跟着就是直径的另一端了。

2、若M不在直径上，若此时NO不是树的直径，那么不妨设树的直径为AB，那么NO可能与AB直接相交，或者通过某条路径CD相连。不管是哪种情况，考察P到A的距离就可以发现，PA一定是大于AB的，这与AB是树的直径相矛盾，于是NO必然是树的直径。

获得树的直径之后，从其中某个点出发，走直径长度的一半就找到要求的根节点了。

最后附上python代码：

```python
class Solution(object):
    def findMinHeightTrees(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: List[int]
        """

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = []
            if y not in g:
                g[y] = []
            g[x].append(y)
            g[y].append(x)

        node, l = self.dfs(0, None, 0, None, g)
        other_node, d = self.dfs(node, None, 0, None, g)

        res, l = self.dfs(node, d / 2, 0, None, g)
        if d % 2 == 1:
            res1, l = self.dfs(node, d / 2 + 1, 0, None, g)
            return [res, res1]
        return [res]

    def dfs(self, now, aim_len, now_len, fa, g):
        if aim_len is not None:
            if aim_len == now_len:
                return now, now_len

        res = now
        choose_len = now_len

        for next_node in g.get(now, []):
            if next_node != fa:
                tmp_res, tmp_len = self.dfs(next_node, aim_len, now_len + 1, now, g)
                if tmp_len > choose_len:
                    choose_len = tmp_len
                    res = tmp_res
        
        return res, choose_len
```
