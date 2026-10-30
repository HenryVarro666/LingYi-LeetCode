---
title: "1743. 从相邻元素对还原数组"
aliases: ["yiduobo的每日leetcode 1743.从相邻元素对还原数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/454221148"
zhihu_id: "454221148"
zhihu_title: "yiduobo的每日leetcode 1743.从相邻元素对还原数组"
question_id: "1743"
question: "从相邻元素对还原数组"
problem_url: "https://leetcode.cn/problems/restore-the-array-from-adjacent-pairs/"
created: "2022-01-06T23:56:25+08:00"
updated: "2022-01-06T23:56:25+08:00"
upvotes: 1
comments: 0
---

# 1743. 从相邻元素对还原数组

> **[yiduobo的每日leetcode 1743.从相邻元素对还原数组](https://zhuanlan.zhihu.com/p/454221148) · 知乎 · 2022-01-06 · 赞同 1**
> 力扣：[1743. 从相邻元素对还原数组](https://leetcode.cn/problems/restore-the-array-from-adjacent-pairs/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1743.从相邻元素对还原数组

[力扣](https://leetcode-cn.com/problems/restore-the-array-from-adjacent-pairs/)

题目非常贴心地限定了数组中每个数字只出现了一次，那么对于数组中最左侧和最右侧的两个数而言，其只会在相邻元素对当中出现一次，于是可以找出只出现一次的数字，应该可以找到两个。任选一个填到数组最左侧，不妨设这个数为x。那么此时与x形成相邻元素的数字y就必然是x右边那个数字，而对于y而言，除了x之外应该还存在一个数z位于y的右侧，那么找到这个z填充在y的右侧之后并重复这个过程，直到填满整个数组即可。

更进一步的，如果这里没有限制每个数只出现一次，那么就需要用到图论中欧拉路径的知识，在这里就不展开了。

最后附上python代码：

```python
class Solution(object):
    def restoreArray(self, adjacentPairs):
        """
        :type adjacentPairs: List[List[int]]
        :rtype: List[int]
        """

        g = {}
        for x, y in adjacentPairs:
            if x not in g:
                g[x] = []
            g[x].append(y)
            if y not in g:
                g[y] = []
            g[y].append(x)
        
        for x in g:
            if len(g[x]) == 1:
                break
        
        res = [x]
        used = set([x])
        while len(res) < len(adjacentPairs) + 1:
            x = res[-1]
            if g[x][0] not in used:
                res.append(g[x][0])
                used.add(g[x][0])
            else:
                res.append(g[x][1])
                used.add(g[x][1])
        
        return res
```
