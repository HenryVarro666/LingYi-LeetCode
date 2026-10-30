---
title: "1272. 删除区间"
aliases: ["yiduobo的每日leetcode 1272.删除区间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/615593660"
zhihu_id: "615593660"
zhihu_title: "yiduobo的每日leetcode 1272.删除区间"
question_id: "1272"
question: "删除区间"
problem_url: "https://leetcode.cn/problems/remove-interval/"
created: "2023-03-20T22:15:05+08:00"
updated: "2023-03-20T22:15:05+08:00"
upvotes: 0
comments: 0
---

# 1272. 删除区间

> **[yiduobo的每日leetcode 1272.删除区间](https://zhuanlan.zhihu.com/p/615593660) · 知乎 · 2023-03-20 · 赞同 0**
> 力扣：[1272. 删除区间](https://leetcode.cn/problems/remove-interval/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1272.删除区间

[力扣](https://leetcode.cn/problems/remove-interval/)

首先，题目描述的区间虽然是实数，但是各个区间的边界点都是整数点，因此也可以认为是离散的整数区间问题。接下来，对于本题中的区间以及移除区间，可以认为是对于区间中的某一段执行全部加上1或者减去1的操作，问最终区间中连续的1有哪些。对于这个问题，则可以利用差分数组来处理。

令f表示差分数组，那么对于intervals中的区间[x, y)，需要将f[x]加上1，f[y]减去1，而对于toBeRemoved这个区间[x, y），则需要将f[x]减去1，f[y]加上1。处理完成后，从小到大遍历所有的区间边界，累积这个f。若某一时刻累加值从1变为了0，说明当前来到了一个幸存区间的右边界，而上一个遍历到的区间边界就是当前幸存区间的左边界，需要将这两个区间边界组成的区间加入到最终答案中。

最后附上python代码：

```python
class Solution(object):
    def removeInterval(self, intervals, toBeRemoved):
        """
        :type intervals: List[List[int]]
        :type toBeRemoved: List[int]
        :rtype: List[List[int]]
        """

        points = []
        for x, y in intervals:
            points.append([x, 1])
            points.append([y, -1])
        
        points.append([toBeRemoved[0], -1])
        points.append([toBeRemoved[1], 1])
        points.sort()

        last = None
        now = 0
        res = []
        for x, v in points:
            now += v
            if v == -1 and now == 0:
                res.append([last, x])
            last = x
        
        return res
```
