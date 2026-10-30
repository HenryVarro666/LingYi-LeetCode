---
title: "2374. 边积分最高的节点"
aliases: ["yiduobo的每日leetcode 2374.边积分最高的节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/array"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/563658149"
zhihu_id: "563658149"
zhihu_title: "yiduobo的每日leetcode 2374.边积分最高的节点"
question_id: "2374"
question: "边积分最高的节点"
problem_url: "https://leetcode.cn/problems/node-with-highest-edge-score/"
difficulty: "Medium"
created: "2022-09-12T17:59:25+08:00"
updated: "2022-09-12T17:59:25+08:00"
upvotes: 0
comments: 0
---

# 2374. 边积分最高的节点

> **[yiduobo的每日leetcode 2374.边积分最高的节点](https://zhuanlan.zhihu.com/p/563658149) · 知乎 · 2022-09-12 · 赞同 0**
> 力扣：[2374. 边积分最高的节点](https://leetcode.cn/problems/node-with-highest-edge-score/) · Medium · 灵茶山艾府：[一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2374.边积分最高的节点

[力扣](https://leetcode.cn/problems/node-with-highest-edge-score/)

直接遍历每一条边，使用一个数组score记录下每个节点的积分。对于边(x, y)，按照题目中对积分的定义就应该是将x累加到score[y]当中。

遍历完成后，score中最大值对应的节点就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def edgeScore(self, edges):
        """
        :type edges: List[int]
        :rtype: int
        """

        n = len(edges)
        scores = [0] * n
        for x, y in enumerate(edges):
            scores[y] += x
        
        res = 0
        ma = scores[0]
        for x in range(1, n):
            if scores[x] > ma:
                res = x
                ma = scores[x]
        
        return res
```
