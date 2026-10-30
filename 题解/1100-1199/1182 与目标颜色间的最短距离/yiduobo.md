---
title: "1182. 与目标颜色间的最短距离"
aliases: ["yiduobo的每日leetcode 1182.与目标颜色间的最短距离"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/612142086"
zhihu_id: "612142086"
zhihu_title: "yiduobo的每日leetcode 1182.与目标颜色间的最短距离"
question_id: "1182"
question: "与目标颜色间的最短距离"
problem_url: "https://leetcode.cn/problems/shortest-distance-to-target-color/"
created: "2023-03-07T21:36:45+08:00"
updated: "2023-03-07T21:36:45+08:00"
upvotes: 0
comments: 0
---

# 1182. 与目标颜色间的最短距离

> **[yiduobo的每日leetcode 1182.与目标颜色间的最短距离](https://zhuanlan.zhihu.com/p/612142086) · 知乎 · 2023-03-07 · 赞同 0**
> 力扣：[1182. 与目标颜色间的最短距离](https://leetcode.cn/problems/shortest-distance-to-target-color/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1182.与目标颜色间的最短距离

[力扣](https://leetcode.cn/problems/shortest-distance-to-target-color/)

首先正反两趟遍历，预处理出两个数组left和right，其含义为对于每个位置，其左侧和右侧最近的1、2、3所在的下标。得到left和right后，那么对于一个查询(i, c)，其左侧最近的c的下标就是left[i][c]，而右侧最近的c的下标是right[i][c]，因此这个查询的结果就是min(i - left[i][c], right[i][c] - i)。

在具体实现上，由于数组下标从0开始，因此下标i两侧最近的颜色c在left和right中的下标应该是left[i][c - 1]以及right[i][c - 1]。

最后附上python代码：

```python
class Solution(object):
    def shortestDistanceColor(self, colors, queries):
        """
        :type colors: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        n = len(colors)

        left = [-n, -n, -n]
        left_list = []
        for index in range(n):
            left[colors[index] - 1] = index
            left_list.append(left[:])
        
        right = [n + n, n + n, n + n]
        right_list = []
        for index in range(n - 1, -1, -1):
            right[colors[index] - 1] = index
            right_list.append(right[:])
        
        right_list.reverse()

        res = []
        for index, c in queries:
            mi = min(index - left_list[index][c - 1], right_list[index][c - 1] - index)
            if mi >= n:
                mi = -1
            res.append(mi)
        
        return res
```
