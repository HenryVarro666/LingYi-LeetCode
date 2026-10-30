---
title: "2998. 使X和Y相等的最少操作次数"
aliases: ["yiduobo的每日leetcode 2998.使X和Y相等的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/memoization", "题单/动态规划", "题单/图论算法", "题单/动态规划/其他", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/692886538"
zhihu_id: "692886538"
zhihu_title: "yiduobo的每日leetcode 2998.使X和Y相等的最少操作次数"
question_id: "2998"
question: "使 X 和 Y 相等的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-make-x-and-y-equal/"
difficulty: "Medium"
rating: 1795
created: "2024-04-17T03:36:56+08:00"
updated: "2024-04-17T03:36:56+08:00"
upvotes: 1
comments: 0
---

# 2998. 使X和Y相等的最少操作次数

> **[yiduobo的每日leetcode 2998.使X和Y相等的最少操作次数](https://zhuanlan.zhihu.com/p/692886538) · 知乎 · 2024-04-17 · 赞同 1**
> 力扣：[2998. 使 X 和 Y 相等的最少操作次数](https://leetcode.cn/problems/minimum-number-of-operations-to-make-x-and-y-equal/) · Medium · 灵茶山艾府：[两种方法：BFS/记忆化搜索（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2998.使X和Y相等的最少操作次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-operations-to-make-x-and-y-equal/description/)

首先，题目中的四种操作只有加1操作可以使得x变大，因此当x小于y时，答案就是y - x。

接下来对于x大于等于y的情况，则可以从x开始进行bfs，每次尝试四种操作来扩展bfs队列。由于x和y的取值范围不大，且bfs存在一个轮次的上界，也就是x - y，因此在这里可以直接暴力bfs，无需针对5和11的情况进行优化。

最后附上python代码：

```python
class Solution(object):
    def minimumOperationsToMakeEqual(self, x, y):
        """
        :type x: int
        :type y: int
        :rtype: int
        """

        if x < y:
            return y - x
        
        vis = set([x])
        q = [x]
        head, tail = 0, 1
        for rnd in range(x - y):
            for x in q[head : tail]:
                if x % 5 == 0 and x // 5 not in vis:
                    q.append(x // 5)
                    vis.add(q[-1])
                if x % 11 == 0 and x // 11 not in vis:
                    q.append(x // 11)
                    vis.add(q[-1])
                if x + 1 not in vis:
                    q.append(x + 1)
                    vis.add(q[-1])
                if x - 1 not in vis:
                    q.append(x - 1)
                    vis.add(q[-1])
                
                if y in vis:
                    return rnd + 1
            
            head, tail = tail, len(q)
        
        return x - y
```
