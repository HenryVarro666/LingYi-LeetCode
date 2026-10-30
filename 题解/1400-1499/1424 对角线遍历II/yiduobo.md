---
title: "1424. 对角线遍历II"
aliases: ["yiduobo的每日leetcode 1424.对角线遍历II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/408405239"
zhihu_id: "408405239"
zhihu_title: "yiduobo的每日leetcode 1424.对角线遍历II"
question_id: "1424"
question: "对角线遍历II"
problem_url: "https://leetcode.cn/problems/diagonal-traverse-ii/"
created: "2021-09-08T23:36:14+08:00"
updated: "2021-09-08T23:36:14+08:00"
upvotes: 0
comments: 0
---

# 1424. 对角线遍历II

> **[yiduobo的每日leetcode 1424.对角线遍历II](https://zhuanlan.zhihu.com/p/408405239) · 知乎 · 2021-09-08 · 赞同 0**
> 力扣：[1424. 对角线遍历II](https://leetcode.cn/problems/diagonal-traverse-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1424.对角线遍历II

[力扣](https://leetcode-cn.com/problems/diagonal-traverse-ii/)

题目要求按照左对角线进行遍历，这种对角线的特点是位于同一对角线上的格子，其横纵坐标之和是一样的，于是一个自然的想法是遍历列表中的所有数字，对于位于第i行第j列的数字nums[i][j]，我们将其转化成三元组（i + j, i, nums[i][j]），并使用记录下所有的三元组。

接下来我们对所有的三元组按照i + j作为第一关键字从小到大，i作为第二关键字从大到小进行排序，并将排序后的nums输出即可。

最后附上python代码：

```python
class Solution(object):
    def findDiagonalOrder(self, nums):
        """
        :type nums: List[List[int]]
        :rtype: List[int]
        """

        num_list = []
        for i in range(len(nums)):
            for j in range(len(nums[i])):
                num_list.append([i + j, i, nums[i][j]])
        
        return [x[2] for x in sorted(num_list, key=lambda d:(d[0], -d[1]))]
```
