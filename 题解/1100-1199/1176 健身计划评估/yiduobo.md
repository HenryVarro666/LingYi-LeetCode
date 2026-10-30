---
title: "1176. 健身计划评估"
aliases: ["yiduobo的每日leetcode 1176.健身计划评估"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/611872674"
zhihu_id: "611872674"
zhihu_title: "yiduobo的每日leetcode 1176.健身计划评估"
question_id: "1176"
question: "健身计划评估"
problem_url: "https://leetcode.cn/problems/diet-plan-performance/"
created: "2023-03-06T23:34:38+08:00"
updated: "2023-03-06T23:34:38+08:00"
upvotes: 0
comments: 0
---

# 1176. 健身计划评估

> **[yiduobo的每日leetcode 1176.健身计划评估](https://zhuanlan.zhihu.com/p/611872674) · 知乎 · 2023-03-06 · 赞同 0**
> 力扣：[1176. 健身计划评估](https://leetcode.cn/problems/diet-plan-performance/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1176.健身计划评估

<https://leetcode.cn/problems/diet-plan-performance/>

非常标准的滑动窗口问题。使用一个长度为k的窗口向后滑动，每一轮滑动都先计算出新的窗口内的卡路里之和，然后与upper和lower的大小关系更新答案。

最后附上python代码：

```python
class Solution(object):
    def dietPlanPerformance(self, calories, k, lower, upper):
        """
        :type calories: List[int]
        :type k: int
        :type lower: int
        :type upper: int
        :rtype: int
        """

        res = 0
        now = sum(calories[:k])

        if now > upper:
            res = 1
        elif now < lower:
            res = -1
        
        for index, c in enumerate(calories[k:]):
            now += c
            now -= calories[index]
            if now > upper:
                res += 1
            elif now < lower:
                res -= 1
        
        return res
```
