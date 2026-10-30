---
title: "3004. 相同颜色的最大子树"
aliases: ["yiduobo的每日leetcode 3004.相同颜色的最大子树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/693509546"
zhihu_id: "693509546"
zhihu_title: "yiduobo的每日leetcode 3004.相同颜色的最大子树"
question_id: "3004"
question: "相同颜色的最大子树"
problem_url: "https://leetcode.cn/problems/maximum-subtree-of-the-same-color/"
created: "2024-04-20T01:34:19+08:00"
updated: "2024-04-20T01:34:19+08:00"
upvotes: 1
comments: 0
---

# 3004. 相同颜色的最大子树

> **[yiduobo的每日leetcode 3004.相同颜色的最大子树](https://zhuanlan.zhihu.com/p/693509546) · 知乎 · 2024-04-20 · 赞同 1**
> 力扣：[3004. 相同颜色的最大子树](https://leetcode.cn/problems/maximum-subtree-of-the-same-color/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3004.相同颜色的最大子树

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-subtree-of-the-same-color/description/)

对于以now为根节点的子树而言，其为同色子树的条件为：

1、now为叶子节点

2、now不是叶子节点，且now的所有子节点的颜色与now相同，同时以now的所有子节点为根节点的子树，也是同色子树

基于这一点，就可以从根节点向下递归求解。对于当前处理的节点now，遍历其所有孩子节点并递归求解计算孩子节点是否同色，以及其中的节点总数。若存在某个孩子节点与now不同色，或者不是同色子树，那么说明now不是同色子树，否则将该子树中的节点数量累加到以now为根节点的节点总数中即可。

最后附上python代码：

```python
class Solution(object):
    def maximumSubtreeSize(self, edges, colors):
        """
        :type edges: List[List[int]]
        :type colors: List[int]
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
        

        def dfs(now, fa):
            cnt = 1

            for son in g.get(now, set()):
                if son != fa:
                    son_cnt = dfs(son, now)
                    if colors[son] == colors[now]:
                        if son_cnt == -1:
                            cnt = -1
                        elif cnt != -1:
                            cnt += son_cnt
                    else:
                        cnt = -1
            
            
            global res
            res = max(res, cnt)

            return cnt
        

        global res
        res = 0
        dfs(0, -1)
        return res
```
