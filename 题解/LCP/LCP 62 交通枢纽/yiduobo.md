---
title: "LCP 62. 交通枢纽"
aliases: ["yiduobo的每日leetcode LCP62.交通枢纽"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/579203622"
zhihu_id: "579203622"
zhihu_title: "yiduobo的每日leetcode LCP62.交通枢纽"
question_id: "LCP 62"
question: "交通枢纽"
problem_url: "https://leetcode.cn/problems/D9PW8w/"
difficulty: "Medium"
created: "2022-11-01T00:57:10+08:00"
updated: "2022-11-01T00:57:10+08:00"
upvotes: 0
comments: 0
---

# LCP 62. 交通枢纽

> **[yiduobo的每日leetcode LCP62.交通枢纽](https://zhuanlan.zhihu.com/p/579203622) · 知乎 · 2022-11-01 · 赞同 0**
> 力扣：[LCP 62. 交通枢纽](https://leetcode.cn/problems/D9PW8w/) · Medium · 灵茶山艾府：[按题意模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP62.交通枢纽

[力扣](https://leetcode.cn/problems/D9PW8w/)

题目给出一张图，要求找出图中入度为n - 1，且出度为0的点。在这里有一个隐藏条件就是这样的点不可能同时出现两个，因为若其中一个点出度为0，那么对于另外的点而言，就不存在从这个出度为0发出的边，那么其他点的入度自然不可能是n - 1了。

如果题目给出图是邻接矩阵，那么利用上面这个结论就可以在O(n)的时间内找出最终答案。本题给出的邻接表，那么就只能遍历所有边，统计每个节点的入度和出度，然后再遍历每个节点，找出入度为n - 1且出度为0的节点。

最后附上python代码：

```python
class Solution(object):
    def transportationHub(self, path):
        """
        :type path: List[List[int]]
        :rtype: int
        """

        ind = {}
        oud = {}
        node_set = set()
        for x, y in path:
            ind[y] = ind.get(y, 0) + 1
            oud[x] = oud.get(x, 0) + 1
            node_set.add(x)
            node_set.add(y)
        
        for res in node_set:
            if ind.get(res, 0) == len(node_set) - 1 and res not in oud:
                return res
        
        return -1
```
