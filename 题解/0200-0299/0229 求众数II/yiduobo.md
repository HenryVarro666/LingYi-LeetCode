---
title: "229. 求众数II"
aliases: ["yiduobo的每日leetcode 229.求众数II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/149736377"
zhihu_id: "149736377"
zhihu_title: "yiduobo的每日leetcode 229.求众数II"
question_id: "229"
question: "求众数II"
problem_url: "https://leetcode.cn/problems/majority-element-ii/"
created: "2020-06-20T23:46:35+08:00"
updated: "2020-06-20T23:46:35+08:00"
upvotes: 0
comments: 0
---

# 229. 求众数II

> **[yiduobo的每日leetcode 229.求众数II](https://zhuanlan.zhihu.com/p/149736377) · 知乎 · 2020-06-20 · 赞同 0**
> 力扣：[229. 求众数II](https://leetcode.cn/problems/majority-element-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

229.求众数II<https://leetcode-cn.com/problems/majority-element-ii/>

169题的升级版（传送门在这里[yiduobo：yiduobo的每日leetcode 169.多数元素](https://zhuanlan.zhihu.com/p/144788323)），做法也是大同小异。169题是对一个候选者投票，这里最多可能有两个数出现次数超过三分之一，于是对两个数进行投票，具体做法为维护两个候选的数，如果新来的数与这两个数都不相同，那么这两个候选者的计数器分别减一，相当于这三票抵消。如果与其中某个数相同，则对应的计数器加一。当某个数的计数器变成0时，需要重新选择候选的数来替代这个数。

需要注意的是，投票完成后还需要一趟扫描检测当前的两个候选的数出现次数是否满足条件。

最后附上python代码：

```python
class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        cnt1 = cnt2 = 0
        x = y = None
        for num in nums:
            if x == num:
                cnt1 += 1
            elif y == num:
                cnt2 += 1
            elif cnt1 == 0:
                x = num
                cnt1 = 1
            elif cnt2 == 0:
                y = num
                cnt2 = 1
            else:
                cnt1 -= 1
                cnt2 -= 1

        cnt1 = cnt2 = 0
        for num in nums:
            if num == x:
                cnt1 += 1
            elif num == y:
                cnt2 += 1
        
        res = []
        if cnt1 > len(nums) / 3:
            res.append(x)
        if cnt2 > len(nums) / 3:
            res.append(y)

        return res
```
