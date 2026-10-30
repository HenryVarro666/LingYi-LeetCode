---
title: "1064. 不动点"
aliases: ["yiduobo的每日leetcode 1064.不动点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/608034759"
zhihu_id: "608034759"
zhihu_title: "yiduobo的每日leetcode 1064.不动点"
question_id: "1064"
question: "不动点"
problem_url: "https://leetcode.cn/problems/fixed-point/"
created: "2023-02-20T23:47:00+08:00"
updated: "2023-02-20T23:47:00+08:00"
upvotes: 0
comments: 0
---

# 1064. 不动点

> **[yiduobo的每日leetcode 1064.不动点](https://zhuanlan.zhihu.com/p/608034759) · 知乎 · 2023-02-20 · 赞同 0**
> 力扣：[1064. 不动点](https://leetcode.cn/problems/fixed-point/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1064.不动点

[力扣](https://leetcode.cn/problems/fixed-point/)

题目要求找出最小的满足arr[i] \= i的下标i，那么在这里可以将数组先转化为b[i] \= arr[i] - i，问题就转化成了找出最小的下标i满足b[i] \= 0。

由于arr一开始是单调递增的，那么在b必然是单调不减的。要找出其中最小的满足b[i] \= 0的下标i，就可以使用二分查找来进行求解。

二分的上下边界初始值显然为0和n - 1，接下来对于当前二分到的mid，根据b[mid]与0的大小关系调整二分的上下界即可。

最后附上python代码：

```python
class Solution(object):
    def fixedPoint(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        n = len(arr)
        b = [arr[i] - i for i in range(n)]
        left = 0
        right = n - 1
        res = -1
        while left <= right:
            mid = (left + right) / 2
            if b[mid] == 0:
                res = mid
                right = mid - 1
            elif b[mid] < 0:
                left = mid + 1
            else:
                right = mid - 1
        
        return res
```
