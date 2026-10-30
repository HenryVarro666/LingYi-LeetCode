---
title: "1413. 逐步求和得到正数的最小值"
aliases: ["yiduobo的每日leetcode 1413.逐步求和得到正数的最小值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/406654451"
zhihu_id: "406654451"
zhihu_title: "yiduobo的每日leetcode 1413.逐步求和得到正数的最小值"
question_id: "1413"
question: "逐步求和得到正数的最小值"
problem_url: "https://leetcode.cn/problems/minimum-value-to-get-positive-step-by-step-sum/"
created: "2021-09-03T23:46:44+08:00"
updated: "2021-09-03T23:46:44+08:00"
upvotes: 0
comments: 0
---

# 1413. 逐步求和得到正数的最小值

> **[yiduobo的每日leetcode 1413.逐步求和得到正数的最小值](https://zhuanlan.zhihu.com/p/406654451) · 知乎 · 2021-09-03 · 赞同 0**
> 力扣：[1413. 逐步求和得到正数的最小值](https://leetcode.cn/problems/minimum-value-to-get-positive-step-by-step-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1413.逐步求和得到正数的最小值

[力扣](https://leetcode-cn.com/problems/minimum-value-to-get-positive-step-by-step-sum/)

比较基础的题目，直接一趟扫描计算前缀和，在计算的过程中找出前缀和中的最小值。若这个最小值为负数，那么这个最小值的倒数加上1就是最终答案，否则答案为1。

最后附上python代码：

```python
class Solution(object):
    def minStartValue(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 1
        now = 0
        for num in nums:
            now += num
            if now < 0:
                res = max(res, -now + 1)
        
        return res
```
