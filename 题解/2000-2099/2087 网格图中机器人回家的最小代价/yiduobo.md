---
title: "2087. 网格图中机器人回家的最小代价"
aliases: ["yiduobo的每日leetcode 2087.网格图中机器人回家的最小代价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/518916205"
zhihu_id: "518916205"
zhihu_title: "yiduobo的每日leetcode 2087.网格图中机器人回家的最小代价"
question_id: "2087"
question: "网格图中机器人回家的最小代价"
problem_url: "https://leetcode.cn/problems/minimum-cost-homecoming-of-a-robot-in-a-grid/"
difficulty: "Medium"
rating: 1744
created: "2022-05-24T00:32:44+08:00"
updated: "2022-05-24T00:32:44+08:00"
upvotes: 0
comments: 0
---

# 2087. 网格图中机器人回家的最小代价

> **[yiduobo的每日leetcode 2087.网格图中机器人回家的最小代价](https://zhuanlan.zhihu.com/p/518916205) · 知乎 · 2022-05-24 · 赞同 0**
> 力扣：[2087. 网格图中机器人回家的最小代价](https://leetcode.cn/problems/minimum-cost-homecoming-of-a-robot-in-a-grid/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2087.网格图中机器人回家的最小代价

[力扣](https://leetcode.cn/problems/minimum-cost-homecoming-of-a-robot-in-a-grid/)

题目中行列互不影响，那么可以分开来考虑。

不妨先考虑行。要从起始行走到目标行，这中间的所有行都必须经过至少一次。由于每次经过的代价都是非负的，那么经过的次数自然是越少越好，于是最优的做法就是从起始行直接往目标行走。

同样的，对于列而言，最优的做法也是从起始列直接往目标列走。

根据上面的结论，分别从起始行和起始列开始，向目标行和目标列遍历，累加期间经过的行和列的cost即可。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, startPos, homePos, rowCosts, colCosts):
        """
        :type startPos: List[int]
        :type homePos: List[int]
        :type rowCosts: List[int]
        :type colCosts: List[int]
        :rtype: int
        """

        row_delta = col_delta = 1
        if startPos[0] > homePos[0]:
            row_delta = -1
        if startPos[1] > homePos[1]:
            col_delta = -1
        
        res = 0
        for index in range(startPos[0] + row_delta, homePos[0] + row_delta, row_delta):
            res += rowCosts[index]
        for index in range(startPos[1] + col_delta, homePos[1] + col_delta, col_delta):
            res += colCosts[index]
        
        return res
```
