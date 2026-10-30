---
title: "2378. 选择边来最大化树的得分"
aliases: ["yiduobo的每日leetcode 2378.选择边来最大化树的得分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/630788234"
zhihu_id: "630788234"
zhihu_title: "yiduobo的每日leetcode 2378.选择边来最大化树的得分"
question_id: "2378"
question: "选择边来最大化树的得分"
problem_url: "https://leetcode.cn/problems/choose-edges-to-maximize-score-in-a-tree/"
created: "2023-05-20T04:51:03+08:00"
updated: "2023-05-20T04:51:03+08:00"
upvotes: 0
comments: 0
---

# 2378. 选择边来最大化树的得分

> **[yiduobo的每日leetcode 2378.选择边来最大化树的得分](https://zhuanlan.zhihu.com/p/630788234) · 知乎 · 2023-05-20 · 赞同 0**
> 力扣：[2378. 选择边来最大化树的得分](https://leetcode.cn/problems/choose-edges-to-maximize-score-in-a-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2378.选择边来最大化树的得分

[力扣](https://leetcode.cn/problems/choose-edges-to-maximize-score-in-a-tree/)

经典的树形动态规划问题，令f[node][flag]表示对于以node为根节点的子树，若其根节点node与node的根节点的边被选择的情况为flag时，子树中最大的得分是多少。在这里flag的取值为true或者false，也就是node与node的根节点之间的边被选择过了，或者没有被选择。

那么对于f[node][flag]：

1、当flag为true时：

对于node的所有孩子节点child而言，都不能选择node与child之间的边，于是就有

f\[node\]\[true\] \= f\[child\[0\]\]\[false\] + f\[child\[1\]\]\[false\] + ... + f\[child\[-1\]\]\[false\]

2、当flag为false时：

同样也可以不选择任意node与child之间的边，于是可以初始化f[node][true]为上面的式子

当然也可以选择某个child与node之间的边，此时就需要使用f[child][true]替代f[child][false]，同时需要将node到child之间的边也加入到得分中，于是就有

f[node][false] \= max(f[node][false], f[node][true] - f[child][false] + f[child][true] + edges[child][1])

而最终答案就是f[root][false]。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: int
        """

        n = len(edges)

        g = [[] for _ in range(n)]

        for index, (p, w) in enumerate(edges):
            if p != -1:
                g[p].append([index, w])
        
        f = [[None] * 2 for _ in range(n)]

        def dfs(now, flag):
            if f[now][flag] is None:
                f[now][flag] = 0
                max_delta = 0
                for child, w in g[now]:
                    v = max(0, dfs(child, False))
                    f[now][flag] += v
                    if not flag:
                        delta = max(0, dfs(child, True)) + w - v
                        max_delta = max(max_delta, delta)
                
                if not flag:
                    f[now][flag] += max_delta
            
            return f[now][flag]
                

        return dfs(0, False)
```
