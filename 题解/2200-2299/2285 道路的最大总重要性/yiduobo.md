---
title: "2285. 道路的最大总重要性"
aliases: ["yiduobo的每日leetcode 2285.道路的最大总重要性"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/graph", "leetcode/math", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/552056392"
zhihu_id: "552056392"
zhihu_title: "yiduobo的每日leetcode 2285.道路的最大总重要性"
question_id: "2285"
question: "道路的最大总重要性"
problem_url: "https://leetcode.cn/problems/maximum-total-importance-of-roads/"
difficulty: "Medium"
rating: 1496
created: "2022-08-10T13:10:45+08:00"
updated: "2022-08-10T13:10:45+08:00"
upvotes: 0
comments: 0
---

# 2285. 道路的最大总重要性

> **[yiduobo的每日leetcode 2285.道路的最大总重要性](https://zhuanlan.zhihu.com/p/552056392) · 知乎 · 2022-08-10 · 赞同 0**
> 力扣：[2285. 道路的最大总重要性](https://leetcode.cn/problems/maximum-total-importance-of-roads/) · Medium · 灵茶山艾府：[排序不等式](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2285.道路的最大总重要性

[力扣](https://leetcode.cn/problems/maximum-total-importance-of-roads/)

题目将对每条边的两个节点计算重要性，也就是说一个节点的度是多少，该节点的重要性就会被计算多少次。因此可以先遍历每条边，计算每个点的度。接下来从小到大进行排序，按顺序将重要性分配给排序后的节点即可。

最后附上python代码：

```python
class Solution(object):
    def maximumImportance(self, n, roads):
        """
        :type n: int
        :type roads: List[List[int]]
        :rtype: int
        """

        tot_d = [0] * n
        for x, y in roads:
            tot_d[x] += 1
            tot_d[y] += 1

        res = 0
        for index, d in enumerate(sorted(tot_d)):
            res += (index + 1) * d
        
        return res
```
